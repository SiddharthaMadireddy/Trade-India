#!/usr/bin/env python3
"""Entry point for the India index options module."""

from .india import (
    discover_nifty_contracts,
    discover_banknifty_contracts,
    discover_sensex_contracts,
    validate_nifty_contract,
    validate_banknifty_contract,
    validate_sensex_contract,
    get_valid_contracts,
    identify_contract,
    get_contract_info,
    get_india_timezone,
    is_indian_market_open,
    get_market_session,
    get_valid_strike_range,
)

__all__ = [
    "discover_nifty_contracts",
    "discover_banknifty_contracts",
    "discover_sensex_contracts",
    "validate_nifty_contract",
    "validate_banknifty_contract",
    "validate_sensex_contract",
    "get_valid_contracts",
    "identify_contract",
    "get_contract_info",
    "get_india_timezone",
    "is_indian_market_open",
    "get_market_session",
    "get_valid_strike_range",
]