"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

from typing import Literal, List, Union
from pydantic import BaseModel, Field
from fastapi import Query


class SummaryDetails(BaseModel):
    """Details of the summary metrics."""

    total_signup_users: int
    total_retained_users: int
    total_retained_users_with_tokens: int
    total_signup_countries: int
    total_signups_from_bridges: int
    total_retained_countries: int
    total_publications: int
    total_published_publications: int
    total_failed_publications: int
    signup_countries: list
    retained_countries: list
    

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


class MetricsParams(BaseModel):
    """Parameters for filtering and grouping metrics."""

    start_date: str = Field(description="Start date in 'YYYY-MM-DD' format.")
    end_date: str = Field(description="End date in 'YYYY-MM-DD' format.")
    country_code: str = Field(
        default=None, description="2-character ISO region code.", max_length=2
    )
    granularity: Literal["day", "month"] = Field(
        default="day", description="Granularity of data."
    )
    group_by: Literal["country", "date"] = Field(
        default="date", description="Criteria to group results."
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


class PaginationDetails(BaseModel):
    """Pagination details for paginated responses."""

    page: int
    page_size: int
    total_pages: int
    total_records: int


class CountrySignupData(BaseModel):
    """Signup data grouped by country."""

    country_code: str
    signup_users: int


class TimeframeSignupData(BaseModel):
    """Signup data grouped by timeframe."""

    timeframe: str
    signup_users: int


class SignupDetails(BaseModel):
    """Details of the signup metrics."""

    total_signup_users: int
    total_countries: int
    total_signups_from_bridges: int
    countries: list
    pagination: PaginationDetails
    data: List[Union[CountrySignupData, TimeframeSignupData]]


class SignupResponse(BaseModel):
    """Response model containing signup metrics."""

    signup: SignupDetails


class CountryRetainedData(BaseModel):
    """Retained data grouped by country."""

    country_code: str
    retained_users: int


class TimeframeRetainedData(BaseModel):
    """Retained data grouped by timeframe."""

    timeframe: str
    retained_users: int


class RetainedDetails(BaseModel):
    """Details of the retained metrics."""

    total_retained_users: int
    total_retained_users_with_tokens: int
    total_countries: int
    countries: list
    pagination: PaginationDetails
    data: List[Union[CountryRetainedData, TimeframeRetainedData]]


class RetainedResponse(BaseModel):
    """Response model containing retained metrics."""

    retained: RetainedDetails
    
class PublicationsParams(BaseModel):
    """Parameters for filtering and grouping publication metrics."""

    start_date: str = Field(description="Start date in 'YYYY-MM-DD' format.")
    end_date: str = Field(description="End date in 'YYYY-MM-DD' format.")
    country_code: str = Field(
        default=None, description="2-character ISO region code.", max_length=2
    )
    platform_name: str = Field(
        default=None, description="Filter by platform name (e.g., 'Twitter')."
    )
    source: str = Field(
        default=None, description="Filter by source of publication."
    )
    status: Literal["published", "failed"] = Field(
        default=None, description="Filter by publication status."
    )
    gateway_client: str = Field(
        default=None, description="Filter by the gateway client."
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

class PublicationsDetails(BaseModel):
    """Details of the summary metrics."""

    country_code: str
    platform_name: str
    source: str
    status: str
    gateway_client: str
    date_time: str
    id: int
    
class PublicationsSummary(BaseModel):
    """Summary of total publications."""

    total_publications: int
    total_published: int
    total_failed: int
    data: List[PublicationsDetails]  
    
class PublicationsResponse(BaseModel):
    """Response model containing publications metrics."""

    publications: PublicationsSummary
    
class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
