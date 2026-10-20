
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import IsolationForest

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
            "Operations",
            "Assortment",
            "Trade Spend",
            "New Channels"
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


# ============================================================
# HELPER: PLOTLY LAYOUT
# ============================================================

def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            color="#20352A",
            size=12
        ),
        title_font=dict(size=16, color="#10452D"),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="#20352A")
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#DCE6DD",
            tickfont=dict(color="#627367")
        ),
        yaxis=dict(
            gridcolor="#E9EFEA",
            zerolinecolor="#DCE6DD",
            tickfont=dict(color="#627367")
        )
    )
    return fig


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":
    st.header("Overview")
    st.write("Monitor sales, contribution and commercial performance.")

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

            brand_sales = (
                df_filtered.groupby("Brand", as_index=False)["Sales AED"]
                .sum()
                .sort_values("Sales AED", ascending=False)
            )

            fig = px.bar(
                brand_sales,
                x="Brand",
                y="Sales AED",
                color="Brand",
                color_discrete_sequence=["#17613D", "#8BB99A"],
                labels={"Sales AED": "Sales (AED)", "Brand": "Brand"}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:
            st.subheader("Sales trend")

            daily_sales = (
                df_filtered.groupby("Date", as_index=False)["Sales AED"]
                .sum()
            )

            fig = px.line(
                daily_sales,
                x="Date",
                y="Sales AED",
                labels={"Sales AED": "Sales (AED)", "Date": "Date"}
            )
            fig.update_traces(
                line=dict(color="#17613D", width=2.5)
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Sales by channel")

        channel_sales = (
            df_filtered.groupby("Channel", as_index=False)["Sales AED"]
            .sum()
            .sort_values("Sales AED", ascending=False)
        )

        fig = px.bar(
            channel_sales,
            x="Channel",
            y="Sales AED",
            color="Sales AED",
            color_continuous_scale=["#C8E0CE", "#17613D"],
            labels={"Sales AED": "Sales (AED)", "Channel": "Channel"}
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig, height=320), use_container_width=True)


# ============================================================
# OPERATIONS
# ============================================================

elif page == "Operations":
    st.header("Operations")
    st.write("Demand trends, replenishment priorities and logistics.")

    if df_filtered.empty:
        st.warning("No records match your selected filters.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Units / product records",
            f"{len(df_filtered):,}"
        )
        col2.metric(
            "Active outlets",
            f"{df_filtered['Outlet'].nunique():,}"
        )
        col3.metric(
            "Daily average sales",
            f"AED {df_filtered.groupby('Date')['Sales AED'].sum().mean():,.0f}"
        )

        st.divider()
        st.subheader("Daily demand trend")

        daily = (
            df_filtered.groupby("Date", as_index=False)["Sales AED"]
            .sum()
        )

        fig = px.line(
            daily,
            x="Date",
            y="Sales AED",
            labels={"Sales AED": "Sales (AED)", "Date": "Date"}
        )
        fig.update_traces(line=dict(color="#17613D", width=2.5))
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Outlet sales performance")

        outlet_sales = (
            df_filtered.groupby("Outlet", as_index=False)["Sales AED"]
            .sum()
            .sort_values("Sales AED", ascending=False)
        )

        fig = px.bar(
            outlet_sales,
            x="Sales AED",
            y="Outlet",
            orientation="h",
            color="Sales AED",
            color_continuous_scale=["#C8E0CE", "#17613D"],
            labels={"Sales AED": "Sales (AED)", "Outlet": "Outlet"}
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )
        st.plotly_chart(style_chart(fig, height=440), use_container_width=True)

        st.caption(
            "These sales records are synthetic. They do not represent actual "
            "demand forecasts or real delivery performance."
        )


# ============================================================
# ASSORTMENT
# ============================================================

elif page == "Assortment":
    st.header("Assortment")
    st.write("Explore product performance across outlets and channels.")

    if df_filtered.empty:
        st.warning("No records match your selected filters.")
    else:
        product_summary = (
            df_filtered.groupby(
                ["Product", "Brand", "Category"], as_index=False
            )
            .agg(
                Sales=("Sales AED", "sum"),
                Contribution=("Contribution AED", "sum"),
                Expiry_Cost=("Expiry Cost AED", "sum"),
                Outlets=("Outlet", "nunique")
            )
            .sort_values("Sales", ascending=False)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Products", f"{product_summary['Product'].nunique():,}")
        col2.metric(
            "Categories",
            f"{product_summary['Category'].nunique():,}"
        )
        col3.metric(
            "Total expiry cost",
            f"AED {product_summary['Expiry_Cost'].sum():,.0f}"
        )

        st.divider()
        st.subheader("Product sales ranking")

        fig = px.bar(
            product_summary.sort_values("Sales", ascending=True),
            x="Sales",
            y="Product",
            color="Brand",
            orientation="h",
            color_discrete_sequence=["#17613D", "#8BB99A"],
            labels={"Sales": "Sales (AED)", "Product": "Product"}
        )
        st.plotly_chart(style_chart(fig, height=440), use_container_width=True)

        st.subheader("Product performance table")

        display_products = product_summary.rename(columns={
            "Sales": "Sales (AED)",
            "Contribution": "Contribution (AED)",
            "Expiry_Cost": "Expiry cost (AED)",
            "Outlets": "Outlet count"
        })

        st.dataframe(
            display_products,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "This is descriptive product analysis, not an AI-generated "
            "assortment recommendation."
        )


# ============================================================
# TRADE SPEND
# ============================================================

elif page == "Trade Spend":
    st.header("Trade Spend")
    st.write("Monitor commercial investment and spending efficiency.")

    if df_filtered.empty:
        st.warning("No records match your selected filters.")
    else:
        total_spend = df_filtered["Trade Spend AED"].sum()
        total_sales = df_filtered["Sales AED"].sum()
        spend_rate = total_spend / total_sales * 100 if total_sales else 0

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Trade Spend", f"AED {total_spend:,.0f}")
        col2.metric("Sales", f"AED {total_sales:,.0f}")
        col3.metric("Trade Spend / Sales", f"{spend_rate:.2f}%")

        st.divider()
        left, right = st.columns(2)

        with left:
            st.subheader("Spend by brand")

            spend_by_brand = (
                df_filtered.groupby("Brand", as_index=False)["Trade Spend AED"]
                .sum()
            )

            fig = px.bar(
                spend_by_brand,
                x="Brand",
                y="Trade Spend AED",
                color="Brand",
                color_discrete_sequence=["#17613D", "#8BB99A"],
                labels={
                    "Trade Spend AED": "Trade spend (AED)",
                    "Brand": "Brand"
                }
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:
            st.subheader("Spend by channel")

            spend_by_channel = (
                df_filtered.groupby("Channel", as_index=False)["Trade Spend AED"]
                .sum()
                .sort_values("Trade Spend AED", ascending=False)
            )

            fig = px.bar(
                spend_by_channel,
                x="Channel",
                y="Trade Spend AED",
                color="Trade Spend AED",
                color_continuous_scale=["#C8E0CE", "#17613D"],
                labels={
                    "Trade Spend AED": "Trade spend (AED)",
                    "Channel": "Channel"
                }
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Trade spend detail")

        spend_detail = (
            df_filtered.groupby(
                ["Outlet", "Brand"], as_index=False
            )
            .agg(
                Sales=("Sales AED", "sum"),
                Trade_Spend=("Trade Spend AED", "sum")
            )
        )

        spend_detail["Spend Rate (%)"] = np.where(
            spend_detail["Sales"] > 0,
            spend_detail["Trade_Spend"] / spend_detail["Sales"] * 100,
            0
        )

        spend_detail = spend_detail.rename(columns={
            "Sales": "Sales (AED)",
            "Trade_Spend": "Trade spend (AED)"
        })

        st.dataframe(
            spend_detail.sort_values(
                "Trade spend (AED)", ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# NEW CHANNELS
# ============================================================

elif page == "New Channels":
    st.header("New Channels")
    st.write("Explore sales performance across current channels.")

    if df_filtered.empty:
        st.warning("No records match your selected filters.")
    else:
        channel_summary = (
            df_filtered.groupby("Channel", as_index=False)
            .agg(
                Sales=("Sales AED", "sum"),
                Contribution=("Contribution AED", "sum"),
                Trade_Spend=("Trade Spend AED", "sum"),
                Outlets=("Outlet", "nunique")
            )
            .sort_values("Sales", ascending=False)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current channels",
            f"{channel_summary['Channel'].nunique():,}"
        )
        col2.metric(
            "Channel sales",
            f"AED {channel_summary['Sales'].sum():,.0f}"
        )
        col3.metric(
            "Channel contribution",
            f"AED {channel_summary['Contribution'].sum():,.0f}"
        )

        st.divider()
        st.subheader("Channel sales and contribution")

        fig = px.bar(
            channel_summary,
            x="Channel",
            y=["Sales", "Contribution"],
            barmode="group",
            color_discrete_sequence=["#17613D", "#8BB99A"],
            labels={"value": "Amount (AED)", "variable": "Metric"}
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Channel economics")

        channel_summary = channel_summary.rename(columns={
            "Sales": "Sales (AED)",
            "Contribution": "Contribution (AED)",
            "Trade_Spend": "Trade spend (AED)",
            "Outlets": "Outlet count"
        })

        st.dataframe(
            channel_summary,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "This section compares existing synthetic channels. "
            "New-channel market sizing, opportunity scoring and scenario "
            "forecasts have not yet been implemented."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "7Harvest Management Dashboard | Prototype by Kaizen | "
    "Synthetic demonstration data only. All figures are illustrative "
    "and must not be interpreted as actual company performance."
)
