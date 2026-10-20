# 7Harvest AI Margin Intelligence — Expanded Prototype

## Dashboard modules
- Executive overview: KPIs, sales/contribution trends, brand and SKU performance
- Outlet & trade spend: outlet economics, trade-spend screening and listing-fee recovery proxy
- AI insights: Isolation Forest anomaly detection and transparent rule-based commercial recommendations
- Smart assortment: outlet-level SKU ranking using sales, contribution margin and an expiry penalty; designed as a prototype for store-format/location-based assortment
- Demand & logistics: weekday-average baseline demand forecast, replenishment proxy, RK/Soorya planning considerations, and the data requirements for delivery-route optimisation
- Scenario simulator: interactive trade-spend, sales and COGS sensitivity analysis
- Data & assumptions: provenance, limitations, sample records and CSV export

## Critical data limitation
The challenge documents do not contain transaction-level outlet/SKU sales, unit quantities, inventory, exact geolocation, delivery routes, expiry dates by batch, or granular costs. The app therefore generates synthetic demonstration data. Do not present generated sales, outlets, product costs, anomaly alerts, assortment decisions, forecasts, replenishment values or savings as actual 7Harvest results.

The demand module is a baseline demonstration, not a validated AI model. The assortment score is a transparent heuristic, not a trained model. The route-planning section explains the intended workflow but does not claim to optimise actual routes.

## Run locally
1. Install Python 3.10+.
2. Extract the ZIP and open a terminal in this folder.
3. Create a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Run: `streamlit run app.py`
6. Open the local URL printed in the terminal.

## Data needed to make this operational
- Date, outlet ID, SKU, units sold, net sales and selling price
- SKU COGS and granular rebate / promotion / listing fee / promoter expenses
- Outlet format, coordinates, shelf capacity, region and channel
- Inventory on hand, stock-outs, purchase orders, case pack, MOQ and supplier lead time
- Batch-level expiry dates and write-offs, especially for Soorya
- Vehicle capacity, delivery windows, order quantities, depot coordinates and route constraints

