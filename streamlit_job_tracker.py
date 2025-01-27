import streamlit as st
import pandas as pd
import plotly.express as px

# Load job applications data from a CSV file
try:
    df = pd.read_csv("job_applications.csv")
    
    # Check if required columns exist
    required_columns = {"Job Title", "Company", "Date Applied", "Status"}
    if not required_columns.issubset(df.columns):
        raise ValueError("The CSV file is missing required columns. Expected columns: " + ", ".join(required_columns))
except FileNotFoundError:
    st.error("The file 'job_applications.csv' was not found. Please ensure the file exists in the directory.")
    st.stop()
except PermissionError:
    st.error("Permission denied while trying to read 'job_applications.csv'. Please check file permissions.")
    st.stop()
except ValueError as ve:
    st.error(f"Error in file format: {ve}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.stop()

# Streamlit app
st.title("Job Applications Tracker")

# Filter options
status_filter = st.multiselect(
    "Filter by Application Status",
    options=df["Status"].unique(),
    default=df["Status"].unique()
)
filtered_df = df[df["Status"].isin(status_filter)]

# Display filtered data
st.write("### Filtered Job Applications", filtered_df)

# Count the statuses for the filtered data
status_counts = filtered_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

# Ensure the bar chart has data
if not status_counts.empty:
    # Create a Plotly bar chart with a dark theme
    fig_bar = px.bar(
        status_counts,
        x="Status",
        y="Count",
        color="Status",
        title="Job Applications by Status",
        labels={"Status": "Application Status", "Count": "Count"},
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        template="plotly_dark"
    )

    # Display the bar chart
    st.plotly_chart(fig_bar)
else:
    st.write("No data available for the selected filters.")

# Ghost job explanation
st.caption("Suspected ghost jobs are a posted job listing with no intention to hire, often used for appearances or candidate harvesting.")