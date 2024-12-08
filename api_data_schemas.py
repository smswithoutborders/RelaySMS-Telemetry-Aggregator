"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

from typing import Literal
from pydantic import BaseModel, Field
from fastapi import Query


class SummaryDetails(BaseModel):
    """Details of the summary metrics."""

    total_signup_users: int
    total_retained_users: int


class SummaryParams(BaseModel):
    """Parameters for filtering and grouping summary metrics."""

    start_date: str = Field(description="Start date in 'YYYY-MM-DD' format.")
    end_date: str = Field(description="End date in 'YYYY-MM-DD' format.")
    country_code: str = Field(
        default=None, description="2-character ISO region code.", max_length=2
    )


class SummaryResponse(BaseModel):
    """Response model containing summary metrics."""

    summary: SummaryDetails


class SignupDetails(BaseModel):
    """Details of the signup metrics."""

    total_signup_users: int
    total_retained_users: int


class SignupParams(BaseModel):
    """Parameters for filtering and grouping signup metrics."""

    start_date: str = Field(description="Start date in 'YYYY-MM-DD' format.")
    end_date: str = Field(description="End date in 'YYYY-MM-DD' format.")
    country_code: str = Field(description="2-character ISO region code.", max_length=2)
    granularity: Literal["day", "month"] = Field(
        default="day", description="Granularity of data (day or month)."
    )
    group_by: Literal["country", "date"] = Field(
        default="date",
        description="Criteria to group results (e.g., 'country', 'date').",
    )
    top: int = Field(
        default=None,
        description="Maximum number of results to return. "
        "(cannot be used with 'page' or 'page_size')",
    )
    page: int = Query(default=1, ge=1, description="Page number for paginated results.")
    page_size: int = Query(
        default=10, ge=10, le=100, description="Number of records per page."
    )


class SignupResponse(BaseModel):
    """Response model containing signup metrics."""

    signup: SignupDetails


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
