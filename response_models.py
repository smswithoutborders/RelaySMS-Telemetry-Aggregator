"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

from pydantic import BaseModel
from typing import List, Dict


class Stats(BaseModel):
    country: str
    signup_users: int
    active_users: int


class SummaryData(BaseModel):
    date: str
    stats: List[Stats]


class Overview(BaseModel):
    total_signup_users: int
    total_active_users: int
    total_signup_countries: int
    total_active_countries: int


class SummaryResponse(BaseModel):
    summary: Overview
    data: List[SummaryData]


class ErrorResponse(BaseModel):
    error: str
