from langchain_core.prompts import PromptTemplate

SKILL_MATCH_PROMPT = PromptTemplate.from_template(
    """You are an expert technical recruiter evaluating a candidate's resume against a job.

JOB TITLE: {job_title}
REQUIRED SKILLS: {required_skills}
PREFERRED SKILLS: {preferred_skills}

RELEVANT RESUME EXCERPTS:
{resume_context}

TASK:
1. Determine which of the REQUIRED skills the candidate demonstrably has (based only on the excerpts).
2. Determine which REQUIRED skills are missing or not evidenced.
3. Score the skill match from 0 to 100, where 100 means every required skill is strongly evidenced.

Be strict: a skill counts as matched only if the excerpts show real experience with it.

"""
)

EXPERIENCE_PROMPT = PromptTemplate.from_template(
    """You are an expert technical recruiter evaluating a candidate's experience level.

JOB TITLE: {job_title}
MINIMUM YEARS OF EXPERIENCE REQUIRED: {minimum_experience}

RELEVANT RESUME EXCERPTS:
{resume_context}

TASK:
1. Estimate the candidate's total years of relevant professional experience from the excerpts.
2. Compare it with the requirement.
3. Score the experience match from 0 to 100:
   - 100: far exceeds the requirement
   - 75-99: meets the requirement fully
   - 40-74: close but slightly below
   - below 40: significantly below

"""
)

SEMANTIC_PROMPT = PromptTemplate.from_template(
    """You are assessing how well a candidate's overall profile fits a job beyond exact keyword matching.

JOB TITLE: {job_title}
JOB DESCRIPTION: {job_description}

RELEVANT RESUME EXCERPTS:
{resume_context}

TASK:
Score the semantic fit from 0 to 100 considering domain alignment, seniority, industry context,
and transferable experience — even when keywords do not match exactly.

"""
)

ATS_QUALITY_PROMPT = PromptTemplate.from_template(
    """You are an ATS (Applicant Tracking System) quality analyst reviewing a resume.

RESUME EXCERPTS:
{resume_context}

TASK:
Score the resume/ATS quality from 0 to 100 based on:
- Clear structure and readable sections
- Quantified achievements and impact
- Relevant keywords present
- Absence of formatting problems, gaps, or red flags

Also list the main strengths of this resume.

"""
)

FINAL_SUMMARY_PROMPT = PromptTemplate.from_template(
    """You are writing the final hiring recommendation for a recruiter.

JOB TITLE: {job_title}

EVALUATION RESULTS:
- Skill match score: {skill_score}/100
- Matched skills: {matched_skills}
- Missing skills: {missing_skills}
- Experience score: {experience_score}/100 ({experience_years} years est., required {minimum_experience})
- Semantic fit score: {semantic_score}/100
- ATS/resume quality score: {ats_score}/100
- Strengths: {strengths}
- Weaknesses: {weaknesses}

TASK:
1. Produce a concise professional summary (3-5 sentences) explaining the overall fit.
2. Give a short recommendation label, one of: "Strong Match", "Good Match", "Moderate Match", "Weak Match".

"""
)

RETRIEVAL_QUERY_PROMPT = PromptTemplate.from_template(
    """Generate ONE focused retrieval query to find resume evidence for this job.
Mention the key required skills and seniority. Return only the query text.

JOB TITLE: {job_title}
REQUIRED SKILLS: {required_skills}
JOB DESCRIPTION (first part): {job_description}
"""
)


ALL_PROMPTS = {
    "skill": SKILL_MATCH_PROMPT,
    "experience": EXPERIENCE_PROMPT,
    "semantic": SEMANTIC_PROMPT,
    "ats": ATS_QUALITY_PROMPT,
    "final": FINAL_SUMMARY_PROMPT,
    "retrieval_query": RETRIEVAL_QUERY_PROMPT,
}
