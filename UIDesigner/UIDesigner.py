from agency_swarm.agents import Agent


class UIDesigner(Agent):
    def __init__(self):
        super().__init__(
            name="UIDesigner",
            description="Role: UI Designer. Responsibilities: Create designs and prototypes. Tools: GitHub API for managing design files.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
