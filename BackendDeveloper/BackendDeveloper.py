from agency_swarm.agents import Agent


class BackendDeveloper(Agent):
    def __init__(self):
        super().__init__(
            name="BackendDeveloper",
            description="Role: Backend Developer. Responsibilities: Implement server-side functionalities. Tools: GitHub API for code pull requests and branch management.",
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
