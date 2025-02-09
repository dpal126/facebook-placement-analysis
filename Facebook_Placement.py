import streamlit as st
import plotly.express as px
import pandas as pd

# Load the data
data = pd.read_excel('ad_report.xlsx')

# Data cleaning and processing steps...

# Streamlit app layout
st.title("Interactive Bubble Chart for Metrics vs Placement")

# Interactive control for 'Campaign name'
campaign_options = ['All Campaigns'] + list(data['Campaign name'].dropna().unique())
selected_campaign = st.selectbox("Select Campaign", campaign_options)

# Filter data based on selected campaign
if selected_campaign == 'All Campaigns':
    plot_data = data  # or your processed data
else:
    plot_data = data[data['Campaign name'] == selected_campaign]

# Function to create bubble charts
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

# Create and display bubble charts
charts = []
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Results', 'Average Results vs Placement', 'blue'))
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Cost per result', 'Average Cost per Result vs Placement', 'green'))
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'CTR (all)', 'Average CTR (all) vs Placement', 'red'))
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'Video average play time', 'Average Video Average Play Time vs Placement', 'purple'))
charts.append(create_uniform_bubble_chart(plot_data, 'Placement', 'CPM (cost per 1,000 impressions)', 'Average CPM vs Placement', 'orange'))

for chart in charts:
    st.plotly_chart(chart)
