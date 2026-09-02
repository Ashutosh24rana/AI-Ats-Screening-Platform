from langgraph.graph import END, START


def build_edges(graph):
    """Linear evaluation pipeline with a single error short-circuit."""
    graph.add_edge(START, "parse_resume_information")
    graph.add_conditional_edges(
        "parse_resume_information",
        lambda state: "error" if state.get("error") else "continue",
        {"error": "handle_error", "continue": "retrieve_relevant_chunks"},
    )
    graph.add_edge("retrieve_relevant_chunks", "evaluate_skill_match")
    graph.add_edge("evaluate_skill_match", "evaluate_experience")
    graph.add_edge("evaluate_experience", "evaluate_semantic_match")
    graph.add_edge("evaluate_semantic_match", "evaluate_ats_quality")
    graph.add_edge("evaluate_ats_quality", "calculate_final_score")
    graph.add_edge("calculate_final_score", "generate_candidate_summary")
    graph.add_edge("generate_candidate_summary", "make_shortlisting_decision")
    graph.add_edge("make_shortlisting_decision", "save_results")
    graph.add_edge("save_results", END)
    graph.add_edge("handle_error", END)
