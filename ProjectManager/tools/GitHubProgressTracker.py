from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define the GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitHubProgressTracker(BaseTool):
    """
    A tool to track the progress of projects on GitHub by managing issues, pull requests, and commits.
    It provides functionalities to list, create, update, and close issues, as well as to list and merge pull requests.
    """

    action: str = Field(
        ..., description="The action to perform: 'list_issues', 'create_issue', 'update_issue', 'close_issue', 'list_pull_requests', 'merge_pull_request'."
    )
    repo_name: str = Field(
        ..., description="The name of the repository to manage."
    )
    repo_owner: str = Field(
        ..., description="The owner of the repository."
    )
    issue_data: dict = Field(
        default=None, description="The data required for issue actions, such as issue details."
    )
    pull_request_number: int = Field(
        default=None, description="The number of the pull request to manage."
    )

    def run(self):
        """
        Executes the specified action on GitHub issues or pull requests using the GitHub API.
        """
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            if self.action == "list_issues":
                return self.list_issues(headers)
            elif self.action == "create_issue":
                return self.create_issue(headers)
            elif self.action == "update_issue":
                return self.update_issue(headers)
            elif self.action == "close_issue":
                return self.close_issue(headers)
            elif self.action == "list_pull_requests":
                return self.list_pull_requests(headers)
            elif self.action == "merge_pull_request":
                return self.merge_pull_request(headers)
            else:
                return "Invalid action specified."
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def list_issues(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/issues",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to list issues: {response.json()}"

    def create_issue(self, headers):
        response = requests.post(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/issues",
            headers=headers,
            json=self.issue_data
        )
        if response.status_code == 201:
            return f"Issue created successfully: {response.json()}"
        else:
            return f"Failed to create issue: {response.json()}"

    def update_issue(self, headers):
        issue_number = self.issue_data.get("number")
        response = requests.patch(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}",
            headers=headers,
            json=self.issue_data
        )
        if response.status_code == 200:
            return f"Issue updated successfully: {response.json()}"
        else:
            return f"Failed to update issue: {response.json()}"

    def close_issue(self, headers):
        issue_number = self.issue_data.get("number")
        response = requests.patch(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}",
            headers=headers,
            json={"state": "closed"}
        )
        if response.status_code == 200:
            return f"Issue closed successfully: {response.json()}"
        else:
            return f"Failed to close issue: {response.json()}"

    def list_pull_requests(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to list pull requests: {response.json()}"

    def merge_pull_request(self, headers):
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls/{self.pull_request_number}/merge",
            headers=headers
        )
        if response.status_code == 200:
            return f"Pull request merged successfully: {response.json()}"
        else:
            return f"Failed to merge pull request: {response.json()}"