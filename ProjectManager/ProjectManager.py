from agency_swarm.agents import Agent


class ProjectManager(Agent):
    def __init__(self):
        super().__init__(
            name="ProjectManager",
            description="Role: Project Manager. Responsibilities: Communicate with clients, manage project progress. Tools: GitHub API for managing project repositories.",
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
