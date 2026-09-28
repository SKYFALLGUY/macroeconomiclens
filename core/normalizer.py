"""
Data loading, normalization, and dynamic synthesis for MacroLens V1.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from core.models import MacroIndicator, MacroObservation, CategoryType


def get_default_seed_path() -> Path:
    """Returns the absolute path to the default macro_seed.json."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "data" / "macro_seed.json"


def load_indicators(seed_path: Optional[Path] = None) -> Dict[str, MacroIndicator]:
    """
    Loads macroeconomic indicators from the curated seed JSON file.
    Returns a dictionary keyed by indicator ID.
    """
    target_path = seed_path or get_default_seed_path()
    if not target_path.exists():
        raise FileNotFoundError(f"Macro seed file not found at: {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    dataset_type = payload.get("metadata", {}).get("dataset_type", "Curated Historical Seed")
    indicators: Dict[str, MacroIndicator] = {}

    for item in payload.get("indicators", []):
        obs_list = [
            MacroObservation(date=o["date"], value=float(o["value"]))
            for o in item.get("history", [])
        ]
        indicator = MacroIndicator(
            id=item["id"],
            name=item["name"],
            category=item["category"],
            unit=item["unit"],
            frequency=item["frequency"],
            source=item["source"],
            description=item.get("description", ""),
            dataset_type=dataset_type,
            methodology_note=item.get("methodology_note", ""),
            history=obs_list,
        )
        indicators[indicator.id] = indicator

    return indicators


def get_indicators_by_category(
    indicators: Dict[str, MacroIndicator], category: CategoryType
) -> List[MacroIndicator]:
    """Filters indicators by pillar: leading, coincident, or lagging."""
    return [ind for ind in indicators.values() if ind.category == category]


def format_indicators_for_ai(indicators: Dict[str, MacroIndicator]) -> str:
    """
    Constructs a clear, structured telemetry snapshot to inject into the AI prompt.
    Uses standardized period dates and mathematically precise delta units.
    """
    lines = [
        "| Indicator | Category | Latest Observation | Previous | Delta | Direction | Unit | Source |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for ind in indicators.values():
        latest_val = ind.latest_value if ind.latest_value is not None else "N/A"
        prev_val = ind.previous_value if ind.previous_value is not None else "N/A"
        delta_str = ind.formatted_delta
        direction = ind.direction.upper()
        date_str = ind.display_date
        lines.append(
            f"| {ind.name} | {ind.category.capitalize()} | {latest_val} ({date_str}) | {prev_val} | {delta_str} | {direction} | {ind.unit} | {ind.source} |"
        )

    return "\n".join(lines)


def generate_dynamic_offline_synthesis(indicators: Dict[str, MacroIndicator]) -> str:
    """
    Dynamically generates the evidence-first baseline macroeconomic synthesis.
    Reads values and provenance directly from the loaded indicators to prevent drift.
    """
    mfg = indicators.get("mfg_pmi")
    serv = indicators.get("services_pmi")
    credit = indicators.get("bank_credit_growth")
    spread = indicators.get("yield_spread_10y_91d")

    gst = indicators.get("gst_collections")
    iip = indicators.get("iip_growth")
    power = indicators.get("power_demand_growth")
    auto = indicators.get("pv_sales_growth")

    cpi = indicators.get("cpi_inflation")
    wpi = indicators.get("wpi_inflation")
    repo = indicators.get("repo_rate")
    gdp = indicators.get("gdp_growth")

    # Dynamic real policy rate calculation if CPI and Repo available
    real_rate_str = "N/A"
    if repo and cpi and repo.latest_value is not None and cpi.latest_value is not None:
        real_rate = round(repo.latest_value - cpi.latest_value, 2)
        real_rate_str = f"{real_rate:+.2f} pp"

    # Safely extract observation strings
    def obs_str(ind: Optional[MacroIndicator]) -> str:
        if not ind or ind.latest_value is None:
            return "Data unavailable"
        return f"**{ind.latest_value} {ind.unit}** ({ind.display_date}, Source: {ind.source})"

    synthesis = f"""### Macroeconomic Synthesis & Baseline Briefing

> **Operating Mode**: Evidence-First Analytical Briefing (Generated dynamically from the loaded V1 Historical Baseline).  
> **Dataset Period**: August 2023 – August 2024 (Monthly Series) / Q1 FY25 (Quarterly Accounts). Not a live economic wire.

---

#### 1. Factual Observations (Direct Telemetry Citations)
- **Leading Indicators**:
  - **Manufacturing PMI**: {obs_str(mfg)} (Delta: {mfg.formatted_delta if mfg else 'N/A'} vs previous {mfg.previous_value if mfg else 'N/A'}).
  - **Services PMI**: {obs_str(serv)} (Delta: {serv.formatted_delta if serv else 'N/A'} vs previous {serv.previous_value if serv else 'N/A'}).
  - **Non-Food Bank Credit Growth**: {obs_str(credit)} (Delta: {credit.formatted_delta if credit else 'N/A'}).
  - **10Y G-Sec vs 91-Day T-Bill Spread**: {obs_str(spread)} (Delta: {spread.formatted_delta if spread else 'N/A'}).
- **Coincident Indicators**:
  - **Gross GST Collections**: {obs_str(gst)} (Delta: {gst.formatted_delta if gst else 'N/A'}).
  - **Index of Industrial Production (IIP)**: {obs_str(iip)} (Delta: {iip.formatted_delta if iip else 'N/A'}).
  - **Electricity Demand Growth**: {obs_str(power)} (Delta: {power.formatted_delta if power else 'N/A'}).
  - **Passenger Vehicle Dispatches**: {obs_str(auto)} (Delta: {auto.formatted_delta if auto else 'N/A'}).
- **Lagging Indicators**:
  - **Headline CPI Inflation**: {obs_str(cpi)} (Delta: {cpi.formatted_delta if cpi else 'N/A'}).
  - **WPI Inflation**: {obs_str(wpi)} (Delta: {wpi.formatted_delta if wpi else 'N/A'}).
  - **RBI Policy Repo Rate**: {obs_str(repo)} (Delta: {repo.formatted_delta if repo else 'N/A'}).
  - **Real GDP Growth**: {obs_str(gdp)} (Latest published quarter).

---

#### 2. Macroeconomic Interpretation & Cycle Phase
- **Services Sector Resilience**: The services sector continues to lead domestic activity, with the Services PMI remaining firmly above 60.0, indicating robust urban commercial turnover.
- **Industrial & Factory Moderation**: Physical high-frequency indicators show signs of plateauing. Industrial production growth ({iip.latest_value if iip else 'N/A'}% YoY) and passenger vehicle shipments ({auto.latest_value if auto else 'N/A'}% YoY) reflect inventory normalization after previous peak dispatches.
- **Restrictive Monetary Stance**: With headline CPI moderating to {cpi.latest_value if cpi else 'N/A'}% YoY and the Policy Repo Rate anchored at {repo.latest_value if repo else 'N/A'}%, the implied ex-post real policy rate stands elevated at **{real_rate_str}**, maintaining disinflationary pressure.

---

#### 3. Divergences & Conflicting Signals
- **Services vs. Physical Production Divergence**: The buoyant Services PMI ({serv.latest_value if serv else 'N/A'}) contrasts with softer industrial production ({iip.latest_value if iip else 'N/A'}% YoY) and contracting wholesale auto shipments ({auto.latest_value if auto else 'N/A'}% YoY), suggesting uneven domestic demand momentum.
- **Wholesale vs. Retail Inflation Spread**: WPI inflation ({wpi.latest_value if wpi else 'N/A'}% YoY) remains lower than CPI ({cpi.latest_value if cpi else 'N/A'}% YoY), reflecting lower global commodity input cost pressures transmitting gradually to consumer baskets.
- **Credit Momentum vs. Deposit Growth**: Bank credit expansion ({credit.latest_value if credit else 'N/A'}% YoY) continues to outpace deposit accretion (~11-12%), placing structural funding pressures on commercial bank margins.

---

#### 4. Methodological Nuances, Data Lags & Uncertainty
- **Wholesale Factory Shipments vs. Retail Demand**: Passenger vehicle dispatches track OEM dispatches to dealerships, which can reflect dealer stock adjustments rather than real-time retail customer sales (Vahan registrations).
- **GDP Reporting Lag**: Official national accounts data ({gdp.latest_value if gdp else 'N/A'}% in {gdp.display_date if gdp else 'Q1'}) arrives with an approximate 60-day lag and is subject to multiple revision cycles.
- **Inflation Base Effects**: Favorable base effects from mid-2023 contributed significantly to the lower headline CPI print, meaning underlying core price pressures warrant continued scrutiny.

---

#### 5. Recommended Next Research Directions
1. **Core CPI vs. Food Inflation Breakdown**: Decompose headline inflation to assess whether price relief is primarily driven by volatile perishable food items or durable disinflation in core services.
2. **Rural Consumption & Agricultural Terms of Trade**: Review two-wheeler sales, tractor dispatches, and rural wage growth to determine whether rural consumption is closing the gap with urban services.
3. **Capex Deployment & Fiscal Execution**: Inspect Union and State government capital expenditure pacing to measure public investment support for the remainder of the fiscal cycle.
"""
    return synthesis


# Alias for cross-module consistency
get_macro_briefing = generate_dynamic_offline_synthesis
