"""
Google Cloud Secret Manager integration for Q360.
Safely load secrets from Secret Manager instead of environment variables.
"""

import os
from functools import lru_cache
from google.cloud import secretmanager


class SecretManager:
    """Load secrets from Google Cloud Secret Manager."""

    def __init__(self, project_id: str):
        """Initialize Secret Manager client.

        Args:
            project_id: Google Cloud project ID
        """
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    @lru_cache(maxsize=10)
    def get_secret(self, secret_name: str, version: str = "latest") -> str:
        """Get secret from Secret Manager.

        Args:
            secret_name: Name of the secret (e.g., 'jira-api-token')
            version: Version of the secret (default: 'latest')

        Returns:
            Secret value as string
        """
        try:
            name = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            # Fallback to environment variable
            env_key = secret_name.upper().replace("-", "_")
            return os.getenv(env_key, "")


# Initialize global secret manager
_secret_manager = None


def init_secrets(project_id: str) -> SecretManager:
    """Initialize the global secret manager.

    Args:
        project_id: Google Cloud project ID

    Returns:
        SecretManager instance
    """
    global _secret_manager
    _secret_manager = SecretManager(project_id)
    return _secret_manager


def get_secret(secret_name: str) -> str:
    """Get a secret from the global secret manager.

    Args:
        secret_name: Name of the secret

    Returns:
        Secret value
    """
    if _secret_manager is None:
        raise RuntimeError("Secret manager not initialized. Call init_secrets() first.")
    return _secret_manager.get_secret(secret_name)


def get_jira_credentials() -> tuple:
    """Get Jira credentials from Secret Manager.

    Returns:
        Tuple of (url, email, api_token)
    """
    return (
        get_secret("jira-url"),
        get_secret("jira-email"),
        get_secret("jira-api-token"),
    )


def get_google_api_key() -> str:
    """Get Google API key from Secret Manager.

    Returns:
        Google API key
    """
    return get_secret("google-api-key")
