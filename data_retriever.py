"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

import requests
from logutils import get_logger
from utils import get_env_var

logger = get_logger(__name__)

VAULT_DOMAIN = get_env_var("RELAYSMS_VAULT_DOMAIN", strict=True)
VAULT_PORT = get_env_var("RELAYSMS_VAULT_PORT", default_value=443)
VAULT_URL = f"{VAULT_DOMAIN}:{VAULT_PORT}"


def get_summary(params: dict):
    """
    Fetch summary metrics from external APIs.

    Args:
        params (dict): Query parameters to pass to the API.

    Returns:
        dict: Combined metrics from the target APIs.

    Raises:
        HTTPError: If any of the external API calls fail.
    """
    retained_metrics_url = f"{VAULT_URL}/v3/metrics/retained"
    signup_metrics_url = f"{VAULT_URL}/v3/metrics/signup"

    try:
        retained_response = requests.get(
            retained_metrics_url, params=params, timeout=30
        )
        signup_response = requests.get(signup_metrics_url, params=params, timeout=30)

        retained_response.raise_for_status()
        signup_response.raise_for_status()

        retained_metrics = retained_response.json()
        signup_metrics = signup_response.json()

        metrics_summary = {
            "total_signup_users": signup_metrics["total_signup_users"],
            "total_retained_users": retained_metrics["total_retained_users"],
        }

        return metrics_summary

    except requests.RequestException as e:
        raise e
