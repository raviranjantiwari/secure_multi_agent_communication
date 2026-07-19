from pipeline import secure_agentic_app
from schema import AgentSystemState, AgentMessage
from security import SecurityProvider

def run_simulation(test_title: str, initial_message_content: str, token: str):
    print(f"\n==========================================")
    print(f" RUNNING: {test_title}")
    print(f"==========================================")
    
    msg = AgentMessage(
        sender="user_gateway",
        recipient="guardrail_agent",
        content=initial_message_content,
        jwt_token=token
    )
    
    initial_state = AgentSystemState(message_history=[msg])
    
    # Invoke state mesh runtime loop
    # Passing the exact Pydantic instance to matching StateGraph configuration
    final_output = secure_agentic_app.invoke(initial_state.dict())
    
    print(f"Is System Compromised : {final_output.get('is_compromised')}")
    print(f"Final Decision Outcome: {final_output.get('orchestrator_decision')}")
    print(f"Telemetry Logs Logged : {final_output.get('quarantine_logs')}")
    print(f"Last Logged Event     : {final_output.get('message_history')[-1]['content']}")

if __name__ == "__main__":
    valid_token = SecurityProvider.mint_mock_token("user_gateway", "guardrail_agent")
    
    # Scenario A: Standard Safe Request
    run_simulation(
        test_title="Clean Transaction Request Profile",
        initial_message_content="Analyze financial distribution trends.",
        token=valid_token
    )

    # Scenario B: Cryptographic Header Compromise
    run_simulation(
        test_title="Lateral Movement Interception (Token Forgery Blocked)",
        initial_message_content="Analyze corporate profile databases.",
        token="REVOKED_OR_EXPIRED_JWT_KEY"
    )

    # Scenario C: Secondary Indirect Prompt Injection Attack Pathway
    run_simulation(
        test_title="Indirect Injection Intercepted By Asymmetric Overseer Node",
        initial_message_content="Process automated ingestion pipelines.",
        token=valid_token
    )
