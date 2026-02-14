import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="Gas Station Dashboard", layout="wide")

st.title("🚦 Gas Station Dashboard")

st.write("""
Monitor Fuel Service and Uniform Compliance from one unified dashboard.
""")

# ======================================================
# Create Tabs
# ======================================================
tab1, tab2 = st.tabs(["⛽ Fuel Service", "👕 Uniform Service"])


# ======================================================
# ⛽ TAB 1 — Fuel Service
# ======================================================
with tab1:

    st.subheader("📊 Fuel Service Overview")

    camera_list = ["Camera2", "Camera13", "Camera17"]
    overview_data = []

    for cam in camera_list:
        summary_csv = os.path.join("outputs", f"{cam}_summary.csv")
        if os.path.exists(summary_csv):
            df = pd.read_csv(summary_csv)
            total_cars = df["cars_served"].sum() if "cars_served" in df.columns else 0
            avg_wait = round(df["average_wait_time_sec"].mean(), 2) if "average_wait_time_sec" in df.columns else 0
            overview_data.append({
                "Camera": cam,
                "Total Cars": total_cars,
                "Average Wait (sec)": avg_wait
            })

    if overview_data:
        df_overview = pd.DataFrame(overview_data)
        st.table(df_overview)

        st.subheader("📈 Fuel Analysis")

        chart_cars = alt.Chart(df_overview).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x="Camera:N",
            y="Total Cars:Q",
            color=alt.Color("Camera:N", legend=None),
            tooltip=["Camera", "Total Cars"]
        ).properties(width=700, height=400, title="🚗 Total Cars per Camera")

        chart_wait = alt.Chart(df_overview).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x="Camera:N",
            y="Average Wait (sec):Q",
            color=alt.Color("Camera:N", legend=None),
            tooltip=["Camera", "Average Wait (sec)"]
        ).properties(width=700, height=400, title="⏱️ Average Wait Time per Camera")

        st.altair_chart(chart_cars, use_container_width=True)
        st.altair_chart(chart_wait, use_container_width=True)

    else:
        st.info("No fuel service data available yet.")

# ======================================================
# 👕 TAB 2 — Uniform Service
# ======================================================
with tab2:
    st.subheader("📊 Uniform Compliance Overview")
    import altair as alt
    import os
    import pandas as pd

    camera_list = ["Camera2", "Camera13", "Camera17"]
    overview_data = []

    for cam in camera_list:
        summary_csv = os.path.join("outputs", f"{cam}_uniform_summary.csv")
        if os.path.exists(summary_csv):
            df = pd.read_csv(summary_csv)
            total_people = df["total_person"].sum() if "total_person" in df.columns else 0
            total_uniform = df["total_uniform"].sum() if "total_uniform" in df.columns else 0
            compliance_rate = round((total_uniform / total_people) * 100, 2) if total_people > 0 else 0
            overview_data.append({
                "Camera": cam,
                "Total People": total_people,
                "Uniform Detected": total_uniform,
                "Compliance (%)": compliance_rate,
                "Non-compliant": total_people - total_uniform
            })

    if overview_data:
        df_overview = pd.DataFrame(overview_data)

        # -----------------------------
        # جدول شامل
        # -----------------------------
        st.subheader("📄 Uniform Compliance Table")
        st.dataframe(df_overview, use_container_width=True)

        # -----------------------------
        # Bar chart: Compliance %
        # -----------------------------
        st.subheader("📈 Compliance Rate per Camera")
        chart_compliance = alt.Chart(df_overview).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X("Camera:N", title="Camera"),
            y=alt.Y("Compliance (%):Q", title="Compliance (%)"),
            color=alt.Color("Camera:N", legend=None),
            tooltip=["Camera", "Compliance (%)"]
        ).properties(width=700, height=400)
        st.altair_chart(chart_compliance, use_container_width=True)

        # -----------------------------
        # Bar chart: Total People
        # -----------------------------
        st.subheader("👥 Total People per Camera")
        chart_people = alt.Chart(df_overview).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X("Camera:N", title="Camera"),
            y=alt.Y("Total People:Q", title="Total People"),
            color=alt.Color("Camera:N", legend=None),
            tooltip=["Camera", "Total People", "Uniform Detected", "Non-compliant"]
        ).properties(width=700, height=400)
        st.altair_chart(chart_people, use_container_width=True)

        # -----------------------------
        # Pie chart: الالتزام مقابل عدم الالتزام
        # -----------------------------
        st.subheader("📊 Compliance vs Non-compliance per Camera")
        for cam in camera_list:
            cam_data = df_overview[df_overview["Camera"] == cam]
            if not cam_data.empty:
                compliance = int(cam_data["Uniform Detected"])
                non_compliance = int(cam_data["Non-compliant"])
                pie_df = pd.DataFrame({
                    "Status": ["Compliant", "Non-compliant"],
                    "Count": [compliance, non_compliance]
                })
                pie_chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Count", type="quantitative"),
                    color=alt.Color(field="Status", type="nominal", scale=alt.Scale(range=["green", "red"])),
                    tooltip=["Status", "Count"]
                ).properties(title=f"{cam} Compliance Distribution")
                st.altair_chart(pie_chart, use_container_width=True)
    else:
        st.info("No uniform data available yet.")