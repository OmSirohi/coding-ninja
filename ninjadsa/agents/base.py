
from typing import Dict, Any

class Agent:
    name: str = "Agent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Return updates to the shared state.
        raise NotImplementedError
