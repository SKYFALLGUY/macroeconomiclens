"""
Data models for MacroLens V1.
Ensures strict typing, provenance metadata tracking, and mathematically correct calculations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal

CategoryType = Literal["leading", "coincident", "lagging"]
DirectionType = Literal["up", "down", "flat"]


def format_display_date(raw_date: str) -> str:
    """
    Converts raw dates into standardized macroeconomic period strings.
    - '2024-08-01' -> 'Aug 2024'
    - '2024-Q2 (Apr-Jun)' -> 'Q1 FY25 (Apr–Jun 2024)'
    """
    if not raw_date or raw_date == "N/A":
        return "N/A"

    # Handle standard YYYY-MM-DD
    if len(raw_date) == 10 and raw_date[4] == "-" and raw_date[7] == "-":
        try:
            dt = datetime.strptime(raw_date, "%Y-%m-%d")
            return dt.strftime("%b %Y")
        except ValueError:
            pass

    # Handle quarterly strings
    if "Q" in raw_date:
        # Standardize Indian fiscal year representation if quarter string
        # e.g., '2024-Q2 (Apr-Jun)' is Q1 FY25 in Indian fiscal year terminology
        mapping = {
            "2022-Q4 (Oct-Dec)": "Q3 FY23 (Oct–Dec 2022)",
            "2023-Q1 (Jan-Mar)": "Q4 FY23 (Jan–Mar 2023)",
            "2023-Q2 (Apr-Jun)": "Q1 FY24 (Apr–Jun 2023)",
            "2023-Q3 (Jul-Sep)": "Q2 FY24 (Jul–Sep 2023)",
            "2023-Q4 (Oct-Dec)": "Q3 FY24 (Oct–Dec 2023)",
            "2024-Q1 (Jan-Mar)": "Q4 FY24 (Jan–Mar 2024)",
            "2024-Q2 (Apr-Jun)": "Q1 FY25 (Apr–Jun 2024)",
        }
        return mapping.get(raw_date, raw_date)

    return raw_date


@dataclass
class MacroObservation:
    """A single macroeconomic data point."""
    date: str          # YYYY-MM-DD or YYYY-Q#
    value: float

    @property
    def display_date(self) -> str:
        return format_display_date(self.date)


@dataclass
class MacroIndicator:
    """A macroeconomic indicator series with full provenance metadata."""
    id: str
    name: str
    category: CategoryType
    unit: str
    frequency: str                     # Monthly, Quarterly, Fortnightly
    source: str                        # MOSPI, RBI, MoF, S&P Global, etc.
    description: str
    dataset_type: str = "Curated Historical Seed"
    methodology_note: str = ""
    history: List[MacroObservation] = field(default_factory=list)

    @property
    def latest_observation(self) -> Optional[MacroObservation]:
        if not self.history:
            return None
        return self.history[-1]

    @property
    def previous_observation(self) -> Optional[MacroObservation]:
        if len(self.history) < 2:
            return None
        return self.history[-2]

    @property
    def latest_value(self) -> Optional[float]:
        obs = self.latest_observation
        return obs.value if obs else None

    @property
    def previous_value(self) -> Optional[float]:
        obs = self.previous_observation
        return obs.value if obs else None

    @property
    def raw_latest_date(self) -> str:
        obs = self.latest_observation
        return obs.date if obs else "N/A"

    @property
    def display_date(self) -> str:
        obs = self.latest_observation
        return obs.display_date if obs else "N/A"

    @property
    def previous_display_date(self) -> str:
        obs = self.previous_observation
        return obs.display_date if obs else "N/A"

    @property
    def delta(self) -> Optional[float]:
        if self.latest_value is None or self.previous_value is None:
            return None
        return round(self.latest_value - self.previous_value, 2)

    @property
    def delta_unit(self) -> str:
        """Returns mathematically correct delta units (e.g. 'pp' for rates, 'pts' for indices)."""
        u = self.unit.lower()
        if "%" in u or "percent" in u:
            return "pp"  # percentage points
        elif "bps" in u:
            return "bps"
        elif "index" in u:
            return "pts"
        elif "lakh cr" in u or "crore" in u:
            return "Lakh Cr"
        return self.unit

    @property
    def formatted_delta(self) -> str:
        """Mathematically precise delta string."""
        d = self.delta
        if d is None:
            return "—"
        return f"{d:+0.2f} {self.delta_unit}"

    @property
    def direction(self) -> DirectionType:
        d = self.delta
        if d is None or abs(d) < 0.001:
            return "flat"
        return "up" if d > 0 else "down"


@dataclass
class MarketQuote:
    """A financial market observation."""
    symbol: str
    name: str
    price: float
    change: float
    pct_change: float
    currency: str
    as_of: str
    source: str = "Yahoo Finance"
    frequency: str = "Daily"
    history_dates: List[str] = field(default_factory=list)
    history_prices: List[float] = field(default_factory=list)
    status: str = "Live Feed"
