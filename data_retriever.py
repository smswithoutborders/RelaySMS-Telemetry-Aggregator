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
            "total_retained_users_with_tokens": retained_metrics["total_retained_users_with_tokens"],
            "total_signups_from_bridges": signup_metrics["total_signups_from_bridges"],
            "total_signup_countries": signup_metrics["total_countries"],
            "total_retained_countries": retained_metrics["total_countries"],
            "signup_countries": signup_metrics["countries"],
            "retained_countries": retained_metrics["countries"],
        }

        return metrics_summary

    except requests.RequestException as e:
        raise e


def get_signup(params: dict):
    """
    Fetches signup metrics data from the metrics API.

    Args:
        params (dict): Query parameters to include in the API request. Expected keys may include:
            - start_date (str): Start date for the metrics in 'YYYY-MM-DD' format.
            - end_date (str): End date for the metrics in 'YYYY-MM-DD' format.
            - granularity (str, optional): Level of detail, e.g., 'day' or 'month'.
            - group_by (str, optional): Dimension to group the metrics by, e.g., 'country'.
            - top (int, optional): Maximum number of results to return.
            - page (int, optional): Pagination page number.
            - page_size (int, optional): Number of records per page.

    Returns:
        dict: The JSON response from the metrics API containing signup data.
    """
    signup_metrics_url = f"{VAULT_URL}/v3/metrics/signup"

    try:
        signup_response = requests.get(signup_metrics_url, params=params, timeout=30)

        signup_response.raise_for_status()

        return signup_response.json()

    except requests.RequestException as e:
        raise e


def get_retained(params: dict):
    """
    Fetches retained metrics data from the metrics API.

    Args:
        params (dict): Query parameters to include in the API request. Expected keys may include:
            - start_date (str): Start date for the metrics in 'YYYY-MM-DD' format.
            - end_date (str): End date for the metrics in 'YYYY-MM-DD' format.
            - granularity (str, optional): Level of detail, e.g., 'day' or 'month'.
            - group_by (str, optional): Dimension to group the metrics by, e.g., 'country'.
            - top (int, optional): Maximum number of results to return.
            - page (int, optional): Pagination page number.
            - page_size (int, optional): Number of records per page.

    Returns:
        dict: The JSON response from the metrics API containing retained data.
    """
    retained_metrics_url = f"{VAULT_URL}/v3/metrics/retained"

    try:
        retained_response = requests.get(
            retained_metrics_url, params=params, timeout=30
        )

        retained_response.raise_for_status()

        return retained_response.json()

    except requests.RequestException as e:
        raise e
