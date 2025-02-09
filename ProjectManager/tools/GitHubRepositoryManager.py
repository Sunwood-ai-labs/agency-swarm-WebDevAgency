from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os
import subprocess

# Define the GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitHubRepositoryManager(BaseTool):
    """
    A tool to manage GitHub repositories, allowing creation, updating, deletion,
    and management of repository settings such as access permissions and branch protections.
    """

    action: str = Field(
        ..., description="The action to perform: 'create', 'update', 'delete', 'manage_settings'."
    )
    repo_name: str = Field(
        ..., description="The name of the repository to manage."
    )
    repo_owner: str = Field(
        default="Sunwood-ai-labs", description="The owner of the repository (organization or user)."
    )
    repo_data: dict = Field(
        default=None, description="The data required for the action, such as repository details or settings."
    )

    def run(self):
        """
        Executes the specified action on a GitHub repository using the GitHub API.
        """
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            if self.action == "create":
                return self.create_repository(headers)
            elif self.action == "update":
                return self.update_repository(headers)
            elif self.action == "delete":
                return self.delete_repository(headers)
            elif self.action == "manage_settings":
                return self.manage_repository_settings(headers)
            else:
                return "Invalid action specified."
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def create_repository(self, headers):
        try:
            # ghコマンドを使用してリポジトリを作成
            visibility = "--private" if self.repo_data and self.repo_data.get("private", False) else "--public"
            cmd = f"gh repo create {self.repo_owner}/{self.repo_name} {visibility} --clone"
            
            # サブプロセスでコマンドを実行
            result = subprocess.run(
                cmd.split(),
                check=True,
                capture_output=True,
                text=True
            )
            return f"Repository '{self.repo_name}' created successfully."
        except subprocess.CalledProcessError as e:
            return f"Failed to create repository: {e.stderr}"

    def update_repository(self, headers):
        response = requests.patch(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}",
            headers=headers,
            json=self.repo_data
        )
        if response.status_code == 200:
            return f"Repository '{self.repo_name}' updated successfully."
        else:
            return f"Failed to update repository: {response.json()}"

    def delete_repository(self, headers):
        response = requests.delete(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}",
            headers=headers
        )
        if response.status_code == 204:
            return f"Repository '{self.repo_name}' deleted successfully."
        else:
            return f"Failed to delete repository: {response.json()}"

    def manage_repository_settings(self, headers):
        # Example: Manage branch protection settings
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/branches/{self.repo_data['branch']}/protection",
            headers=headers,
            json=self.repo_data['protection_settings']
        )
        if response.status_code == 200:
            return f"Repository settings for '{self.repo_name}' updated successfully."
        else:
            return f"Failed to update repository settings: {response.json()}"
