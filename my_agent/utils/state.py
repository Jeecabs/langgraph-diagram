# state.py 
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    raw_data: Optional[dict]
    analysis: Optional[dict]
    recommendations: Optional[List[dict]]
    approval_status: Optional[bool]  # Renamed from "approval"
    deployed_workflows: Optional[List[str]]
    user_feedback: Optional[dict]  # Renamed from "feedback"
    ui_displayed: Optional[bool]
    cycle_count: int
    review_cycles: int