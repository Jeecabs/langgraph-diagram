import time
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState
from my_agent.utils.nodes import (
    data_ingestion_node,
    workflow_analysis_node,
    recommendation_node,
    workflow_presentation_node,
    human_review_node,
    deployment_node,
    feedback_node,
)


class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai"]
    auto_approve: bool
    max_cycles: int


workflow = StateGraph(AgentState, config_schema=GraphConfig)

workflow.add_node("data_ingestion", data_ingestion_node)
workflow.add_node("workflow_analysis", workflow_analysis_node)
workflow.add_node("automation_recommendation", recommendation_node)
workflow.add_node("workflow_presentation", workflow_presentation_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("deploy_workflows", deployment_node)
workflow.add_node("collect_feedback", feedback_node)

workflow.set_entry_point("data_ingestion")

workflow.add_edge("data_ingestion", "workflow_analysis")
workflow.add_edge("workflow_analysis", "automation_recommendation")
workflow.add_edge("automation_recommendation", "workflow_presentation")
workflow.add_edge("workflow_presentation", "human_review")


def route_human_decision(state):
    if state.get("approval_status"):
        return "approved"
    if state.get("review_cycles", 0) >= 3:
        return "max_rejected"
    return "rejected"


workflow.add_conditional_edges(
    "human_review",
    route_human_decision,
    {
        "approved": "deploy_workflows",
        "rejected": "workflow_analysis",
        "max_rejected": END,
    },
)


def should_continue(state, config):
    if state.get("cycle_count", 0) < 3:
        time.sleep(5)  # Reduced from 10s for better demo pacing
        return "continue"
    return "end"


workflow.add_conditional_edges(
    "collect_feedback", should_continue, {"continue": "data_ingestion", "end": END}
)

workflow.add_edge("deploy_workflows", "collect_feedback")

graph = workflow.compile()