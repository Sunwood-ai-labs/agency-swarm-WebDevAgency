from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define the GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitHubBranchManager(BaseTool):
    """
    A tool to manage GitHub branches, allowing creation, listing, deletion,
    and management of branches, as well as setting branch protection rules.
    """

    action: str = Field(
        ..., description="The action to perform: 'create', 'list', 'delete', 'set_protection'."
    )
    repo_name: str = Field(
        ..., description="The name of the repository to manage."
    )
    repo_owner: str = Field(
        ..., description="The owner of the repository."
    )
    branch_name: str = Field(
        default=None, description="The name of the branch to manage."
    )
    branch_data: dict = Field(
        default=None, description="The data required for branch actions, such as branch details or protection rules."
    )

    def run(self):
        """
        Executes the specified action on GitHub branches using the GitHub API.
        """
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            if self.action == "create":
                return self.create_branch(headers)
            elif self.action == "list":
                return self.list_branches(headers)
            elif self.action == "delete":
                return self.delete_branch(headers)
            elif self.action == "set_protection":
                return self.set_branch_protection(headers)
            else:
                return "Invalid action specified."
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def create_branch(self, headers):
        # To create a branch, we need to specify the branch name and the SHA of the commit to base it on
        base_branch = self.branch_data.get("base_branch")
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{base_branch}",
            headers=headers
        )
        if response.status_code == 200:
            sha = response.json()["object"]["sha"]
            create_response = requests.post(
                f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/git/refs",
                headers=headers,
                json={"ref": f"refs/heads/{self.branch_name}", "sha": sha}
            )
            if create_response.status_code == 201:
                return f"Branch '{self.branch_name}' created successfully."
            else:
                return f"Failed to create branch: {create_response.json()}"
        else:
            return f"Failed to retrieve base branch: {response.json()}"

    def list_branches(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/branches",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to list branches: {response.json()}"

    def delete_branch(self, headers):
        response = requests.delete(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{self.branch_name}",
            headers=headers
        )
        if response.status_code == 204:
            return f"Branch '{self.branch_name}' deleted successfully."
        else:
            return f"Failed to delete branch: {response.json()}"

    def set_branch_protection(self, headers):
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/branches/{self.branch_name}/protection",
            headers=headers,
            json=self.branch_data
        )
        if response.status_code == 200:
            return f"Branch protection rules set successfully for '{self.branch_name}'."
        else:
            return f"Failed to set branch protection: {response.json()}"