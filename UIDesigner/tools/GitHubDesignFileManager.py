from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os
import base64

# Define the GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitHubDesignFileManager(BaseTool):
    """
    A tool to manage design files in a GitHub repository, allowing upload, update, delete,
    and listing of files, as well as managing file versions and access permissions.
    """

    action: str = Field(
        ..., description="The action to perform: 'upload', 'update', 'delete', 'list'."
    )
    repo_name: str = Field(
        ..., description="The name of the repository to manage."
    )
    repo_owner: str = Field(
        ..., description="The owner of the repository."
    )
    file_path: str = Field(
        default=None, description="The path of the file to manage in the repository."
    )
    file_content: str = Field(
        default=None, description="The content of the file to upload or update, encoded in base64."
    )
    commit_message: str = Field(
        default="File operation via GitHubDesignFileManager", description="The commit message for the file operation."
    )
    branch: str = Field(
        default="main", description="The branch to perform the file operation on."
    )

    def run(self):
        """
        Executes the specified action on design files in a GitHub repository using the GitHub API.
        """
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            if self.action == "upload":
                return self.upload_file(headers)
            elif self.action == "update":
                return self.update_file(headers)
            elif self.action == "delete":
                return self.delete_file(headers)
            elif self.action == "list":
                return self.list_files(headers)
            else:
                return "Invalid action specified."
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def upload_file(self, headers):
        # Check if the file already exists
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            params={"ref": self.branch}
        )
        if response.status_code == 200:
            return "File already exists. Use 'update' action to modify it."
        elif response.status_code != 404:
            return f"Failed to check file existence: {response.json()}"

        # Upload the file
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            json={
                "message": self.commit_message,
                "content": self.file_content,
                "branch": self.branch
            }
        )
        if response.status_code == 201:
            return f"File '{self.file_path}' uploaded successfully."
        else:
            return f"Failed to upload file: {response.json()}"

    def update_file(self, headers):
        # Get the current file SHA
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            params={"ref": self.branch}
        )
        if response.status_code != 200:
            return f"Failed to retrieve file for update: {response.json()}"

        file_sha = response.json()["sha"]

        # Update the file
        response = requests.put(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            json={
                "message": self.commit_message,
                "content": self.file_content,
                "sha": file_sha,
                "branch": self.branch
            }
        )
        if response.status_code == 200:
            return f"File '{self.file_path}' updated successfully."
        else:
            return f"Failed to update file: {response.json()}"

    def delete_file(self, headers):
        # Get the current file SHA
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            params={"ref": self.branch}
        )
        if response.status_code != 200:
            return f"Failed to retrieve file for deletion: {response.json()}"

        file_sha = response.json()["sha"]

        # Delete the file
        response = requests.delete(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}",
            headers=headers,
            json={
                "message": self.commit_message,
                "sha": file_sha,
                "branch": self.branch
            }
        )
        if response.status_code == 200:
            return f"File '{self.file_path}' deleted successfully."
        else:
            return f"Failed to delete file: {response.json()}"

    def list_files(self, headers):
        response = requests.get(
            f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/contents",
            headers=headers,
            params={"ref": self.branch}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to list files: {response.json()}"