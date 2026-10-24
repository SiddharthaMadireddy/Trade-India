#!/usr/bin/env python3
"""India index options module for trader-india.

This module provides functionality to work with NIFTY 50, BANKNIFTY, and SENSEX
options contracts. It includes contract discovery, validation, and contract
identification based on exchange, expiry, strike, and option type.

The module is designed to integrate with the existing trader-scanner,
trader-risk, and trader-broker modules.
"""

import datetime
import json
import re
from typing import Dict, List, Optional, Tuple

# Constants for Indian market conventions
NIFTY_EXCHANGE = "NSE"
BANKNIFTY_EXCHANGE = "NSE"
SENSEX_EXCHANGE = "BSE"

# Option types
CE = "CE"
PE = "PE"

# Contract identifier patterns
NIFTY_PATTERN = re.compile(r"^NIFTY[0-9]{2}([CEPE])[0-9]{3,4}$")
BANKNIFTY_PATTERN = re.compile(r"^BANKNIFTY[0-9]{2}([CEPE])[0-9]{3,4}$")
SENSEX_PATTERN = re.compile(r"^SENSEX[0-9]{2}([CEPE])[0-9]{3,4}$")

# Contract validation
def validate_nifty_contract(contract: str) -> bool:
    """Validate NIFTY contract format."""
    return bool(NIFTY_PATTERN.match(contract))

def validate_banknifty_contract(contract: str) -> bool:
    """Validate BANKNIFTY contract format."""
    return bool(BANKNIFTY_PATTERN.match(contract))

def validate_sensex_contract(contract: str) -> bool:
    """Validate SENSEX contract format."""
    return bool(SENSEX_PATTERN.match(contract))

# Contract discovery and validation
def discover_nifty_contracts(expiry: str, strike_interval: int = 10) -> List[str]:
    """
    Discover valid NIFTY options contracts for a given expiry.

    Args:
        expiry: Expiry date in YYYYMMDD format
        strike_interval: Strike interval in points (default 10)

    Returns:
        List of valid NIFTY contract identifiers
    """
    contracts = []
    # NIFTY 50 contracts typically have strikes around 20000-22000
    # We'll generate strikes from 18000 to 24000 in intervals
    for strike in range(18000, 24001, strike_interval):
        ce_contract = f"NIFTY{strike:05d}{CE}"
        pe_contract = f"NIFTY{strike:05d}{PE}"
        if validate_nifty_contract(ce_contract):
            contracts.append(ce_contract)
        if validate_nifty_contract(pe_contract):
            contracts.append(pe_contract)
    return contracts

def discover_banknifty_contracts(expiry: str, strike_interval: int = 5) -> List[str]:
    """
    Discover valid BANKNIFTY options contracts for a given expiry.

    Args:
        expiry: Expiry date in YYYYMMDD format
        strike_interval: Strike interval in points (default 5)

    Returns:
        List of valid BANKNIFTY contract identifiers
    """
    contracts = []
    # BANKNIFTY typically has strikes around 35000-45000
    for strike in range(35000, 46001, strike_interval):
        ce_contract = f"BANKNIFTY{strike:05d}{CE}"
        pe_contract = f"BANKNIFTY{strike:05d}{PE}"
        if validate_banknifty_contract(ce_contract):
            contracts.append(ce_contract)
        if validate_banknifty_contract(pe_contract):
            contracts.append(pe_contract)
    return contracts

def discover_sensex_contracts(expiry: str, strike_interval: int = 500) -> List[str]:
    """
    Discover valid SENSEX options contracts for a given expiry.

    Args:
        expiry: Expiry date in YYYYMMDD format
        strike_interval: Strike interval in points (default 500)

    Returns:
        List of valid SENSEX contract identifiers
    """
    contracts = []
    # SENSEX typically has strikes around 15000-35000
    for strike in range(15000, 36001, strike_interval):
        ce_contract = f"SENSEX{strike:05d}{CE}"
        pe_contract = f"SENSEX{strike:05d}{PE}"
        if validate_sensex_contract(ce_contract):
            contracts.append(ce_contract)
        if validate_sensex_contract(pe_contract):
            contracts.append(pe_contract)
    return contracts

def validate_contract(
    exchange: str, contract: str
) -> Tuple[bool, str]:
    """
    Validate a contract against exchange-specific patterns.

    Args:
        exchange: "NSE" or "BSE"
        contract: Contract identifier

    Returns:
        Tuple of (is_valid, error_message)
    """
    if exchange == "NSE":
        if "NIFTY" in contract and validate_nifty_contract(contract):
            return True, ""
        if "BANKNIFTY" in contract and validate_banknifty_contract(contract):
            return True, ""
    elif exchange == "BSE":
        if "SENSEX" in contract and validate_sensex_contract(contract):
            return True, ""
    return False, "Invalid contract format for exchange"

def get_expiry_from_contract(contract: str) -> Optional[str]:
    """
    Extract expiry date from contract identifier.

    Args:
        contract: Contract identifier (e.g., "NIFTY22050CE")

    Returns:
        Expiry date in YYYYMMDD format, or None if invalid
    """
    # Extract the numeric part after the index name
    match = re.search(r"(\d{6})$", contract)
    if not match:
        return None

    # Format: YYMMDD -> YYYYMMDD (assuming 20xx)
    date_str = match.group(1)
    if len(date_str) != 6:
        return None

    # Convert YYMMDD to YYYYMMDD
    year = "20" + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:]

    try:
        # Validate it's a valid date
        datetime.datetime(int(year), int(month), int(day))
        return year + month + day
    except ValueError:
        return None

def get_strike_from_contract(contract: str) -> Optional[int]:
    """
    Extract strike price from contract identifier.

    Args:
        contract: Contract identifier (e.g., "NIFTY22050CE")

    Returns:
        Strike price as integer, or None if invalid
    """
    # Extract the numeric part after the index name and option type
    match = re.search(r"(\d{5})([CEPE])", contract)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None

def is_valid_expiry(expiry: str) -> bool:
    """
    Validate expiry date format (YYYYMMDD).

    Args:
        expiry: Expiry date string

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.datetime.strptime(expiry, "%Y%m%d")
        return True
    except ValueError:
        return False

def get_valid_contracts(
    exchange: str, expiry: str, strike_interval: int = 10
) -> List[str]:
    """
    Get valid contracts for a given exchange, expiry, and strike interval.

    Args:
        exchange: "NSE" or "BSE"
        expiry: Expiry date in YYYYMMDD format
        strike_interval: Strike interval in points

    Returns:
        List of valid contract identifiers
    """
    if not is_valid_expiry(expiry):
        return []

    if exchange == "NSE":
        if "NIFTY" in expiry or "BANKNIFTY" in expiry:
            return discover_nifty_contracts(expiry, strike_interval) + discover_banknifty_contracts(expiry, strike_interval)
        elif "SENSEX" in expiry:
            return discover_sensex_contracts(expiry, strike_interval)
    elif exchange == "BSE":
        if "SENSEX" in expiry:
            return discover_sensex_contracts(expiry, strike_interval)

    return []

# Contract identification and validation
def identify_contract(
    exchange: str, contract: str
) -> Tuple[bool, str]:
    """
    Identify and validate a contract.

    Args:
        exchange: "NSE" or "BSE"
        contract: Contract identifier

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not contract:
        return False, "Empty contract"

    # Validate contract format based on exchange
    is_valid, error = validate_contract(exchange, contract)
    if not is_valid:
        return False, error

    # Additional validation
    if exchange in ["NSE", "BSE"]:
        if "NIFTY" in contract and not validate_nifty_contract(contract):
            return False, "Invalid NIFTY contract format"
        if "BANKNIFTY" in contract and not validate_banknifty_contract(contract):
            return False, "Invalid BANKNIFTY contract format"
        if "SENSEX" in contract and not validate_sensex_contract(contract):
            return False, "Invalid SENSEX contract format"

    return True, ""

def get_contract_info(contract: str) -> Dict[str, str]:
    """
    Extract information from a contract identifier.

    Args:
        contract: Contract identifier

    Returns:
        Dictionary with keys: exchange, expiry, strike, option_type
    """
    info = {
        "exchange": "",
        "expiry": "",
        "strike": "",
        "option_type": ""
    }

    # Extract exchange
    if "NIFTY" in contract:
        info["exchange"] = "NSE"
        info["expiry"] = contract[5:11]  # NIFTY22050 -> 22050
        info["option_type"] = contract[5:7]  # 22050CE -> CE
    elif "BANKNIFTY" in contract:
        info["exchange"] = "NSE"
        info["expiry"] = contract[8:14]  # BANKNIFTY22050 -> 22050
        info["option_type"] = contract[8:10]  # 22050CE -> CE
    elif "SENSEX" in contract:
        info["exchange"] = "BSE"
        info["expiry"] = contract[6:12]  # SENSEX22050 -> 22050
        info["option_type"] = contract[6:8]  # 22050CE -> CE

    # Validate extracted info
    info["strike"] = contract[:-3]  # Remove option type

    return info

# Timezone handling for Indian market
def get_india_timezone() -> str:
    """
    Return the Indian Standard Time timezone identifier.

    Returns:
        "Asia/Kolkata"
    """
    return "Asia/Kolkata"

def is_indian_market_open(date: datetime.date) -> bool:
    """
    Check if the Indian market is open on a given date.

    Args:
        date: Date to check

    Returns:
        True if market is open, False otherwise
    """
    # This is a simplified check - in practice, we'd need a comprehensive holiday calendar
    # For now, we assume all trading days are open (Monday-Friday, excluding holidays)
    return date.weekday() < 5  # Monday-Friday

def get_market_session(
    date: datetime.date,
    timezone: str = "Asia/Kolkata"
) -> Tuple[Optional[datetime.time], Optional[datetime.time]]:
    """
    Get the market session times for India.

    Args:
        date: Date to check
        timezone: Timezone identifier

    Returns:
        Tuple of (open_time, close_time) in local time, or None if market is closed
    """
    # Simplified - in practice, this would check against a holiday calendar
    if date.weekday() >= 5:  # Weekend
        return None, None

    # Standard market hours for Indian exchanges
    return datetime.time(9, 30), datetime.time(15, 30)

def get_valid_strike_range(
    exchange: str, contract: str
) -> Tuple[Optional[int], Optional[int]]:
    """
    Get the valid strike price range for a contract.

    Args:
        exchange: "NSE" or "BSE"
        contract: Contract identifier

    Returns:
        Tuple of (min_strike, max_strike) or (None, None) if invalid
    """
    info = get_contract_info(contract)
    if not info["exchange"] or not info["strike"]:
        return None, None

    strike = int(info["strike"])

    if exchange == "NSE":
        # NSE typically has strikes from 10000 to 30000 for NIFTY/BANKNIFTY
        min_strike = 10000
        max_strike = 30000
    elif exchange == "BSE":
        # BSE typically has strikes from 10000 to 35000 for SENSEX
        min_strike = 10000
        max_strike = 35000

    # Adjust based on actual contract
    if info["exchange"] == "NSE":
        if "NIFTY" in contract:
            min_strike = max(10000, strike - 5000)
            max_strike = min(30000, strike + 5000)
        elif "BANKNIFTY" in contract:
            min_strike = max(35000, strike - 10000)
            max_strike = min(45000, strike + 10000)
    elif info["exchange"] == "BSE":
        if "SENSEX" in contract:
            min_strike = max(15000, strike - 5000)
            max_strike = min(35000, strike + 5000)

    return min_strike, max_strike
# Auto-run helper: runs India module checks automatically
if __name__ == "__main__":
    from .india import discover_nifty_contracts, get_india_timezone, validate_nifty_contract
    print("Auto-check India module:")
    print("Timezone:", get_india_timezone())
    print("Sample valid contract:", validate_nifty_contract("NIFTY25050CE"))
