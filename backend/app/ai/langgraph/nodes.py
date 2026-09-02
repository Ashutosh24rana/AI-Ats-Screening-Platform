import logging
import os

from app.ai.chunking.resume_chunker import ResumeChunker
from app.ai.evaluation.evaluation_schemas import (
    ATSEvaluation,
    ExperienceEvaluation,
    FinalEvaluation,
    SemanticEvaluation,
    SkillEvaluation,
)
from app.ai.evaluation.experience_evaluator import ExperienceEvaluator
from app.ai.evaluation.final_scorer import calculate_final_score
from app.ai.evaluation.skill_matcher import SkillMatcher
from app.ai.loaders.resume_loader import ResumeLoader
from app.ai.rag.rag_pipeline import RAGPipeline
from app.ai.rag.prompt_templates import (
    ATS_QUALITY_PROMPT,
    EXPERIENCE_PROMPT,
    FINAL_SUMMARY_PROMPT,
    SEMANTIC_PROMPT,
    SKILL_MATCH_PROMPT,
)
from app.ai.vectorstore.pinecone_client import ResumeVectorStore
from app.utils.text_utils import clean_text, truncate_text

logger = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 12000


def _llm():
    from app.ai.rag.retriever import get_llm

    return get_llm()


def parse_resume_information(state: dict) -> dict:
    """Extract and clean raw text from the resume PDF, then store chunks in Pinecone."""
    try:
        path = state["resume_file_path"]
        # stored file_url is relative like "uploads/<candidate>/<file>"; resolve from cwd
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        loader = ResumeLoader()
        text = clean_text(loader.load_text(path))
        metadata = {
            "application_id": state["application_id"],
            "job_id": state["job_id"],
            "candidate_id": state["candidate_id"],
            "resume_id": state["resume_id"],
        }
        vector_store = ResumeVectorStore()
        chunks = ResumeChunker().split(text, metadata=metadata)
        vector_store.store_resume_chunks(chunks)
        return {"resume_text": text}
    except Exception as exc:  # noqa: BLE001
        logger.exception("Resume parsing failed")
        return {"error": f"Resume parsing failed: {exc}", "resume_text": ""}


def retrieve_relevant_chunks(state: dict) -> dict:
    """RAG retrieval: job-aware query -> Pinecone top-k chunks."""
    try:
        pipeline = RAGPipeline()
        context = pipeline.get_resume_context(
            job_title=state["job_title"],
            job_description=state["job_description"],
            required_skills=state["required_skills"],
            job_id=state["job_id"],
            candidate_id=state["candidate_id"],
        )
        if not context:
            # Fallback: use the most relevant sections of the full text directly.
            context = truncate_text(state.get("resume_text", ""), MAX_CONTEXT_CHARS)
        return {"resume_context": truncate_text(context, MAX_CONTEXT_CHARS)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("Retrieval failed; falling back to direct resume text")
        fallback = truncate_text(state.get("resume_text", ""), MAX_CONTEXT_CHARS)
        return {"resume_context": fallback, "error": None if fallback else f"Retrieval failed: {exc}"}


def evaluate_skill_match(state: dict) -> dict:
    prompt = SKILL_MATCH_PROMPT.format(
        job_title=state["job_title"],
        required_skills=", ".join(state["required_skills"]) or "None specified",
        preferred_skills=", ".join(state["preferred_skills"]) or "None",
        resume_context=state["resume_context"] or "(no excerpts retrieved)",
    )
    result: SkillEvaluation = _structured_invoke(prompt, SkillEvaluation)

    # Deterministic cross-check using regex matching over the raw resume.
    matcher = SkillMatcher(state.get("resume_text", ""))
    for skill in state["required_skills"]:
        if matcher.has_skill(skill) and skill.lower() not in [m.lower() for m in result.matched_skills]:
            result.matched_skills.append(skill)
        if not matcher.has_skill(skill) and skill.lower() in [m.lower() for m in result.matched_skills]:
            pass  # trust LLM evidence from excerpts
    required_count = max(len(state["required_skills"]), 1)
    matched_count = len([s for s in state["required_skills"] if matcher.has_skill(s)])
    llm_matched = len(result.matched_skills)
    blended_score = round((llm_matched / required_count) * 60 + (matched_count / required_count) * 40)
    result.skill_score = min(max(blended_score, 0), 100)
    return {"skill_result": result}


def evaluate_experience(state: dict) -> dict:
    heuristic_years = ExperienceEvaluator(state.get("resume_text", "")).estimate_years()
    prompt = EXPERIENCE_PROMPT.format(
        job_title=state["job_title"],
        minimum_experience=state["minimum_experience"],
        resume_context=state["resume_context"] or "(no excerpts retrieved)",
    )
    result: ExperienceEvaluation = _structured_invoke(prompt, ExperienceEvaluation)
    if heuristic_years is not None and heuristic_years > result.experience_years:
        result.experience_years = float(heuristic_years)
    if heuristic_years is not None:
        ratio = heuristic_years / max(state["minimum_experience"], 1)
        heuristic_score = 100 if ratio >= 1.25 else (85 if ratio >= 1.0 else int(min(90, ratio * 80)))
        result.experience_score = max(result.experience_score, min(heuristic_score, 100))
    return {"experience_result": result}


def evaluate_semantic_match(state: dict) -> dict:
    prompt = SEMANTIC_PROMPT.format(
        job_title=state["job_title"],
        job_description=truncate_text(state["job_description"], 3000),
        resume_context=state["resume_context"] or "(no excerpts retrieved)",
    )
    result: SemanticEvaluation = _structured_invoke(prompt, SemanticEvaluation)
    return {"semantic_result": result}


def evaluate_ats_quality(state: dict) -> dict:
    prompt = ATS_QUALITY_PROMPT.format(
        resume_context=truncate_text(state.get("resume_text", "") or state["resume_context"], MAX_CONTEXT_CHARS),
    )
    result: ATSEvaluation = _structured_invoke(prompt, ATSEvaluation)
    return {"ats_result": result}


def calculate_final_score_node(state: dict) -> dict:
    final = calculate_final_score(
        skill_score=state["skill_result"].skill_score,
        experience_score=state["experience_result"].experience_score,
        semantic_score=state["semantic_result"].semantic_match_score,
        ats_score=state["ats_result"].ats_score,
    )
    strengths = list(state["ats_result"].strengths)
    weaknesses = list(state["ats_result"].weaknesses)
    if state["skill_result"].missing_skills:
        weaknesses.append(f"Missing skills: {', '.join(state['skill_result'].missing_skills[:5])}")
    if state["experience_result"].experience_score < 60:
        weaknesses.append("Experience below the role requirement")
    if not any("skills" in s.lower() for s in strengths) and state["skill_result"].matched_skills:
        strengths.insert(0, f"Matched skills: {', '.join(state['skill_result'].matched_skills[:6])}")
    return {
        "final_scores": final,
        "strengths": strengths[:8],
        "weaknesses": weaknesses[:8],
    }


def generate_candidate_summary(state: dict) -> dict:
    skill = state["skill_result"]
    exp = state["experience_result"]
    sem = state["semantic_result"]
    ats = state["ats_result"]
    prompt = FINAL_SUMMARY_PROMPT.format(
        job_title=state["job_title"],
        skill_score=skill.skill_score,
        matched_skills=", ".join(skill.matched_skills) or "None",
        missing_skills=", ".join(skill.missing_skills) or "None",
        experience_score=exp.experience_score,
        experience_years=exp.experience_years,
        minimum_experience=state["minimum_experience"],
        semantic_score=sem.semantic_match_score,
        ats_score=ats.ats_score,
        strengths="; ".join(state.get("strengths", [])) or "None noted",
        weaknesses="; ".join(state.get("weaknesses", [])) or "None noted",
    )
    result: FinalEvaluation = _structured_invoke(prompt, FinalEvaluation)
    result.final_score = state.get("final_scores", result.final_score)
    return {"result": result}


def make_shortlisting_decision(state: dict) -> dict:
    """Applies configurable thresholds to set a recommendation-consistent status label."""
    from app.core.config import settings

    from app.ai.evaluation.final_scorer import decide_status

    result = state.get("result")
    if result is None:
        return {}
    status_label = decide_status(
        result.final_score,
        shortlist_threshold=settings.shortlist_threshold,
        review_threshold=settings.review_threshold,
    )
    return {"shortlist_status": status_label}


def save_results(state: dict) -> dict:
    """Persistence happens in the Celery task after the graph completes;
    this node normalizes the final output."""
    return {"saved": True}


def _structured_invoke(prompt_text: str, schema):
    llm = _llm()
    structured_llm = llm.with_structured_output(schema)
    return structured_llm.invoke(prompt_text)
