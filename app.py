import streamlit as st
import pandas as pd
import plotly.express as px

# Upload Excel file
st.title("🧶 Carpet Inventory Dashboard")

uploaded_file = st.file_uploader("Upload your Excel sheet", type=["xlsx", "xls"])

if uploaded_file:
    # Load Excel sheet
    df = pd.read_excel(uploaded_file)

    # Ensure proper column names
    df.columns = [
        "Serial No",
        "Carpet Origin & Manufacturer",
        "Size",
        "Cost (BHD)",
        "Selling Price (BHD)",
        "Current Status"
    ]

    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # Filter by status
    status_filter = st.multiselect(
        "Filter by Current Status",
        options=["Available", "Sold", "Returned", "Send to Saudi"],
        default=["Available", "Sold", "Returned", "Send to Saudi"]
    )

    filtered_df = df[df["Current Status"].isin(status_filter)]

    # KPIs
    total_carpets = len(filtered_df)
    total_cost = filtered_df["Cost (BHD)"].sum()
    total_revenue = filtered_df["Selling Price (BHD)"].sum()
    profit = total_revenue - total_cost

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🧺 Total Carpets", total_carpets)
    col2.metric("💰 Total Cost (BHD)", f"{total_cost:,.2f}")
    col3.metric("📈 Total Revenue (BHD)", f"{total_revenue:,.2f}")
    col4.metric("🏦 Profit (BHD)", f"{profit:,.2f}")

    # Pie chart - Status Distribution
    st.subheader("📊 Status Distribution")
    status_counts = filtered_df["Current Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig_pie = px.pie(status_counts, names="Status", values="Count", title="Carpet Status Breakdown")
    st.plotly_chart(fig_pie)

    # Bar chart - Manufacturer vs Count
    st.subheader("🏭 Carpets by Origin/Manufacturer")
    manufacturer_counts = filtered_df["Carpet Origin & Manufacturer"].value_counts().reset_index()
    manufacturer_counts.columns = ["Manufacturer", "Count"]

    fig_bar = px.bar(
        manufacturer_counts,
        x="Manufacturer",
        y="Count",
        title="Carpet Distribution by Manufacturer",
        text="Count"
    )
    st.plotly_chart(fig_bar)

    # Profit by Manufacturer
    st.subheader("💹 Profit by Manufacturer")
    profit_df = filtered_df.copy()
    profit_df["Profit"] = profit_df["Selling Price (BHD)"] - profit_df["Cost (BHD)"]
    profit_by_manufacturer = profit_df.groupby("Carpet Origin & Manufacturer")["Profit"].sum().reset_index()

    fig_profit = px.bar(
        profit_by_manufacturer,
        x="Carpet Origin & Manufacturer",
        y="Profit",
        title="Profit by Manufacturer",
        text="Profit"
    )
    st.plotly_chart(fig_profit)

    # Download filtered data
    st.subheader("⬇️ Download Filtered Data")
    st.download_button(
        label="Download as Excel",
        data=filtered_df.to_excel(index=False, engine="openpyxl"),
        file_name="filtered_carpet_inventory.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
