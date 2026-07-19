from langgraph.graph import StateGraph, START, END
from schema import AgentSystemState
from nodes import (
    input_guardrail_node, 
    sandboxed_scraper_node, 
    overseer_validator_node, 
    quarantine_node, 
    execution_node
)

def router_decision_engine(state: AgentSystemState) -> str:
    """Routing Controller Engine checking security state metrics."""
    # Direct access checks for standard dictionary structures fed by LangGraph engine
    is_compromised = state.get("is_compromised", False)
    decision = state.get("orchestrator_decision", "PROCEED")
    
    if is_compromised or decision in ["ISOLATE_AND_ABORT", "TERMINATE_ATTACK", "TERMINATE_AUTH_FAILURE"]:
        return "quarantine"
    if decision == "PROCEED_TO_EXECUTION":
        return "execute_mutation"
    return "continue"

def build_secure_workflow() -> StateGraph:
    workflow = StateGraph(AgentSystemState)
    
    # Register Nodes
    workflow.add_node("guardrail", input_guardrail_node)
    workflow.add_node("scraper", sandboxed_scraper_node)
    workflow.add_node("overseer", overseer_validator_node)
    workflow.add_node("quarantine", quarantine_node)
    workflow.add_node("execution", execution_node)
    
    # Establish Secure Structural Flow Topology
    workflow.add_edge(START, "guardrail")
    
    workflow.add_conditional_edges(
        "guardrail",
        router_decision_engine,
        {
            "quarantine": "quarantine",
            "continue": "scraper"
        }
    )
    
    workflow.add_edge("scraper", "overseer")
    
    workflow.add_conditional_edges(
        "overseer",
        router_decision_engine,
        {
            "quarantine": "quarantine",
            "execute_mutation": "execution"
        }
    )
    
    workflow.add_edge("quarantine", END)
    workflow.add_edge("execution", END)
    
    return workflow.compile()

secure_agentic_app = build_secure_workflow()
