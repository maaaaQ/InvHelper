from enum import Enum


class FilterDividendPolicy(str, Enum):
    DIVIDEND = "dividend"
    NO_DIVIDEND = "no_dividend"


class FilterOccupation(str, Enum):
    OIL_AND_GAS = "oil_and_gas"
    BANKS = "banks"
    FINANCE = "finance"
    METALLURGY = "metallurgy"
    RETAIL = "retail"
    ELECTRIC_GENERATION = "electric_generation"
    TELECOM = "telecom"
    TRANSPORT = "transport"
    INTERNET = "imternet"
    MEDIA = "media"
    BUILDERS = "builders"
    OTHERS = "others"
