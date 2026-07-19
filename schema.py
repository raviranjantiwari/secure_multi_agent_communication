import operator
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field

class AgentMessage(BaseModel):
    sender: str = Field(..., description="Cryptographic identity of the sending agent.")
    recipient: str = Field(..., description="Intended target agent identity.")
    content: str = Field(..., description="The raw message payload.")
    jwt_token: str = Field(..., description="Scoped authorization token for verification.")

class AgentSystemState(BaseModel):
    # Using Annotated list with operator.add ensuring updates append to history
    message_history: Annotated[List[AgentMessage], operator.add] = Field(default_factory=list)
    untrusted_payload: Optional[str] = None
    is_compromised: bool = False
    orchestrator_decision: str = "PROCEED"
    loop_count: int = 0  # Capped strictly at 10 hops to eliminate cascade collapse
    quarantine_logs: Annotated[List[str], operator.add] = Field(default_factory=list)
