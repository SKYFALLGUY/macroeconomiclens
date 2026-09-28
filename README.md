# 🔭 MacroLens V1

> **An AI-powered Indian macroeconomic research assistant and dashboard tracking Leading, Coincident, and Lagging indicators.**

---

## 🌟 Overview

MacroLens is designed to analyze the economic momentum and business cycle phase of the Indian economy. It is built on three core foundations:

1. **Indicator Classification**:
   - **Leading Indicators**: Anticipate economic turning points 3 to 6 months in advance (*Manufacturing PMI, Services PMI, Non-Food Bank Credit Growth, 10Y G-Sec vs 91-Day T-Bill Yield Spread*).
   - **Coincident Indicators**: Measure the real-time heartbeat of domestic production and demand (*Gross GST Collections, Index of Industrial Production (IIP), Electricity Demand Growth, Passenger Vehicle Dispatches*).
   - **Lagging Indicators**: Confirm and validate established cyclical trends (*Headline CPI Inflation, WPI Inflation, RBI Policy Repo Rate, Quarterly Real GDP Growth*).
2. **Strict Data Provenance**:
   - Every observation explicitly cites its **Source** (e.g. MOSPI, RBI, Ministry of Finance, S&P Global), **Observation Date**, **Reporting Frequency**, **Unit**, and **Dataset Type**.
   - No fabricated or implied "live" economic numbers.
3. **Decoupled Financial Markets**:
   - Market sentiment proxies (*Nifty 50, Bank Nifty, 10-Year G-Sec Yield, USD/INR, Brent Crude Oil*) are isolated in a dedicated section to separate financial speculation from fundamental economic accounting.
4. **Evidence-First Macro Briefing**:
   - Grounded directly in verified telemetry.
   - Enforces strict separation between **[Observation]** and **[Interpretation]**.
   - Highlights **divergences** and conflicting signals.
   - Articulates **uncertainties and data publication lags**.
   - Recommends actionable **next research directions**.

---

## 🚀 Deployment on Streamlit Community Cloud

MacroLens is fully configured for deployment on **Streamlit Community Cloud** (running on Linux containers):

1. **GitHub Setup**:
   - Push this directory to your GitHub account (a `.gitignore` is included to exclude `.venv/` and `.env`).
2. **Deploy via Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and click **New app**.
   - Select your repository and branch (`main`).
   - Set **Main file path** to:
     ```text
     app.py
     ```
3. **Secrets Configuration (Optional)**:
   - In your app dashboard on Streamlit Cloud, go to **App Settings** $\rightarrow$ **Secrets**.
   - Paste any desired secrets (e.g. Gemini API key for future AI features):
     ```toml
     GEMINI_API_KEY = "your_actual_key_here"
     ```

---

## 💻 Local Quick Start

### Windows (Easy 1-Click Method):
Double-click the **`run_macrolens.bat`** file in this folder.
Your default web browser will automatically open at `http://localhost:8501`.

### Command Line (Cross-Platform: Windows / Linux / macOS):
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Architecture

```text
Macro/
├── app.py                         # [ENTRY POINT] Streamlit frontend & interactive dashboard
├── requirements.txt               # Python library dependencies for deployment
├── run_macrolens.bat              # Optional Windows 1-click launcher (not used on Linux)
├── README.md                      # Project documentation and deployment guide
├── .gitignore                     # Git ignore rules (protects .venv, .env, secrets)
├── .env.example                   # Local environment variable template
│
├── .streamlit/
│   └── secrets.toml.example       # Streamlit Cloud secrets template
│
├── core/
│   ├── __init__.py                # Package initialization
│   ├── models.py                  # Data structures: MacroIndicator, Observation, MarketQuote
│   └── normalizer.py              # Data loaders, MoM/YoY delta calculations & formatting
│
├── data/
│   ├── macro_seed.json            # Curated historical Indian macro series with provenance
│   └── market_service.py          # Decoupled market quotes (yfinance + fallback safety)
│
└── assistant/
    ├── __init__.py                # Package initialization
    ├── gemini_client.py           # Synthesis client for evidence-first briefings
    └── prompt_templates.py        # Evidence-first system prompt & guidelines
```
