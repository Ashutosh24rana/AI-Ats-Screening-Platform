from langgraph.graph import StateGraph

from app.ai.langgraph import edges, nodes
from app.ai.langgraph.state import EvaluationState

ERROR_NODE = "handle_error"


def build_evaluation_workflow():
    """LangGraph workflow for complete candidate evaluation:

    START -> parse_resume_information -> retrieve_relevant_chunks
          -> evaluate_skill_match -> evaluate_experience
          -> evaluate_semantic_match -> evaluate_ats_quality
          -> calculate_final_score -> generate_candidate_summary
          -> make_shortlisting_decision -> save_results -> END
    """
    graph = StateGraph(EvaluationState)

    def handle_error(state):
        return state  # error already recorded in state

    graph.add_node("parse_resume_information", nodes.parse_resume_information)
    graph.add_node("retrieve_relevant_chunks", nodes.retrieve_relevant_chunks)
    graph.add_node("evaluate_skill_match", nodes.evaluate_skill_match)
    graph.add_node("evaluate_experience", nodes.evaluate_experience)
    graph.add_node("evaluate_semantic_match", nodes.evaluate_semantic_match)
    graph.add_node("evaluate_ats_quality", nodes.evaluate_ats_quality)
    graph.add_node("calculate_final_score", nodes.calculate_final_score_node)
    graph.add_node("generate_candidate_summary", nodes.generate_candidate_summary)
    graph.add_node("make_shortlisting_decision", nodes.make_shortlisting_decision)
    graph.add_node("save_results", nodes.save_results)
    graph.add_node(ERROR_NODE, handle_error)

    edges.build_edges(graph)
    return graph.compile()
