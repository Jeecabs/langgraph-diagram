from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    raw_data: Optional[dict]
    analysis: Optional[dict]
    recommendations: Optional[List[dict]]
    approval_status: Optional[bool]
    deployed_workflows: Optional[List[str]]
    user_feedback: Optional[dict]
    workflows_rendered: Optional[bool]  # Updated key
    cycle_count: int
    review_cycles: int