# nodes.py

from typing import Dict, Any
import random
from datetime import datetime
import time  # For demo


# Mock data generators
def mock_crm_data():
    return {"sales": random.randint(10, 50), "orders": random.randint(5, 20)}


def mock_desktop_activity():
    tasks = ["report_generation", "data_entry", "email_response"]
    return {"active_app": random.choice(tasks), "duration_min": random.randint(5, 120)}


def mock_customer_service_data():
    return {"tickets": random.randint(1, 10), "response_time": random.uniform(0.5, 2.0)}


def data_ingestion_node(state: Dict[str, Any], config: Dict[str, Any]):
    new_data = {
        "timestamp": datetime.now().isoformat(),
        "crm": mock_crm_data(),
        "desktop": mock_desktop_activity(),
        "customer_service": mock_customer_service_data(),
        "feedback": state.get("user_feedback", {}),  # Updated key
    }
    return {"raw_data": new_data}


def workflow_analysis_node(state: Dict[str, Any], config: Dict[str, Any]):
    """Analyze data patterns to find automation candidates"""
    data = state["raw_data"]

    # Simple pattern detection for demo
    patterns = []
    if data["desktop"]["active_app"] == "report_generation":
        patterns.append("Daily report generation")
    if data["crm"]["orders"] > 15:
        patterns.append("High order volume processing")
    time.sleep(2)
    return {"analysis": {"patterns": patterns, "timestamp": data["timestamp"]}}


def recommendation_node(state: Dict[str, Any], config: Dict[str, Any]):
    """Generate automation recommendations based on analysis"""
    patterns = state["analysis"]["patterns"]
    recs = []

    for pattern in patterns:
        if "report" in pattern:
            recs.append(
                {
                    "name": "Auto-report Generator",
                    "impact": "Saves 2h daily",
                    "complexity": "Low",
                }
            )
        if "order" in pattern:
            recs.append(
                {
                    "name": "Order Processing Bot",
                    "impact": "Reduces errors by 40%",
                    "complexity": "Medium",
                }
            )
    time.sleep(2)
    return {"recommendations": recs}


def dashboard_ui_node(state: Dict[str, Any], config: Dict[str, Any]):
    """Present recommendations to users (mock)"""
    # In real implementation, this would trigger UI display
    return {"ui_displayed": True}


def workflow_presentation_node(state: Dict[str, Any], config: Dict[str, Any]):  # Renamed
    """Present workflow blueprints to users"""
    return {"workflows_rendered": True}  # Updated key

def deployment_node(state: Dict[str, Any], config: Dict[str, Any]):
    return {
        "deployed_at": datetime.now().isoformat(),
        "deployed_workflows": [rec["name"] for rec in state["recommendations"]],  # Updated key
    }

def feedback_node(state: Dict[str, Any], config: Dict[str, Any]):
    cycle_count = state.get("cycle_count", 0) + 1
    return {
        "user_feedback": {
            "satisfaction": random.randint(3, 5),
            "issues_reported": random.randint(0, 2)
        },
        "cycle_count": cycle_count
    }

def human_review_node(state: Dict[str, Any], config: Dict[str, Any]):
    review_cycles = state.get("review_cycles", 0)
    if not config.get("auto_approve"):
        review_cycles += 1
    
    approval = random.random() < 0.8 if not config.get("auto_approve") else True
    time.sleep(1)
    return {
        "approval_status": approval,
        "review_cycles": review_cycles
    }