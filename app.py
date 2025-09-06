import streamlit as st
import pandas as pd
import plotly.express as px
import io

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

    # Convert numeric columns to numbers
    df["Cost (BHD)"] = pd.to_numeric(df["Cost (BHD)"], errors="coerce").fillna(0)
    df["Selling Price (BHD)"] = pd.to_numeric(df["Selling Price (BHD)"], errors="coerce").fillna(0)

    # Calculate profit and profit margin
    df["Profit"] = df["Selling Price (BHD)"] - df["Cost (BHD)"]
    df["Profit Margin (%)"] = (df["Profit"] / df["Cost (BHD)"]) * 100

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
    total_profit = filtered_df["Profit"].sum()
    overall_margin = (total_profit / total_cost * 100) if total_cost else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🧺 Total Carpets", total_carpets)
    col2.metric("💰 Total Cost (BHD)", f"{total_cost:,.2f}")
    col3.metric("📈 Total Revenue (BHD)", f"{total_revenue:,.2f}")
    col4.metric("🏦 Profit (BHD)", f"{total_profit:,.2f}", delta_color="inverse" if total_profit < 0 else "normal")
    col5.metric("📊 Profit Margin (%)", f"{overall_margin:.2f}%", delta_color="inverse" if overall_margin < 0 else "normal")

    # Warning for negative profit
    if total_profit < 0:
        st.warning("⚠️ Overall profit is negative! Consider reviewing your selling prices.")

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
    profit_by_manufacturer = filtered_df.groupby("Carpet Origin & Manufacturer")["Profit"].sum().reset_index()
    fig_profit = px.bar(
        profit_by_manufacturer,
        x="Carpet Origin & Manufacturer",
        y="Profit",
        title="Profit by Manufacturer",
        text="Profit"
    )
    st.plotly_chart(fig_profit)

    # Download filtered data as Excel
    st.subheader("⬇️ Download Filtered Data")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        filtered_df.to_excel(writer, index=False)
    processed_data = output.getvalue()

    st.download_button(
        label="Download as Excel",
        data=processed_data,
        file_name="filtered_carpet_inventory.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
