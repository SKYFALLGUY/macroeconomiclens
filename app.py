"""
MacroLens V1 - Indian Macroeconomic Research Assistant & Dashboard.
Built with Python, Streamlit, and Plotly.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.models import format_display_date
from core.normalizer import (
    load_indicators,
    get_indicators_by_category,
    format_indicators_for_ai,
)
from data.market_service import get_market_overview
from assistant.gemini_client import get_macro_briefing

# --- Page Configuration ---
st.set_page_config(
    page_title="MacroLens | Indian Macroeconomic Assistant",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Professional Institutional Styling ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 1.95rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
    }
    .sub-header {
        font-size: 0.98rem;
        color: #475569;
        margin-bottom: 1.1rem;
        line-height: 1.4;
    }
    .baseline-alert {
        background-color: #F8FAFC;
        border-left: 4px solid #0284C7;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 18px;
        font-size: 0.88rem;
        color: #1E293B;
    }
    .baseline-tag-prominent {
        background-color: #0284C7;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 2px 7px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }
    .metric-card-pro {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 14px 16px;
        height: 100%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .metric-title-pro {
        font-size: 0.88rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    .metric-value-pro {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
        font-feature-settings: "tnum";
    }
    .metric-unit-pro {
        font-size: 0.80rem;
        color: #64748B;
        font-weight: 500;
        margin-left: 4px;
    }
    .delta-badge-up {
        display: inline-block;
        color: #15803D;
        font-weight: 600;
        font-size: 0.82rem;
        margin-top: 4px;
    }
    .delta-badge-down {
        display: inline-block;
        color: #B91C1C;
        font-weight: 600;
        font-size: 0.82rem;
        margin-top: 4px;
    }
    .delta-badge-flat {
        display: inline-block;
        color: #64748B;
        font-weight: 600;
        font-size: 0.82rem;
        margin-top: 4px;
    }
    .pro-badge {
        display: inline-block;
        background-color: #F1F5F9;
        color: #475569;
        font-size: 0.70rem;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 3px;
        margin-right: 4px;
        margin-top: 8px;
        border: 1px solid #E2E8F0;
        letter-spacing: 0.02em;
    }
    .badge-leading {
        background-color: #F0F9FF;
        color: #0369A1;
        border-color: #BAE6FD;
    }
    .badge-coincident {
        background-color: #FEFCE8;
        color: #A16207;
        border-color: #FEF08A;
    }
    .badge-lagging {
        background-color: #F8FAFC;
        color: #475569;
        border-color: #CBD5E1;
    }
    .badge-market {
        background-color: #F0FDF4;
        color: #166534;
        border-color: #BBF7D0;
    }
    .badge-static {
        background-color: #FFF7ED;
        color: #C2410C;
        border-color: #FFEDD5;
    }
    .methodology-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 0.88rem;
        color: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Load Data ---
@st.cache_data(ttl=300)
def fetch_all_data():
    indicators = load_indicators()
    market = get_market_overview()
    return indicators, market

try:
    indicators, market = fetch_all_data()
except Exception as e:
    st.error(f"Error loading macroeconomic data: {e}")
    st.stop()


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### MacroLens V1")
    st.caption("Indian Macroeconomic Research Dashboard")
    st.markdown("---")

    st.markdown("#### Data Architecture")
    st.markdown(
        """
        - **Macroeconomic Series**:  
          `Curated Historical Baseline`  
          *Period: Aug 2023 – Aug 2024 / Q1 FY25*  
          *Sources: MOSPI, RBI, MoF, S&P Global*
        - **Financial Markets**:  
          `Decoupled Live / Fallback Feeds`  
          *Source: NSE & Global Interbank via Yahoo Finance*
        - **Sovereign Yield**:  
          `Static Settlement Reference`  
          *Source: CCIL / RBI Aug 2024 Benchmark*
        """
    )
    st.markdown("---")

    st.markdown("#### System Integrity")
    st.markdown(
        """
        - **Mathematical Standard**: All rate deltas expressed in percentage points (`pp`) or basis points (`bps`).
        - **Date Standardization**: Period notation (`Aug 2024`, `Q1 FY25`).
        - **Zero Fabrication**: Grounded citations only.
        """
    )

    st.markdown("---")
    if st.button("Refresh Cache"):
        st.cache_data.clear()
        st.rerun()

    st.caption("MacroLens V1.1 • Research Specification")


# --- MAIN HEADER ---
st.markdown('<div class="main-header">MacroLens: Indian Macroeconomic Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Analytical tracking of Leading, Coincident, and Lagging macroeconomic indicators with evidence-first synthesis.</div>',
    unsafe_allow_html=True,
)

# --- PROMINENT TOP-LEVEL DATA DISCLOSURE ---
st.markdown(
    """
    <div class="baseline-alert">
        <span class="baseline-tag-prominent">Historical Baseline: Aug 2023 – Aug 2024</span>
        <strong>DATASET PROVENANCE NOTICE:</strong> The macroeconomic metrics displayed on this dashboard reflect a 
        <strong>verified historical research baseline</strong> (August 2023 to August 2024 for monthly series; Q1 FY25 for quarterly GDP). 
        This is <strong>not a live macroeconomic wire service</strong>. Financial market sentiment indicators (Nifty, USD/INR, Crude) are 
        tracked separately in the Markets section.
    </div>
    """,
    unsafe_allow_html=True,
)

# --- MAIN TABS ---
tab_macro, tab_markets, tab_briefing = st.tabs([
    "Macroeconomic Indicators",
    "Financial Markets",
    "Macroeconomic Synthesis & AI Briefing",
])


# ==========================================
# TAB 1: MACROECONOMIC INDICATORS
# ==========================================
with tab_macro:
    st.markdown("#### Macroeconomic Indicator Pillars")
    st.caption(
        "Indicators are categorized into three analytical classes based on their temporal relationship with the economic cycle: "
        "Leading (3–6 month forward horizon), Coincident (current-month activity), and Lagging (confirmatory and policy anchoring)."
    )

    pillar = st.radio(
        "Select Analytical Pillar:",
        options=["Leading Indicators", "Coincident Indicators", "Lagging Indicators"],
        horizontal=True,
    )

    category_key = "leading" if "Leading" in pillar else "coincident" if "Coincident" in pillar else "lagging"
    selected_indicators = get_indicators_by_category(indicators, category_key)

    # 4 Metric Cards in 2x2 Clean Grid
    col_r1c1, col_r1c2 = st.columns(2)
    col_r2c1, col_r2c2 = st.columns(2)
    card_cols = [col_r1c1, col_r1c2, col_r2c1, col_r2c2]

    badge_class = f"badge-{category_key}"

    for idx, ind in enumerate(selected_indicators[:4]):
        with card_cols[idx]:
            delta_class = (
                "delta-badge-up" if ind.direction == "up" else
                "delta-badge-down" if ind.direction == "down" else
                "delta-badge-flat"
            )
            arrow = "▲" if ind.direction == "up" else "▼" if ind.direction == "down" else "●"

            st.markdown(
                f"""
                <div class="metric-card-pro">
                    <div class="metric-title-pro">{ind.name}</div>
                    <div class="metric-value-pro">
                        {ind.latest_value} <span class="metric-unit-pro">{ind.unit}</span>
                    </div>
                    <div class="{delta_class}">
                        {arrow} {ind.formatted_delta} vs {ind.previous_display_date} ({ind.previous_value})
                    </div>
                    <div>
                        <span class="pro-badge {badge_class}">{ind.category.upper()}</span>
                        <span class="pro-badge">PERIOD: {ind.display_date}</span>
                        <span class="pro-badge">FREQ: {ind.frequency.upper()}</span>
                        <span class="pro-badge">SOURCE: {ind.source.upper()}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dedicated Historical Series & Methodology Inspector (Prevents Card Layout Shifts)
    st.markdown("#### Historical Trajectory & Methodology Inspector")
    st.caption("Select an indicator to inspect its full historical series, statistical behavior, and classification rationale.")

    ind_names = [ind.name for ind in selected_indicators]
    selected_ind_name = st.selectbox("Select Series to Inspect:", options=ind_names, index=0)
    target_ind = next(ind for ind in selected_indicators if ind.name == selected_ind_name)

    col_chart, col_method = st.columns([3, 2])

    with col_chart:
        # Plotly chart with clean standardized period dates
        dates = [o.display_date for o in target_ind.history]
        values = [o.value for o in target_ind.history]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=values,
                mode="lines+markers",
                name=target_ind.name,
                line=dict(color="#0284C7", width=2.5),
                marker=dict(size=6, color="#0369A1"),
            )
        )

        if "PMI" in target_ind.name:
            fig.add_hline(y=50, line_dash="dash", line_color="#94A3B8", annotation_text="50 (Neutral)")
        elif "CPI" in target_ind.name:
            fig.add_hline(y=4.0, line_dash="dash", line_color="#10B981", annotation_text="4.0% RBI Target")
            fig.add_hrect(y0=2.0, y1=6.0, fillcolor="rgba(16, 185, 129, 0.06)", line_width=0)
        elif target_ind.id == "yield_spread_10y_91d":
            fig.add_hline(y=0, line_dash="dash", line_color="#EF4444", annotation_text="0 bps (Inversion Line)")

        fig.update_layout(
            margin=dict(l=20, r=20, t=25, b=20),
            height=280,
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickangle=-30),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=target_ind.unit),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_method:
        st.markdown(
            f"""
            <div class="methodology-box">
                <strong>Series Definition:</strong><br>
                {target_ind.description}<br><br>
                <strong>Methodology & Rationale:</strong><br>
                {target_ind.methodology_note}<br><br>
                <strong>Provenance:</strong><br>
                Official release from <em>{target_ind.source}</em> ({target_ind.dataset_type}).
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Methodology & Rationale Framework Disclosure
    with st.expander("Indicator Methodology & Classification Rationale"):
        st.markdown(
            """
            ### Classification Rationale & Methodological Nuances

            Economic indicators do not always behave as universal, static truths. In India's emerging market context, 
            several indicators exhibit context-dependent or mixed properties:

            1. **Wholesale Price Index (WPI) Inflation**:
               - *Current Classification*: Lagging (Price index group).
               - *Methodological Nuance*: WPI measures producer and input prices (primary commodities, fuel, manufactured inputs). 
                 Because wholesale costs transmit to consumer prices with a 2–3 month lead time, WPI frequently acts as a 
                 **leading or coincident driver of retail CPI and corporate profit margins**, rather than a purely lagging indicator.
            
            2. **Non-Food Bank Credit Growth**:
               - *Current Classification*: Leading (Credit availability).
               - *Methodological Nuance*: While credit expansion facilitates future capital formation, empirical evidence from 
                 RBI working papers indicates that headline bank credit disbursement often **coincides with or lags** business cycle 
                 inflection points. Working capital demands surge during late-cycle inventory accumulation, and disbursements trail 
                 initial investment commitments.

            3. **Passenger Vehicle (PV) Dispatches**:
               - *Current Classification*: Coincident (Discretionary consumption).
               - *Methodological Nuance*: SIAM data tracks **wholesale shipments from vehicle factories to dealerships**, not final retail 
                 registrations by consumers (tracked separately via the Ministry of Road Transport's Vahan database). When OEMs push inventory, 
                 wholesale dispatches can remain positive even as retail off-take softens and dealer inventory days expand.

            4. **Yield Curve Spread (10Y G-Sec vs. 91-Day T-Bill)**:
               - *Current Classification*: Leading (Term structure).
               - *Methodological Nuance*: While a classic leading indicator of monetary stance and growth expectations, India's sovereign debt 
                 market is influenced by Statutory Liquidity Ratio (SLR) bank investment quotas and RBI Open Market Operations (OMOs), which 
                 partially buffer yield spread sensitivity relative to freely floating benchmark curves like US Treasuries.
            """
        )


# ==========================================
# TAB 2: FINANCIAL MARKETS
# ==========================================
with tab_markets:
    st.markdown("#### Financial Market Sentiment Indicators")
    st.caption(
        "Financial market indicators reflect capital pricing, liquidity conditions, and external sentiment. "
        "They are presented in this separate section to maintain strict demarcation between financial asset pricing and fundamental economic accounting."
    )

    m_col1, m_col2, m_col3 = st.columns(3)
    m_col4, m_col5, _ = st.columns(3)
    market_col_list = [m_col1, m_col2, m_col3, m_col4, m_col5]

    quote_keys = ["^NSEI", "^NSEBANK", "INR=X", "BZ=F", "IN10Y"]

    for idx, key in enumerate(quote_keys):
        if key in market:
            quote = market[key]
            with market_col_list[idx]:
                delta_class = "delta-badge-up" if quote.change >= 0 else "delta-badge-down"
                arrow = "▲" if quote.change >= 0 else "▼"
                status_badge_class = "badge-static" if "Static" in quote.status else "badge-market"

                st.markdown(
                    f"""
                    <div class="metric-card-pro">
                        <div class="metric-title-pro">{quote.name} ({quote.symbol})</div>
                        <div class="metric-value-pro">
                            {quote.price:,.2f} <span class="metric-unit-pro">{quote.currency}</span>
                        </div>
                        <div class="{delta_class}">
                            {arrow} {quote.change:+0.2f} ({quote.pct_change:+0.2f}%)
                        </div>
                        <div>
                            <span class="pro-badge {status_badge_class}">{quote.status.upper()}</span>
                            <span class="pro-badge">PERIOD: {quote.as_of}</span>
                            <span class="pro-badge">FREQ: {quote.frequency.upper()}</span>
                            <span class="pro-badge">SOURCE: {quote.source.upper()}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Market Trends & Macroeconomic Transmission")

    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown("**Equity Benchmark Trajectory (Recent Closes)**")
        nifty = market.get("^NSEI")
        if nifty and nifty.history_dates:
            fig_m1 = go.Figure()
            fig_m1.add_trace(
                go.Scatter(
                    x=nifty.history_dates,
                    y=nifty.history_prices,
                    mode="lines+markers",
                    name="Nifty 50",
                    line=dict(color="#0284C7", width=2),
                )
            )
            fig_m1.update_layout(
                height=260,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Index Level"),
            )
            st.plotly_chart(fig_m1, use_container_width=True)

    with c_m2:
        st.markdown("**External Headwinds & Cost Pressures**")
        crude = market.get("BZ=F")
        usdinr = market.get("INR=X")
        yield10y = market.get("IN10Y")
        st.markdown(
            f"""
            - **Brent Crude Oil**: **${crude.price:.2f}/bbl** ({crude.status})  
              *Transmission*: India imports over 85% of crude oil requirements. Fluctuations impact current account balance and fuel inflation.
            - **USD / INR**: **₹{usdinr.price:.2f}** ({usdinr.status})  
              *Transmission*: Influences imported inflation pass-through, foreign portfolio investment (FPI) flows, and RBI foreign exchange reserves.
            - **India 10Y Benchmark Sovereign Yield**: **{yield10y.price:.2f}%** ({yield10y.status})  
              *Transmission*: Primary pricing anchor for long-term domestic corporate credit, state development loans (SDLs), and commercial borrowing costs.
            """
        )


# ==========================================
# TAB 3: MACROECONOMIC SYNTHESIS & AI BRIEFING
# ==========================================
with tab_briefing:
    st.markdown("#### Macroeconomic Synthesis & Baseline Briefing")
    st.caption(
        "Structured, evidence-first analytical briefing generated dynamically from the currently loaded macroeconomic baseline (Aug 2023 – Aug 2024). "
        "Separates factual observations from interpretation, highlights indicator divergences, and articulates data publication lags."
    )

    # Dynamic generation directly from the loaded indicators
    briefing_content = get_macro_briefing(indicators)
    st.markdown(briefing_content)

    st.markdown("---")
    st.markdown("#### Future Interactive AI Research Integration")
    st.info(
        "ℹ️ **Status**: In this V1 baseline release, the analytical synthesis above is generated programmatically from verified telemetry. "
        "Live interactive Q&A and scenario testing powered by Google Gemini will be enabled in the next phase after core data pipelines are established."
    )
