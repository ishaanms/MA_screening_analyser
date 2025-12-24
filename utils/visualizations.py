"""
Visualization utilities for M&A analysis dashboard
"""

import plotly.graph_objects as go
import plotly.express as px


def create_radar_chart(dimensions_data):
    """
    Create radar chart for 5 strategic dimensions
    
    Args:
        dimensions_data: dict with dimension scores
    
    Returns:
        plotly figure
    """
    # Extract dimension names and scores
    dimensions = {
        'technology_synergy': 'Technology Synergy',
        'market_overlap': 'Market Overlap',
        'product_complementarity': 'Product Complementarity',
        'cultural_alignment': 'Cultural Alignment',
        'financial_health': 'Financial Health'
    }
    
    categories = []
    scores = []
    
    for key, label in dimensions.items():
        if key in dimensions_data:
            categories.append(label)
            scores.append(dimensions_data[key].get('score', 0))
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 128, 96, 0.2)',  # Shopify green with transparency
        line=dict(color='#008060', width=2),
        marker=dict(size=8, color='#008060'),
        name='Strategic Fit'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color='#FFFFFF')
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_gauge_chart(overall_score, recommendation):
    """
    Create gauge chart for overall fit score
    
    Args:
        overall_score: numeric score 0-100
        recommendation: text recommendation
    
    Returns:
        plotly figure
    """
    # Determine color based on score
    if overall_score >= 80:
        color = "#50B83C"  # Green
    elif overall_score >= 60:
        color = "#FFC453"  # Yellow
    elif overall_score >= 40:
        color = "#FF8C42"  # Orange
    else:
        color = "#E32C2B"  # Red
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Strategic Fit", 'font': {'size': 20, 'color': '#FFFFFF'}},
        number={'font': {'size': 50, 'color': color}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#FFE6E6'},
                {'range': [40, 60], 'color': '#FFF4E6'},
                {'range': [60, 80], 'color': '#FFFAE6'},
                {'range': [80, 100], 'color': '#E6F4EA'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_dimension_bar_chart(dimensions_data):
    """
    Create horizontal bar chart for dimension scores
    
    Args:
        dimensions_data: dict with dimension scores
    
    Returns:
        plotly figure
    """
    dimensions = {
        'technology_synergy': 'Technology Synergy',
        'market_overlap': 'Market Overlap',
        'product_complementarity': 'Product Complementarity',
        'cultural_alignment': 'Cultural Alignment',
        'financial_health': 'Financial Health'
    }
    
    categories = []
    scores = []
    colors = []
    
    for key, label in dimensions.items():
        if key in dimensions_data:
            score = dimensions_data[key].get('score', 0)
            categories.append(label)
            scores.append(score)
            
            # Color based on score
            if score >= 75:
                colors.append('#50B83C')
            elif score >= 60:
                colors.append('#FFC453')
            else:
                colors.append('#FF8C42')
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker=dict(color=colors),
        text=scores,
        textposition='outside',
        textfont=dict(size=12, color='#333')
    ))
    
    fig.update_layout(
        xaxis=dict(range=[0, 100], title="Score", gridcolor='lightgray'),
        yaxis=dict(title=""),
        height=300,
        margin=dict(l=20, r=20, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def get_recommendation_color(recommendation):
    """Get color for recommendation badge"""
    colors = {
        "Strong Fit": "#50B83C",
        "Moderate Fit": "#FFC453",
        "Weak Fit": "#FF8C42",
        "Poor Fit": "#E32C2B"
    }
    return colors.get(recommendation, "#999999")


def get_recommendation_emoji(recommendation):
    """Get emoji for recommendation"""
    emojis = {
        "Strong Fit": "✅",
        "Moderate Fit": "⚠️",
        "Weak Fit": "⚡",
        "Poor Fit": "❌"
    }
    return emojis.get(recommendation, "ℹ️")
