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
    retained_metrics_url = f"{VAULT_URL}/v3//retained-user-metrics"
    signup_metrics_url = f"{VAULT_URL}/v3//signup-metrics"

    try:
        retained_response = requests.get(
            retained_metrics_url, params=params, timeout=30
        )
        signup_response = requests.get(signup_metrics_url, params=params, timeout=30)

        retained_response.raise_for_status()
        signup_response.raise_for_status()

        retained_metrics = retained_response.json()
        signup_metrics = signup_response.json()

        combined_metrics = {
            "summary": {
                "total_signup_users": signup_metrics["total_signup_count"],
                "total_active_users": retained_metrics["total_retained_user_count"],
                "total_signup_countries": signup_metrics["total_country_count"],
                "total_active_countries": retained_metrics["total_country_count"],
                "data": [],
            }
        }

        all_dates = set(signup_metrics["data"].keys()).union(
            retained_metrics["data"].keys()
        )

        sorted_dates = sorted(all_dates, reverse=True)

        for date in sorted_dates:
            combined_date_data = {"date": date, "stats": []}

            signup_countries = signup_metrics["data"].get(date, {})
            retained_countries = retained_metrics["data"].get(date, {})
            all_countries = set(signup_countries.keys()).union(
                retained_countries.keys()
            )

            for country in all_countries:
                stats = {
                    "country": country,
                    "signup_users": signup_countries.get(country, {}).get(
                        "signup_count", 0
                    ),
                    "active_users": retained_countries.get(country, {}).get(
                        "retained_user_count", 0
                    ),
                }
                combined_date_data["stats"].append(stats)

            combined_metrics["summary"]["data"].append(combined_date_data)

        return combined_metrics

    except requests.RequestException as e:
        raise e
