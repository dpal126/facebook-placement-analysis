import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load the data
data = pd.read_excel('ad_report.xlsx')

# Step 1: Data Cleaning
# Remove rows with blank 'Placement' and select rows where 'Result type' is 'Thank You Page'
filtered_data = data.dropna(subset=['Placement'])
thank_you_data = filtered_data[filtered_data['Result type'] == 'Thank You Page']

# Step 2: Calculate the average CPM for unique placements
avg_cpm_data = thank_you_data.groupby('Placement')['CPM (cost per 1,000 impressions)'].mean().reset_index()

# Step 3: Create a bubble chart for average CPM vs Placement
fig = px.scatter(
    avg_cpm_data,
    x='Placement',
    y='CPM (cost per 1,000 impressions)',
    size='CPM (cost per 1,000 impressions)',
    title="Bubble Chart for Average CPM vs Placement",
    labels={'CPM (cost per 1,000 impressions)': 'CPM'},
    size_max=60
)

# Show the plot
fig.show()

# Step 4: Calculate the average for each metric by unique placement
avg_metrics_data = thank_you_data.groupby('Placement').agg({
    'Results': 'mean',
    'Cost per result': 'mean',
    'CTR (all)': 'mean',
    'Video average play time': 'mean'
}).reset_index()

# Define a function to create bubble charts with uniform bubble sizes
def create_uniform_bubble_chart(data, x_col, y_col, title, color):
    fig = go.Figure()

    # Add scatter plot with uniform bubble size
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='markers',
        marker=dict(
            size=20,  # Uniform bubble size
            color=color,  # Set bubble color
            opacity=0.6,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        name=y_col
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True
    )

    return fig

# Step 5: Create bubble charts for each specified column vs 'Placement' with uniform bubble sizes
uniform_charts = []

# Results vs Placement
uniform_charts.append(create_uniform_bubble_chart(avg_metrics_data, 'Placement', 'Results', 'Average Results vs Placement', 'blue'))

# Cost per result vs Placement
uniform_charts.append(create_uniform_bubble_chart(avg_metrics_data, 'Placement', 'Cost per result', 'Average Cost per Result vs Placement', 'green'))

# CTR (all) vs Placement
uniform_charts.append(create_uniform_bubble_chart(avg_metrics_data, 'Placement', 'CTR (all)', 'Average CTR (all) vs Placement', 'red'))

# Video average play time vs Placement
uniform_charts.append(create_uniform_bubble_chart(avg_metrics_data, 'Placement', 'Video average play time', 'Average Video Average Play Time vs Placement', 'purple'))

# Add Average CPM vs Placement to the charts
uniform_charts.append(create_uniform_bubble_chart(avg_cpm_data, 'Placement', 'CPM (cost per 1,000 impressions)', 'Average CPM vs Placement', 'orange'))

# Step 6: Display the charts
for chart in uniform_charts:
    chart.show()
