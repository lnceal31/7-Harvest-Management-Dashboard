import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="7Harvest | AI Margin Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN / CSS
# ============================================================

st.markdown("""
<style>
:root {
    --green: #17613D;
    --green-dark: #10452D;
    --green-light: #E8F2EA;
    --page-bg: #F5F8F5;
    --card-bg: #FFFFFF;
    --text: #20352A;
    --muted: #627367;
    --border: #DCE6DD;
}

.stApp {
    background-color: #F5F8F5;
    color: #20352A;
    font-family: "Segoe UI", Arial, sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Text and headings */
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stCaptionContainer"] {
    color: #20352A;
}

h1, h2, h3 {
    color: #10452D !important;
    font-weight: 650 !important;
    letter-spacing: -0.4px;
}

h1 {
    font-size: 2rem !important;
}

h2 {
    font-size: 1.45rem !important;
}

h3 {
    font-size: 1.15rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EAF1EA;
    border-right: 1px solid #DCE6DD;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #20352A !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #10452D !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE6DD;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(23, 60, 38, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #627367 !important;
}

div[data-testid="stMetricValue"] {
    color: #10452D !important;
    font-weight: 700;
}

div[data-testid="stMetricDelta"] {
    color: #17613D !important;
}

/* Input fields */
.stApp input,
.stApp textarea {
    background-color: #FFFFFF !important;
    color: #20352A !important;
    border-color: #CBD8CC !important;
}

/* Dropdowns and multiselects */
.stApp [data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-color: #CBD8CC;
}

.stApp [data-baseweb="select"] input {
    color: #20352A !important;
}

.stApp [data-baseweb="select"] span {
    color: #20352A;
}

/* Buttons */
.stButton button {
    background-color: #17613D;
    color: #FFFFFF !important;
    border: 1px solid #17613D;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #10452D;
    border-color: #10452D;
    color: #FFFFFF !important;
}

/* Radio navigation */
section[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #20352A !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #20352A;
}

.stTabs [aria-selected="true"] {
    color: #17613D !important;
}

/* Charts and tables */
div[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE6DD;
    border-radius: 14px;
    padding: 10px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #DCE6DD;
    border-radius: 12px;
    overflow: hidden;
}

/* Dividers and alerts */
hr {
    border-color: #DCE6DD !important;
}

.stAlert {
    border-radius: 10px;
}

/* Links */
.stApp a {
    color: #17613D;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SYNTHETIC DEMO DATA
# ============================================================

rng = np.random.default_rng(7)


@st.cache_data
def make_demo_data():
    outlets = [
        ("OUT-001", "Metro Mart - Deira", "Modern Trade"),
        ("OUT-002", "Fresh Basket - Al Nahda", "Modern Trade"),
        ("OUT-003", "Green Corner Grocery", "General Trade"),
        ("OUT-004", "Family Hypermarket - Dubai", "Modern Trade"),
        ("OUT-005", "Neighbourhood Foods", "General Trade"),
        ("OUT-006", "QuickCart Online", "E-commerce"),
        ("OUT-007", "City Supermarket - Sharjah", "Modern Trade"),
        ("OUT-008", "Daily Needs Grocery", "General Trade"),
        ("OUT-009", "Value Foods - Ajman", "Modern Trade"),
        ("OUT-010", "Rapid Basket", "Quick-commerce"),
        ("OUT-011", "Sunrise Grocery", "General Trade"),
        ("OUT-012", "Prime Hypermarket", "Modern Trade"),
    ]

    rk_products = [
        ("RK-P01", "Basmati Rice 5kg", "RK Foods", "Rice", 0.625),
        ("RK-P02", "Toor Dal 1kg", "RK Foods", "Pulses", 0.625),
        ("RK-P03", "Turmeric Powder 200g", "RK Foods", "Spice powders", 0.625),
        ("RK-P04", "Black-eye Beans 1kg", "RK Foods", "Beans & peas", 0.625),
        ("RK-P05", "Cooking Oil 1L", "RK Foods", "Miscellaneous", 0.625),
        ("RK-P06", "Cumin Seeds 200g", "RK Foods", "Seeds", 0.625),
        ("RK-P07", "Cashews 500g", "RK Foods", "Nuts & dry fruits", 0.625),
    ]

    soorya_products = [
        ("SO-P01", "Malabar Porotta 5pc", "Soorya Foods", "Frozen / ready-to-cook", 0.40),
        ("SO-P02", "Whole Wheat Chapati 5pc", "Soorya Foods", "Frozen / ready-to-cook", 0.40),
        ("SO-P03", "Idli/Dosa Batter 1kg", "Soorya Foods", "Batter", 0.40),
        ("SO-P04", "Appam Batter 1kg", "Soorya Foods", "Batter", 0.40),
        ("SO-P05", "Ragi Batter 1kg", "Soorya Foods", "Batter", 0.40),
    ]

    products = rk_products + soorya_products
    rows = []

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=180,
        freq="D"
    )

    for day in dates:
        for outlet_id, outlet_name, channel in outlets:
            weekend_factor = 1.15 if day.dayofweek >= 4 else 1.0

            for pid, pname, brand, category, cogs_ratio in products:
                if brand == "RK Foods":
                    base = rng.uniform(220, 850)
                    trade_ratio = rng.uniform(0.035, 0.085)
                    vehicle_ratio = 0.0175
                else:
                    base = rng.uniform(140, 500)
                    trade_ratio = rng.uniform(0.035, 0.075)
                    vehicle_ratio = 0.05

                channel_factor = {
                    "Modern Trade": 1.25,
                    "General Trade": 0.78,
                    "E-commerce": 0.90,
                    "Quick-commerce": 0.82
                }[channel]

                sales = base * weekend_factor * channel_factor * rng.normal(1, 0.12)
                sales = max(20, sales)

                cogs = sales * cogs_ratio * rng.normal(1, 0.025)
                trade = sales * trade_ratio
                vehicle = sales * vehicle_ratio

                listing_fee = 0.0
                if day.day == 1 and brand == "RK Foods" and rng.random() < 0.055:
                    listing_fee = rng.choice([500, 750, 1200, 1800])

                promoter_cost = (
                    sales * (0.015 if brand == "RK Foods" else 0.0047)
                    if channel == "Modern Trade" else 0
                )

                expiry = sales * 0.02 if brand == "Soorya Foods" else 0

                rows.append({
                    "Date": day,
                    "Outlet ID": outlet_id,
                    "Outlet": outlet_name,
                    "Channel": channel,
                    "Product ID": pid,
                    "Product": pname,
                    "Brand": brand,
                    "Category": category,
                    "Sales AED": round(sales, 2),
                    "COGS AED": round(cogs, 2),
                    "Trade Spend AED": round(trade, 2),
                    "Vehicle Cost AED": round(vehicle, 2),
                    "Promoter Cost AED": round(promoter_cost, 2),
                    "Expiry Cost AED": round(expiry, 2),
                    "Listing Fee AED": listing_fee
                })

    df = pd.DataFrame(rows)

    # Synthetic anomalies for demonstration only.
    outlier_dates = (
        df["Date"].drop_duplicates().sort_values().tail(14).tolist()
    )

    mask = (
        (df["Outlet ID"] == "OUT-004")
        & (df["Date"].isin(outlier_dates))
        & (df["Brand"] == "RK Foods")
    )
    df.loc[mask, "Trade Spend AED"] *= 2.6

    mask2 = (
        (df["Outlet ID"] == "OUT-010")
        & (df["Date"].isin(outlier_dates))
        & (df["Brand"] == "Soorya Foods")
    )
    df.loc[mask2, "Expiry Cost AED"] *= 3.0

    df["Contribution AED"] = (
        df["Sales AED"]
        - df["COGS AED"]
        - df["Trade Spend AED"]
        - df["Vehicle Cost AED"]
        - df["Promoter Cost AED"]
        - df["Expiry Cost AED"]
        - df["Listing Fee AED"]
    )

    # Additional synthetic operational fields for the AI Forecaster demo.
    # These are simulated assumptions, not actual 7Harvest operational data.
    unit_prices = {
        "Basmati Rice 5kg": 32.0,
        "Toor Dal 1kg": 9.0,
        "Turmeric Powder 200g": 5.0,
        "Black-eye Beans 1kg": 8.0,
        "Cooking Oil 1L": 10.0,
        "Cumin Seeds 200g": 7.0,
        "Cashews 500g": 22.0,
        "Malabar Porotta 5pc": 8.0,
        "Whole Wheat Chapati 5pc": 7.0,
        "Idli/Dosa Batter 1kg": 9.0,
        "Appam Batter 1kg": 9.0,
        "Ragi Batter 1kg": 10.0,
    }
    df["Illustrative Unit Price AED"] = df["Product"].map(unit_prices).fillna(10.0)
    df["Units Sold"] = np.maximum(
        1, np.rint(df["Sales AED"] / df["Illustrative Unit Price AED"])
    ).astype(int)

    # Synthetic promotion indicator and customer orders, used as demo inputs.
    operational_rng = np.random.default_rng(27)
    df["Promotion Active"] = operational_rng.random(len(df)) < 0.08
    df["Customer Orders Units"] = np.maximum(
        0,
        np.rint(df["Units Sold"] * operational_rng.normal(1.02, 0.12, len(df)))
    ).astype(int)

    # Inventory snapshot per outlet/SKU, based on simulated days of cover.
    avg_units = df.groupby(["Outlet", "Product"])["Units Sold"].mean()
    inventory_rng = np.random.default_rng(42)
    inventory_map = {}
    for key, avg in avg_units.items():
        inventory_map[key] = max(0, int(round(avg * inventory_rng.uniform(1.5, 16))))
    df["Current Inventory Units"] = [
        inventory_map[(outlet, product)]
        for outlet, product in zip(df["Outlet"], df["Product"])
    ]

    df["Lead Time Days"] = np.where(df["Brand"] == "RK Foods", 5, 2)
    df["Shelf Life Days"] = np.where(
        df["Product"].str.contains("Batter", case=False), 5,
        np.where(df["Brand"] == "Soorya Foods", 90, 240)
    )

    # Approximate coordinates for route-planning demonstration only.
    outlet_coordinates = {
        "Metro Mart - Deira": (25.2697, 55.3095),
        "Fresh Basket - Al Nahda": (25.2930, 55.3730),
        "Green Corner Grocery": (25.2048, 55.2708),
        "Family Hypermarket - Dubai": (25.1180, 55.2006),
        "Neighbourhood Foods": (25.2760, 55.3420),
        "QuickCart Online": (25.1972, 55.2744),
        "City Supermarket - Sharjah": (25.3463, 55.4209),
        "Daily Needs Grocery": (25.2854, 55.3581),
        "Value Foods - Ajman": (25.4052, 55.5136),
        "Rapid Basket": (25.2040, 55.2700),
        "Sunrise Grocery": (25.2560, 55.3040),
        "Prime Hypermarket": (25.2285, 55.3273),
    }
    df["Latitude"] = df["Outlet"].map(lambda x: outlet_coordinates[x][0])
    df["Longitude"] = df["Outlet"].map(lambda x: outlet_coordinates[x][1])

    return df


df = make_demo_data()


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("7Harvest Management Dashboard")
st.caption(
    "Prototype using synthetic demonstration data"
)

st.divider()


# ============================================================
# SIDEBAR NAVIGATION AND FILTERS
# ============================================================

with st.sidebar:
    st.title("   KAIZEN TECH")
    st.caption("Hadiya | Nicole | Lance | Soha")
    st.divider()

    page = st.radio(
        "MAIN NAVIGATION",
        [
            "Overview",
            "AI Forecaster",
            "AI Assortment Optimisation",
            "Trade Spend & Rebate Optimisation",
            "Institutional Sales Pilot",
            "Rebate Calculator"
        ]
       
    )

    st.divider()
    st.subheader("Dashboard filters")

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()

    date_range = st.date_input(
        "Date range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )

    brands = st.multiselect(
        "Brand",
        sorted(df["Brand"].unique()),
        default=sorted(df["Brand"].unique())
    )

    channels = st.multiselect(
        "Channel",
        sorted(df["Channel"].unique()),
        default=sorted(df["Channel"].unique())
    )

    st.divider()
    st.caption("Demo environment · All records are synthetic")

# ============================================================
# FILTER DATA
# ============================================================

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_min, date_max

df_filtered = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Brand"].isin(brands))
    & (df["Channel"].isin(channels))
].copy()


def style_chart(fig, height=360):
    fig.update_layout(
        height=height, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(family="Segoe UI, Arial, sans-serif", color="#20352A", size=12),
        title_font=dict(size=16, color="#10452D"),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color="#20352A")),
        xaxis=dict(showgrid=False, linecolor="#DCE6DD", tickfont=dict(color="#627367")),
        yaxis=dict(gridcolor="#E9EFEA", zerolinecolor="#DCE6DD", tickfont=dict(color="#627367"))
    )
    return fig


def haversine_km(a, b):
    """Distance between two latitude/longitude pairs in kilometres."""
    from math import radians, sin, cos, asin, sqrt
    lat1, lon1 = a
    lat2, lon2 = b
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    h = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(min(1, h)))


def nearest_neighbour_route(points, depot):
    """Simple nearest-neighbour route heuristic, not a guaranteed optimum."""
    remaining = list(points)
    route = []
    current = depot
    while remaining:
        nxt = min(remaining, key=lambda p: haversine_km(current, p["coords"]))
        route.append(nxt)
        remaining.remove(nxt)
        current = nxt["coords"]
    return route


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":
    st.header("Overview")
    st.write("A decision-focused summary of demand, product economics and commercial performance across the proposed initiatives.")
    if df_filtered.empty:
        st.warning("No records match your selected filters.")
    else:
        sales = df_filtered["Sales AED"].sum()
        contribution = df_filtered["Contribution AED"].sum()
        margin = contribution / sales * 100 if sales else 0
        trade_spend = df_filtered["Trade Spend AED"].sum()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Net Sales", f"AED {sales:,.0f}")
        col2.metric("Contribution", f"AED {contribution:,.0f}")
        col3.metric("Contribution Margin", f"{margin:.1f}%")
        col4.metric("Trade Spend", f"AED {trade_spend:,.0f}")
        st.divider()
        left, right = st.columns(2)
        with left:
            st.subheader("Sales by brand")
            brand_sales = df_filtered.groupby("Brand", as_index=False)["Sales AED"].sum().sort_values("Sales AED", ascending=False)
            fig = px.bar(brand_sales, x="Brand", y="Sales AED", color="Brand", color_discrete_sequence=["#17613D", "#8BB99A"], labels={"Sales AED": "Sales (AED)"})
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with right:
            st.subheader("Sales trend")
            daily_sales = df_filtered.groupby("Date", as_index=False)["Sales AED"].sum()
            fig = px.line(daily_sales, x="Date", y="Sales AED", labels={"Sales AED": "Sales (AED)"})
            fig.update_traces(line=dict(color="#17613D", width=2.5))
            st.plotly_chart(style_chart(fig), use_container_width=True)
        st.subheader("Sales by channel")
        channel_sales = df_filtered.groupby("Channel", as_index=False)["Sales AED"].sum().sort_values("Sales AED", ascending=False)
        fig = px.bar(channel_sales, x="Channel", y="Sales AED", color="Sales AED", color_continuous_scale=["#C8E0CE", "#17613D"], labels={"Sales AED": "Sales (AED)"})
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig, 320), use_container_width=True)

# ============================================================
# AI FORECASTER - INITIATIVE 1
# ============================================================

elif page == "AI Forecaster":
    st.header("AI Forecaster")
    st.write("Improve existing operations, cut avoidable costs and increase profitability through smarter forecasting and logistics.")
  

 

    with st.expander("How it works", expanded=True):
        st.markdown("""
        **1. Demand forecasting:** Estimate future demand for each SKU using historical sales, weekday patterns, promotion indicators, customer orders and local outlet demand.

        **2. Stock and production planning:** Recommend stock levels and production/replenishment quantities using forecast demand, simulated inventory, lead times and expiry risk.

        **3. Delivery optimisation:** Group outlet deliveries and compare a simple consolidated route with separate depot-to-outlet trips.

        **4. Exception alerts:** Flag potential stockouts, excess stock and expiry risks so staff can investigate before losses occur. Late-delivery alerts require actual delivery-time data, which this prototype does not have.

        **5. Product-level economics:** Use each SKU's unit price, product costs, lead time and shelf life to tailor recommendations.

        **6. Improve the existing model:** The aim is to reduce avoidable waste, transport and inventory costs and improve contribution, not to depend on new products or price increases.
        """)


    st.divider()
    st.subheader("1. SKU-level demand forecast")
    f1, f2, f3 = st.columns(3)
    with f1:
        forecast_brand = st.selectbox("Company", sorted(df["Brand"].unique()), key="af_brand")
    brand_data = df[df["Brand"] == forecast_brand].copy()
    with f2:
        forecast_product = st.selectbox("Product / SKU", sorted(brand_data["Product"].unique()), key="af_product")
    product_data = brand_data[brand_data["Product"] == forecast_product].copy()
    with f3:
        forecast_outlet = st.selectbox("Outlet", sorted(product_data["Outlet"].unique()), key="af_outlet")

    chosen = product_data[product_data["Outlet"] == forecast_outlet].copy()
    daily_units = chosen.groupby("Date")["Units Sold"].sum().sort_index()
    daily_orders = chosen.groupby("Date")["Customer Orders Units"].sum().sort_index()
    if len(daily_units) < 28:
        st.warning("Not enough historical records for this forecast.")
    else:
        uplift_col, order_col = st.columns(2)
        with uplift_col:
            promo_uplift = st.slider("Assumed promotion uplift", 0, 50, 10, 5, format="%d%%")
        with order_col:
            order_weight = st.slider("Weight given to recent customer orders", 0, 100, 50, 10, format="%d%%")

        # Weekday-aware baseline: average units for each weekday over the last 8 weeks.
        hist = daily_units.tail(56)
        weekday_avg = hist.groupby(hist.index.dayofweek).mean()
        last_date = daily_units.index.max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=14, freq="D")
        recent_order_avg = daily_orders.tail(28).mean()
        predictions = []
        for future_day in future_dates:
            baseline = float(weekday_avg.get(future_day.dayofweek, hist.mean()))
            blended = (1 - order_weight / 100) * baseline + (order_weight / 100) * recent_order_avg
            predictions.append(max(0, blended * (1 + promo_uplift / 100)))
        forecast = pd.DataFrame({"Date": future_dates, "Forecast units": np.round(predictions, 1)})
        total_forecast_units = float(forecast["Forecast units"].sum())
        avg_daily_forecast = float(forecast["Forecast units"].mean())
        k1, k2, k3 = st.columns(3)
        k1.metric("Forecast demand (next 14 days)", f"{total_forecast_units:,.0f} units")
        k2.metric("Average daily forecast", f"{avg_daily_forecast:,.1f} units")
        k3.metric("Assumed promotion uplift", f"{promo_uplift}%")

        total_historical_units = max(1, int(chosen["Units Sold"].sum()))
        estimated_unit_cost = float(chosen["COGS AED"].sum() / total_historical_units)
        estimated_unit_sales_value = float(chosen["Sales AED"].sum() / total_historical_units)
        cost1, cost2, cost3 = st.columns(3)
        cost1.metric("Estimated product cost / unit", f"AED {estimated_unit_cost:,.2f}")
        cost2.metric("Forecast product cost", f"AED {total_forecast_units * estimated_unit_cost:,.2f}")
        cost3.metric("Forecast sales value", f"AED {total_forecast_units * estimated_unit_sales_value:,.2f}")
        st.caption("Product economics are estimated from synthetic historical sales and cost records. They exclude any future changes in supplier prices, trade terms or production efficiency.")

        hist_plot = daily_units.tail(56).rename("Historical units").reset_index()
        fig = px.line(hist_plot, x="Date", y="Historical units", title="Historical SKU demand and 14-day forecast")
        fig.add_scatter(x=forecast["Date"], y=forecast["Forecast units"], mode="lines+markers", name="Forecast units", line=dict(color="#D97706", width=3, dash="dash"))
        st.plotly_chart(style_chart(fig, 400), use_container_width=True)
        st.dataframe(forecast, use_container_width=True, hide_index=True)
        st.caption("Method: weekday averages from the last 56 days are blended with recent synthetic customer-order data and an adjustable promotion uplift. This is a transparent baseline model, not a trained ML forecast; validate it against held-out real data before business use.")

        st.divider()
        st.subheader("2. Stock, replenishment and expiry-risk planning")
        current_inventory = int(chosen.sort_values("Date").iloc[-1]["Current Inventory Units"])
        lead_days = int(chosen.iloc[-1]["Lead Time Days"])
        shelf_days = int(chosen.iloc[-1]["Shelf Life Days"])
        s1, s2, s3 = st.columns(3)
        s1.metric("Simulated current inventory", f"{current_inventory:,} units")
        s2.metric("Lead time", f"{lead_days} days")
        s3.metric("Assumed shelf life", f"{shelf_days} days")
        stock_a, stock_b = st.columns(2)
        with stock_a:
            safety_days = st.slider("Safety-stock buffer", 0, 14, 3, key="af_safety")
        with stock_b:
            holding_cost = st.number_input("Illustrative holding cost (AED / unit / 14 days)", min_value=0.0, value=0.10, step=0.05, key="af_holding")
        target_stock = avg_daily_forecast * (lead_days + safety_days)
        reorder_qty = max(0, int(np.ceil(target_stock - current_inventory)))
        days_cover = current_inventory / avg_daily_forecast if avg_daily_forecast > 0 else float("inf")
        excess_units = max(0, int(current_inventory - avg_daily_forecast * min(shelf_days, 14)))
        a, b, c = st.columns(3)
        a.metric("Target stock level", f"{target_stock:,.0f} units")
        b.metric("Suggested replenishment", f"{reorder_qty:,} units")
        c.metric("Estimated days of cover", "N/A" if not np.isfinite(days_cover) else f"{days_cover:.1f} days")
        if current_inventory < avg_daily_forecast * lead_days:
            st.error("Potential stockout: simulated inventory is below forecast demand during lead time. Prioritise a stock and supply review.")
        elif days_cover > shelf_days:
            st.warning("Expiry risk: simulated inventory cover exceeds the assumed shelf life. Review production, replenishment and stock rotation.")
        elif excess_units > 0:
            st.warning(f"Potential excess inventory: approximately {excess_units:,} units may exceed the next {min(shelf_days, 14)} days of forecast demand. Review before acting.")
        else:
            st.success("No immediate stock or expiry exception under the selected assumptions. Continue monitoring.")
        st.caption(f"Illustrative holding cost for the suggested stock level: AED {target_stock * holding_cost:,.2f} per 14-day period. This is a scenario estimate, not a verified saving. Production quantities require production capacity, minimum batch sizes and confirmed inventory records.")

        st.divider()
        st.subheader("3. Shipment planning and route decision")
        st.write("The route demo uses synthetic outlet coordinates and forecast demand. It compares a consolidated nearest-neighbour route with separate round trips from an illustrative Dubai depot. The heuristic is not guaranteed to find the globally shortest route.")
        route_df = brand_data.groupby(["Outlet", "Channel", "Latitude", "Longitude"], as_index=False).agg(Daily_Units=("Units Sold", "mean"), Avg_Sales_AED=("Sales AED", "mean"))
        route_df["Forecast 7-day units"] = np.ceil(route_df["Daily_Units"] * 7 * (1 + promo_uplift / 100)).astype(int)
        vehicle_capacity = st.number_input("Illustrative vehicle capacity (units)", min_value=100, max_value=10000, value=2500, step=100, key="af_capacity")
        cost_per_km = st.number_input("Illustrative delivery cost (AED/km)", min_value=0.1, max_value=20.0, value=1.5, step=0.1, key="af_costkm")
        selected_route_df = route_df.sort_values("Forecast 7-day units", ascending=False).head(8).copy()
        selected_route_df["Forecast 7-day units"] = selected_route_df["Forecast 7-day units"].astype(int)
        total_units = int(selected_route_df["Forecast 7-day units"].sum())
        loads_needed = max(1, int(np.ceil(total_units / vehicle_capacity)))
        st.metric("Estimated loads for selected high-demand outlets", f"{loads_needed}")
        st.caption("For this route comparison, the selected outlets are the eight highest-demand outlets for the chosen company. If demand exceeds capacity, multiple loads are indicated; detailed multi-vehicle scheduling is not implemented.")

        depot = (25.0657, 55.1713)  # illustrative Dubai depot location
        points = [{"name": r["Outlet"], "coords": (float(r["Latitude"]), float(r["Longitude"])), "units": int(r["Forecast 7-day units"]), "channel": r["Channel"]} for _, r in selected_route_df.iterrows()]
        route = nearest_neighbour_route(points, depot)
        if route:
            consolidated_km = haversine_km(depot, route[0]["coords"])
            for idx in range(len(route) - 1):
                consolidated_km += haversine_km(route[idx]["coords"], route[idx + 1]["coords"])
            consolidated_km += haversine_km(route[-1]["coords"], depot)
            separate_km = sum(2 * haversine_km(depot, p["coords"]) for p in points)
            saved_km = max(0, (separate_km - consolidated_km) * loads_needed)
            route_cost = consolidated_km * cost_per_km * loads_needed
            separate_cost = separate_km * cost_per_km * loads_needed
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("Consolidated route distance", f"{consolidated_km:,.1f} km")
            rc2.metric("Separate-trip distance", f"{separate_km:,.1f} km")
            rc3.metric("Indicative distance difference", f"{saved_km:,.1f} km")
            st.write("**Suggested visit sequence**")
            st.write("Depot → " + " → ".join(p["name"] for p in route) + " → Depot")
            st.write(f"Estimated consolidated delivery cost across {loads_needed} load(s): **AED {route_cost:,.2f}**. Separate round-trip benchmark: **AED {separate_cost:,.2f}**.")
            if loads_needed > 1:
                st.warning("The consolidated cost assumes the same route is repeated for each load. A production-grade planner should allocate outlets across vehicles and enforce capacity, time windows and driver-hour constraints.")
        st.dataframe(selected_route_df[["Outlet", "Channel", "Forecast 7-day units"]], use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("4. Exception monitoring")
        latest = brand_data.sort_values("Date").groupby(["Outlet", "Product"], as_index=False).tail(1).copy()
        # Calculate recent demand at each outlet/SKU to avoid relying only on the last row.
        recent_cutoff = brand_data["Date"].max() - pd.Timedelta(days=13)
        recent = brand_data[brand_data["Date"] >= recent_cutoff].groupby(["Outlet", "Product"], as_index=False).agg(Recent_Daily_Units=("Units Sold", "mean"))
        latest = latest.drop(columns=["Avg Daily Units"], errors="ignore").merge(recent, on=["Outlet", "Product"], how="left")
        latest["Days Cover"] = np.where(latest["Recent_Daily_Units"] > 0, latest["Current Inventory Units"] / latest["Recent_Daily_Units"], np.inf)
        latest["Alert"] = np.select(
            [latest["Days Cover"] < latest["Lead Time Days"], latest["Days Cover"] > latest["Shelf Life Days"]],
            ["Potential stockout", "Potential expiry / overstock"], default="Monitor"
        )
        alerts = latest[latest["Alert"] != "Monitor"].copy()
        if alerts.empty:
            st.success("No stockout or expiry exceptions were flagged by the current synthetic rules.")
        else:
            st.dataframe(alerts[["Outlet", "Product", "Current Inventory Units", "Recent_Daily_Units", "Days Cover", "Lead Time Days", "Shelf Life Days", "Alert"]].sort_values("Days Cover"), use_container_width=True, hide_index=True)
        st.caption("Late-delivery alerts are not generated because actual delivery timestamps and delivery windows are not present in the dataset. The route and alert outputs are illustrative planning signals and should be validated before operational use.")

# ============================================================
# AI ASSORTMENT OPTIMISATION - INITIATIVE 2
# ============================================================

elif page == "AI Assortment Optimisation":
    st.header("AI Assortment Optimisation")
    st.write("Recommend a more suitable product range for each retailer using sales velocity, contribution, inventory and expiry-risk indicators.")


    a1, a2 = st.columns(2)
    with a1:
        assortment_brand = st.selectbox("Company", sorted(df["Brand"].unique()), key="assort_brand")
    brand_assort = df[(df["Brand"] == assortment_brand) & df["Date"].dt.date.between(start_date, end_date)].copy()
    with a2:
        assortment_outlet = st.selectbox("Retailer / outlet", sorted(brand_assort["Outlet"].unique()), key="assort_outlet")

    outlet_data = brand_assort[brand_assort["Outlet"] == assortment_outlet].copy()
    other_data = brand_assort.copy()
    if outlet_data.empty:
        st.warning("No records match the selected outlet and date range.")
    else:
        sku = outlet_data.groupby(["Product", "Product ID", "Category"], as_index=False).agg(
            Sales_AED=("Sales AED", "sum"), Contribution_AED=("Contribution AED", "sum"),
            Units_Sold=("Units Sold", "sum"), Expiry_Cost_AED=("Expiry Cost AED", "sum"),
            Inventory_Units=("Current Inventory Units", "last"),
            Unit_Cost_AED=("COGS AED", "sum")
        )
        days_observed=max(1, outlet_data["Date"].nunique())
        sku["Units / day"] = sku["Units_Sold"] / days_observed
        sku["Contribution / unit (AED)"] = np.where(sku["Units_Sold"] > 0, sku["Contribution_AED"] / sku["Units_Sold"], 0)
        sku["Contribution margin (%)"] = np.where(sku["Sales_AED"] > 0, sku["Contribution_AED"] / sku["Sales_AED"] * 100, 0)
        velocity_median = float(sku["Units / day"].median())
        margin_median = float(sku["Contribution margin (%)"].median())

        def assortment_action(row):
            if row["Units / day"] >= sku["Units / day"].quantile(0.75) and row["Contribution / unit (AED)"] > 0:
                return "Prioritise"
            if row["Units / day"] <= sku["Units / day"].quantile(0.25) and row["Contribution margin (%)"] < margin_median:
                return "Review / test"
            return "Maintain and monitor"

        sku["Illustrative recommendation"] = sku.apply(assortment_action, axis=1)
        m1, m2, m3 = st.columns(3)
        m1.metric("SKUs in current range", f"{sku['Product'].nunique()}")
        m2.metric("SKUs to prioritise", f"{(sku['Illustrative recommendation'] == 'Prioritise').sum()}")
        m3.metric("SKUs to review", f"{(sku['Illustrative recommendation'] == 'Review / test').sum()}")

        st.subheader("Recommended assortment for this retailer")
        st.caption("Rules-based demonstration: recommendations compare this outlet's simulated sales velocity and contribution. They are not trained AI outputs or confirmed findings about the retailer.")
        show = sku[["Product", "Category", "Units / day", "Contribution / unit (AED)", "Contribution margin (%)", "Inventory_Units", "Expiry_Cost_AED", "Illustrative recommendation"]].copy()
        show = show.rename(columns={"Inventory_Units":"Simulated inventory (units)", "Expiry_Cost_AED":"Expiry cost (AED)"})
        st.dataframe(show.sort_values(["Illustrative recommendation", "Units / day"], ascending=[True, False]).round(2), use_container_width=True, hide_index=True)

        fig = px.scatter(sku, x="Units / day", y="Contribution / unit (AED)", size="Sales_AED", color="Illustrative recommendation", hover_name="Product", title="SKU velocity versus contribution per unit", color_discrete_sequence=["#17613D", "#8BB99A", "#D97706"])
        st.plotly_chart(style_chart(fig, 420), use_container_width=True)

        st.subheader("How to interpret the recommendations")
        st.markdown("""
        - **Prioritise:** relatively high simulated sales velocity and positive contribution per unit; consider maintaining availability and using the forecaster to set stock levels.
        - **Maintain and monitor:** performance does not trigger either simple rule; keep reviewing demand and margin.
        - **Review / test:** relatively low velocity and below-median contribution margin; investigate before reducing the range.

        Do not discontinue a product based on low sales alone. Check whether it was consistently in stock, whether demand is seasonal, its strategic value, repeat orders, shelf-space constraints and retailer agreements. The current synthetic data does not include all of these inputs.
        """)
        st.subheader("Portfolio productivity")
        all_sku = other_data.groupby(["Product", "Category"], as_index=False).agg(Sales_AED=("Sales AED", "sum"), Contribution_AED=("Contribution AED", "sum"), Units_Sold=("Units Sold", "sum"), Outlet_Count=("Outlet", "nunique"))
        all_sku["Contribution margin (%)"] = np.where(all_sku["Sales_AED"] > 0, all_sku["Contribution_AED"] / all_sku["Sales_AED"] * 100, 0)
        st.dataframe(all_sku.sort_values("Sales_AED", ascending=False).rename(columns={"Sales_AED":"Sales (AED)", "Contribution_AED":"Contribution (AED)", "Units_Sold":"Units sold", "Outlet_Count":"Outlets selling SKU"}).round(2), use_container_width=True, hide_index=True)

# ============================================================
# TRADE SPEND & REBATE OPTIMISATION - PROBLEM 2
# ============================================================

elif page == "Trade Spend & Rebate Optimisation":
    st.header("Trade Spend & Rebate Optimisation")
    st.write("Evaluate commercial support using customer-level economics, and compare current terms with a proposed, measurable retailer commitment.")

    r1, r2 = st.columns(2)
    with r1:
        rebate_brand = st.selectbox("Company", sorted(df["Brand"].unique()), key="rebate_brand")
    rb = df[(df["Brand"] == rebate_brand) & df["Date"].dt.date.between(start_date, end_date)].copy()
    with r2:
        rebate_outlet = st.selectbox("Retailer / outlet", sorted(rb["Outlet"].unique()), key="rebate_outlet")
    customer = rb[rb["Outlet"] == rebate_outlet]

    if customer.empty:
        st.warning("No records match the selected company, outlet and date range.")
    else:
        total_sales = float(customer["Sales AED"].sum())
        historical_trade_spend = float(customer["Trade Spend AED"].sum())
        historical_contribution = float(customer["Contribution AED"].sum())
        margin = historical_contribution / total_sales if total_sales else 0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sales", f"AED {total_sales:,.0f}")
        c2.metric("Recorded trade spend", f"AED {historical_trade_spend:,.0f}")
        c3.metric("Contribution after recorded costs", f"AED {historical_contribution:,.0f}")
        c4.metric("Contribution margin", f"{margin*100:.1f}%")

        st.subheader("Commercial performance by product")
        product_spend = customer.groupby("Product", as_index=False).agg(Sales=("Sales AED", "sum"), Contribution=("Contribution AED", "sum"), Trade_Spend=("Trade Spend AED", "sum"))
        product_spend["Trade spend / sales (%)"] = np.where(product_spend["Sales"] > 0, product_spend["Trade_Spend"] / product_spend["Sales"] * 100, 0)
        product_spend["Contribution margin (%)"] = np.where(product_spend["Sales"] > 0, product_spend["Contribution"] / product_spend["Sales"] * 100, 0)
        st.dataframe(product_spend.rename(columns={"Sales":"Sales (AED)", "Contribution":"Contribution (AED)", "Trade_Spend":"Recorded trade spend (AED)"}).round(2).sort_values("Sales (AED)", ascending=False), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Compare current and proposed terms")
        st.write("Model a transparent scenario where commercial support is linked to a measurable retailer commitment, such as a documented promotional display, flyer or advertising campaign.")
        x1, x2, x3 = st.columns(3)
        with x1:
            current_rate = st.number_input("Assumed current rebate (%)", min_value=0.0, max_value=30.0, value=5.0, step=0.5, key="current_rebate")
        with x2:
            proposed_rate = st.number_input("Proposed rebate (%)", min_value=0.0, max_value=30.0, value=4.0, step=0.5, key="proposed_rebate")
        with x3:
            uplift = st.slider("Assumed sales uplift from commitment", 0, 30, 5, 1, format="%d%%", key="rebate_uplift")
        campaign_cost = st.number_input("Additional campaign support (AED)", min_value=0.0, value=1000.0, step=250.0, key="campaign_support")

        expected_extra_sales = total_sales * uplift / 100
        extra_sales_contribution = expected_extra_sales * margin
        current_rebate_cost = total_sales * current_rate / 100
        proposed_rebate_cost = total_sales * proposed_rate / 100
        rebate_cost_change = current_rebate_cost - proposed_rebate_cost
        net_scenario_change = extra_sales_contribution + rebate_cost_change - campaign_cost
        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Assumed extra sales", f"AED {expected_extra_sales:,.0f}")
        q2.metric("Extra contribution", f"AED {extra_sales_contribution:,.0f}")
        q3.metric("Rebate cost reduction", f"AED {rebate_cost_change:,.0f}")
        q4.metric("Estimated net change", f"AED {net_scenario_change:,.0f}", delta="Positive scenario" if net_scenario_change >= 0 else "Negative scenario", delta_color="normal" if net_scenario_change >= 0 else "inverse")

        if net_scenario_change >= 0:
            st.success("Under these assumptions, the proposed terms have a positive estimated contribution impact. Validate the uplift and campaign delivery before making a decision.")
        else:
            st.warning("Under these assumptions, the proposed terms do not cover their estimated cost. Negotiate different terms or do not proceed without stronger evidence.")
        st.caption("Scenario formula: estimated contribution from assumed incremental sales + reduction in assumed rebate cost − additional campaign support. It assumes the historical contribution margin applies to incremental sales. It does not establish causality or include all possible contractual costs.")

        st.subheader("Commercial safeguards")
        st.markdown("""
        - Link additional support to objective, documented commitments and evidence of delivery.
        - Review RK Foods' existing customer-by-product rebate structure and Soorya Foods' customer-level discount structure separately.
        - Do not assume a rebate or shelf-space payment is automatically unlawful; review the proposed terms and market circumstances with qualified legal counsel.
        - Check applicable UAE competition-law requirements and any relevant price-monitoring constraints before implementation.
        """)

# ============================================================
# INSTITUTIONAL SALES PILOT - INITIATIVE 3
# ============================================================

elif page == "Institutional Sales Pilot":
    st.header("Institutional Sales Pilot")


    i1, i2 = st.columns(2)
    with i1:
        pilot_brand = st.selectbox("Company", sorted(df["Brand"].unique()), key="pilot_brand")
    with i2:
        buyer_type = st.selectbox("Potential buyer type", ["School catering contractor", "Hospital catering contractor", "School", "Hospital"], key="buyer_type")
    pilot_data = df[(df["Brand"] == pilot_brand) & df["Date"].dt.date.between(start_date, end_date)].copy()
    if pilot_data.empty:
        st.warning("No records match the selected company and date range.")
    else:
        latest_snapshot = pilot_data.sort_values("Date").groupby(["Outlet", "Product"], as_index=False).tail(1)
        inventory_summary = latest_snapshot.groupby("Product", as_index=False).agg(
            Current_Inventory_Units=("Current Inventory Units", "sum"),
            Shelf_Life_Days=("Shelf Life Days", "min")
        )
        product_summary = pilot_data.groupby(["Product", "Category"], as_index=False).agg(
            Units_Sold=("Units Sold", "sum"), Sales_AED=("Sales AED", "sum"),
            COGS_AED=("COGS AED", "sum"), Contribution_AED=("Contribution AED", "sum"),
            Expiry_Cost_AED=("Expiry Cost AED", "sum"), Unit_Price=("Illustrative Unit Price AED", "mean")
        )
        product_summary = product_summary.merge(inventory_summary, on="Product", how="left")
        product_summary = product_summary.rename(columns={"Current_Inventory_Units": "Current Inventory Units", "Shelf_Life_Days": "Shelf Life Days"})
        observed_days=max(1, pilot_data["Date"].nunique())
        product_summary["Average units / day"] = product_summary["Units_Sold"] / observed_days
        product_summary["Estimated cost / unit (AED)"] = np.where(product_summary["Units_Sold"] > 0, product_summary["COGS_AED"] / product_summary["Units_Sold"], 0)
        product_summary["Contribution margin (%)"] = np.where(product_summary["Sales_AED"] > 0, product_summary["Contribution_AED"] / product_summary["Sales_AED"] * 100, 0)

        st.subheader("Product suitability and surplus scenario")
        chosen_products = st.multiselect("Products to include in the pilot", product_summary["Product"].tolist(), default=product_summary["Product"].tolist()[:min(3, len(product_summary))], key="pilot_products")
        p1, p2, p3 = st.columns(3)
        with p1:
            pilot_order_units = st.number_input("Illustrative order quantity per selected SKU", min_value=1, max_value=100000, value=100, step=25, key="pilot_order_units")
        with p2:
            min_shelf_life = st.number_input("Minimum remaining shelf-life requirement (days)", min_value=1, max_value=365, value=14, step=1, key="pilot_shelf")
        with p3:
            delivery_cost = st.number_input("Estimated delivery cost per pilot order (AED)", min_value=0.0, value=250.0, step=50.0, key="pilot_delivery")

        selected = product_summary[product_summary["Product"].isin(chosen_products)].copy()
        if selected.empty:
            st.warning("Choose at least one product to estimate the pilot economics.")
        else:
            selected["Requested units"] = pilot_order_units
            selected["Inventory after order (units)"] = selected["Current Inventory Units"] - selected["Requested units"]
            selected["Estimated sales value (AED)"] = selected["Requested units"] * selected["Unit_Price"]
            selected["Estimated product cost (AED)"] = selected["Requested units"] * selected["Estimated cost / unit (AED)"]
            selected["Estimated contribution before delivery (AED)"] = selected["Estimated sales value (AED)"] - selected["Estimated product cost (AED)"]
            selected["Shelf-life check"] = np.where(selected["Shelf Life Days"] >= min_shelf_life, "Passes assumed shelf-life check", "Review shelf-life requirement")
            selected["Inventory check"] = np.where(selected["Current Inventory Units"] >= selected["Requested units"], "Inventory appears sufficient", "Would require replenishment")
            st.dataframe(selected[["Product", "Category", "Current Inventory Units", "Shelf Life Days", "Average units / day", "Requested units", "Inventory check", "Shelf-life check", "Estimated sales value (AED)", "Estimated product cost (AED)"]].round(2), use_container_width=True, hide_index=True)
            total_value = float(selected["Estimated sales value (AED)"].sum())
            total_cost = float(selected["Estimated product cost (AED)"].sum())
            gross_contribution = total_value - total_cost - delivery_cost
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Potential order value", f"AED {total_value:,.0f}")
            h2.metric("Estimated product cost", f"AED {total_cost:,.0f}")
            h3.metric("Assumed delivery cost", f"AED {delivery_cost:,.0f}")
            h4.metric("Illustrative contribution after delivery", f"AED {gross_contribution:,.0f}")
            if (selected["Shelf Life Days"] < min_shelf_life).any():
                st.warning("At least one selected product fails the assumed shelf-life requirement. Confirm buyer specifications and remaining shelf life before including it.")
            if (selected["Current Inventory Units"] < selected["Requested units"]).any():
                st.warning("At least one selected SKU exceeds simulated inventory. Do not promise supply until replenishment and production feasibility are confirmed.")
            if gross_contribution < 0:
                st.error("The scenario has negative contribution after the assumed delivery cost. Review pricing, order size, product selection or logistics before proceeding.")
            st.caption(f"Buyer scenario: {buyer_type}. Estimates use assumed unit prices and historical synthetic cost ratios. Actual order specifications, food-safety requirements, remaining shelf life, payment terms, buyer approval and repeat-order behaviour must be validated.")

        st.subheader("Pilot success measures")
        st.markdown("""
        Track contribution after delivery, order fulfilment reliability, repeat orders, payment timing, customer retention and whether any sale prevents avoidable expiry without undermining regular profitable channels. Start with a limited pilot and expand only after validated results.
        """)

# rebate calculator 

elif page == "Rebate Calculator":
    st.title("🧮 Rebate Calculator")
    st.caption(
        "Calculate estimated rebates by company, outlet branch and product."
    )

    # Select the company
    companies = sorted(df["Brand"].dropna().unique())

    selected_company = st.selectbox(
        "Select Company",
        companies
    )

    # Filter branches based on the selected company
    company_data = df[df["Brand"] == selected_company]

    branches = sorted(company_data["Outlet"].dropna().unique())

    selected_branch = st.selectbox(
        "Select Outlet Branch",
        branches
    )

    # Filter products based on the company and branch
    branch_data = company_data[
        company_data["Outlet"] == selected_branch
    ]

    products = sorted(branch_data["Product"].dropna().unique())

    selected_product = st.selectbox(
        "Select Product",
        products
    )

    # Get sales records for the selected product
    product_data = branch_data[
        branch_data["Product"] == selected_product
    ]

    # Calculate sales from the existing dataset
    total_sales = product_data["Sales AED"].sum()

    st.divider()
    st.subheader("Rebate Details")

    rebate_rate = st.number_input(
        "Rebate Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )

    # Calculate rebate
    rebate_amount = total_sales * rebate_rate / 100

    # Display results
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sales",
        f"AED {total_sales:,.2f}"
    )

    col2.metric(
        "Rebate Rate",
        f"{rebate_rate:.2f}%"
    )

    col3.metric(
        "Estimated Rebate",
        f"AED {rebate_amount:,.2f}"
    )

    st.divider()

    st.subheader("Calculation Summary")

    st.write(f"**Company:** {selected_company}")
    st.write(f"**Outlet Branch:** {selected_branch}")
    st.write(f"**Product:** {selected_product}")
    st.write(f"**Eligible Sales:** AED {total_sales:,.2f}")
    st.write(f"**Rebate Rate:** {rebate_rate:.2f}%")

    st.success(
        f"Estimated rebate payable: AED {rebate_amount:,.2f}"
    )

    st.caption(
        "Prototype calculation using synthetic sales data. "
        "The rebate rate is illustrative and should be replaced "
        "with the applicable commercial agreement."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("7Harvest Management Dashboard | Prototype by Kaizen | Synthetic demonstration data only. All figures are illustrative and must not be interpreted as actual company performance.")
