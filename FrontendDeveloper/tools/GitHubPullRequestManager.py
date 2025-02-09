from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define the GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitHubPullRequestManager(BaseTool):
    """
    A tool to manage GitHub pull requests, allowing creation, listing, updating, merging,
    and reviewing pull request details and comments.
    """

    action: str = Field(
        ..., description="The action to perform: 'create', 'list', 'update', 'merge', 'review'."
    )
    repo_name: str = Field(
        ..., description="The name of the repository to manage."
    )
    repo_owner: str = Field(
        ..., description="The owner of the repository."
    )
    pull_request_data: dict = Field(
        default=None, description="The data required for pull request actions, such as pull request details."
    )
    pull_request_number: int = Field(
        default=None, description="The number of the pull request to manage."
    )

    def run(self):
        """
        Executes the specified action on GitHub pull requests using the GitHub API.
        """
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            if self.action == "create":
                return self.create_pull_request(headers)
            elif self.action == "list":
                return self.list_pull_requests(headers)
            elif self.action == "update":
                return self.update_pull_request(headers)
            elif self.action == "merge":
                return self.merge_pull_request(headers)
            elif self.action == "review":
                return self.review_pull_request(headers)
            else:
                return "Invalid action specified."
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def create_pull_request(self, headers):
        response = requests.post(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls",
            headers=headers,
            json=self.pull_request_data
        )
        if response.status_code == 201:
            return f"Pull request created successfully: {response.json()}"
        else:
            return f"Failed to create pull request: {response.json()}"

    def list_pull_requests(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to list pull requests: {response.json()}"

    def update_pull_request(self, headers):
        response = requests.patch(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls/{self.pull_request_number}",
            headers=headers,
            json=self.pull_request_data
        )
        if response.status_code == 200:
            return f"Pull request updated successfully: {response.json()}"
        else:
            return f"Failed to update pull request: {response.json()}"

    def merge_pull_request(self, headers):
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls/{self.pull_request_number}/merge",
            headers=headers
        )
        if response.status_code == 200:
            return f"Pull request merged successfully: {response.json()}"
        else:
            return f"Failed to merge pull request: {response.json()}"

    def review_pull_request(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls/{self.pull_request_number}",
            headers=headers
        )
        if response.status_code == 200:
            pull_request_details = response.json()
            comments_response = requests.get(
                f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/issues/{self.pull_request_number}/comments",
                headers=headers
            )
            if comments_response.status_code == 200:
                comments = comments_response.json()
                return {
                    "pull_request_details": pull_request_details,
                    "comments": comments
                }
            else:
                return f"Failed to retrieve comments: {comments_response.json()}"
        else:
            return f"Failed to review pull request: {response.json()}"