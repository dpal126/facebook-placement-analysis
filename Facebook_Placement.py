import streamlit as st
import plotly.express as px
import pandas as pd

# Load the data
data = pd.read_excel('ad_report.xlsx')

# Step 1: Data Cleaning
# Remove rows with blank 'Placement' and select rows where 'Result type' is 'Thank You Page'
filtered_data = data.dropna(subset=['Placement'])
thank_you_data = filtered_data[filtered_data['Result type'] == 'Thank You Page']

# Step 4: Calculate the average for each metric by unique placement
avg_metrics_data = thank_you_data.groupby('Placement').agg({
    'Results': 'mean',
    'Cost per result': 'mean',
    'CTR (all)': 'mean',
    'Video average play time': 'mean'
}).reset_index()

avg_cpm_data = thank_you_data.groupby('Placement')['CPM (cost per 1,000 impressions)'].mean().reset_index()

# Streamlit app layout
st.title("Interactive Bubble Chart for Metrics vs Placement")

# Step 3: Interactive control for 'Campaign name'
# Get unique campaign names and add an 'All Campaigns' option
campaign_options = ['All Campaigns'] + list(thank_you_data['Campaign name'].dropna().unique())
selected_campaign = st.selectbox("Select Campaign", campaign_options)

# Filter data based on selected campaign
if selected_campaign == 'All Campaigns':
    plot_data = avg_metrics_data
else:
    plot_data = thank_you_data[thank_you_data['Campaign name'] == selected_campaign]

# Function to create bubble charts with uniform bubble sizes
def create_uniform_bubble_chart(data, x_col, y_col, title, color):
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        size=[20]*len(data),  # Uniform bubble size
        color_discrete_sequence=[color],
        title=title,
        labels={y_col: y_col.replace(' (cost per 1,000 impressions)', '')}
    )
    return fig

# Create bubble charts for each specified column vs 'Placement' with uniform bubble sizes
charts = []

# Results vs Placement
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Results', 'Average Results vs Placement', 'blue'))

# Cost per result vs Placement
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Cost per result', 'Average Cost per Result vs Placement', 'green'))

# CTR (all) vs Placement
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'CTR (all)', 'Average CTR (all) vs Placement', 'red'))

# Video average play time vs Placement
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Video average play time', 'Average Video Average Play Time vs Placement', 'purple'))

# Average CPM vs Placement
charts.append(create_uniform_bubble_chart(avg_cpm_data, 'Placement', 'CPM (cost per 1,000 impressions)', 'Average CPM vs Placement', 'orange'))

# Display the charts
for chart in charts:
    st.plotly_chart(chart)
