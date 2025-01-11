"""
Investment Portfolio Simulator - Plotting Functions
-----------------------------------------------
This module handles all visualization aspects of the Monte Carlo simulation results.
It provides functions to create:
- Investment growth scenarios plot
- Return distribution histogram
- Final balance distribution
- Monthly growth analysis

Uses Plotly for interactive visualizations with a dark theme optimized for web display.

Author: [Muhammad Abdelhamid]
Date: [2025-01-11]
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Color scheme for dark theme
COLORS = {
    'best': '#4ade80',    # Bright green
    'median': '#60a5fa',  # Bright blue
    'worst': '#f87171',   # Bright red
    'background': '#475569',  # Light slate for background paths
    'invested': '#e2e8f0',  # Light slate for invested line
    'grid': '#334155',    # Darker slate for grid
    'text': '#f1f5f9',    # Very light slate for text
    'plot_bg': '#1e293b',  # Dark slate blue background
    'paper_bg': '#0f172a',  # Darker background for the figure
    'annotation': '#94a3b8'  # Slate for annotations
}


def create_simulation_plots(simulation_results: dict, inputs: dict):
    """Creates a figure with four subplots showing different aspects of the simulation"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "<b>Investment Growth Scenarios</b>",
            "<b>Distribution of Annual Returns</b>",
            "<b>Distribution of Final Balances</b>",
            "<b>Monthly Growth Analysis</b>"
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )

    # Add investment growth plot
    _add_growth_plot(fig, simulation_results, inputs)

    # Add returns distribution
    _add_returns_dist(fig, simulation_results['mean_returns'])

    # Add final balance distribution
    _add_balance_dist(fig, simulation_results['final_balances'])

    # Add monthly growth analysis
    _add_monthly_analysis(fig, simulation_results['results'])

    # Update layout with dark theme
    _update_layout(fig)

    return fig


def _add_growth_plot(fig, simulation_results, inputs):
    """Add investment growth scenarios plot"""
    # Plot background simulations
    num_background_sims = 10
    background_alpha = 0.3

    results = simulation_results['results']
    random_indices = np.random.choice(
        len(results),
        num_background_sims,
        replace=False
    )

    # Plot background simulations
    for idx in random_indices:
        sim_data = results[idx]
        fig.add_trace(
            go.Scatter(
                x=list(range(len(sim_data))),
                y=sim_data,
                name="Simulation Path",
                line=dict(
                    color='rgba(148, 163, 184, 0.8)',
                    width=1,
                    shape='spline'
                ),
                opacity=background_alpha,
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )

    # Plot percentile lines
    percentiles = simulation_results['yearly_percentiles']
    fig.add_trace(
        go.Scatter(
            x=percentiles['year'],
            y=percentiles['95th'],
            name="95th Percentile",
            line=dict(color=COLORS['best'], width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=percentiles['year'],
            y=percentiles['median'],
            name="Median",
            line=dict(color=COLORS['median'], width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=percentiles['year'],
            y=percentiles['5th'],
            name="5th Percentile",
            line=dict(color=COLORS['worst'], width=2)
        ),
        row=1, col=1
    )

    # Add total invested line
    fig.add_trace(
        go.Scatter(
            x=percentiles['year'],
            y=percentiles['invested'],
            name="Total Invested",
            line=dict(
                color=COLORS['invested'],
                dash='dash',
                width=2
            )
        ),
        row=1, col=1
    )


def _add_returns_dist(fig, returns):
    """Add returns distribution histogram"""
    fig.add_trace(
        go.Histogram(
            x=returns,
            name="Returns Distribution",
            nbinsx=50,
            marker=dict(
                color=COLORS['median'],
                opacity=0.75,
                line=dict(color='white', width=0.5)
            ),
            histnorm='probability density'
        ),
        row=1, col=2
    )


def _add_balance_dist(fig, balances):
    """Add final balance distribution histogram with key statistics"""
    # Calculate key statistics
    median = np.median(balances)
    lower_conf = np.percentile(balances, 2.5)
    upper_conf = np.percentile(balances, 97.5)

    # Add histogram
    fig.add_trace(
        go.Histogram(
            x=balances,
            name="Final Balance Distribution",
            nbinsx=50,
            marker=dict(
                color=COLORS['best'],
                opacity=0.75,
                line=dict(color='white', width=0.5)
            ),
            histnorm='probability density'
        ),
        row=2, col=1
    )

    # Add vertical lines for key statistics
    fig.add_vline(
        x=median,
        line=dict(
            color=COLORS['median'],
            width=2,
            dash='solid'
        ),
        annotation=dict(
            text="Median",
            font=dict(
                family="Atkinson Hyperlegible",
                size=12,
                color=COLORS['text']
            ),
            yanchor="bottom"
        ),
        row=2, col=1
    )

    # Add confidence interval lines
    fig.add_vline(
        x=lower_conf,
        line=dict(
            color=COLORS['annotation'],
            width=2,
            dash='dash'
        ),
        annotation=dict(
            text="95% CI",
            font=dict(
                family="Atkinson Hyperlegible",
                size=12,
                color=COLORS['text']
            ),
            yanchor="bottom"
        ),
        row=2, col=1
    )

    fig.add_vline(
        x=upper_conf,
        line=dict(
            color=COLORS['annotation'],
            width=2,
            dash='dash'
        ),
        row=2, col=1
    )


def _add_monthly_analysis(fig, results):
    """Add monthly growth analysis"""
    monthly_growth = _calculate_monthly_growth(results)

    fig.add_trace(
        go.Bar(
            x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y=monthly_growth,
            name="Average Monthly Growth",
            marker=dict(
                color=COLORS['worst'],
                opacity=0.75,
                line=dict(color='white', width=1)
            )
        ),
        row=2, col=2
    )


def _calculate_monthly_growth(results):
    """Calculate average monthly growth rates"""
    monthly_values = [[] for _ in range(12)]

    for sim in results:
        for year in range(len(sim)-1):
            for month in range(12):
                if year * 12 + month < len(sim) - 1:
                    growth = ((sim[year * 12 + month + 1] - sim[year * 12 + month]) /
                              sim[year * 12 + month] * 100)
                    monthly_values[month].append(growth)

    return [np.mean(month) for month in monthly_values]


def _update_layout(fig):
    """Update figure layout with dark theme styling"""
    fig.update_layout(
        height=900,
        width=1000,
        showlegend=True,
        title=dict(
            text="<b>Investment Portfolio Growth Simulation</b>",
            font=dict(
                family="Atkinson Hyperlegible",
                size=24,
                color=COLORS['text']
            ),
            y=0.95
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(241, 245, 249, 0.2)',
            borderwidth=1,
            font=dict(
                family="Atkinson Hyperlegible",
                color=COLORS['text']
            )
        ),
        plot_bgcolor=COLORS['plot_bg'],
        paper_bgcolor=COLORS['paper_bg'],
        font=dict(
            family="Atkinson Hyperlegible",
            size=12,
            color=COLORS['text']
        )
    )

    # Update axes styling
    _update_axes_styling(fig)


def _update_axes_styling(fig):
    """Update axes styling for all subplots"""
    axes_titles = [
        ("Portfolio Value (€)", "Years"),
        ("Count", "Annual Return (%)"),
        ("Count", "Final Balance (€)"),
        ("Growth Rate (%)", "Month")
    ]

    for i, (yaxis, xaxis) in enumerate(axes_titles):
        row = (i // 2) + 1
        col = (i % 2) + 1

        fig.update_xaxes(
            title=dict(
                text=xaxis,
                font=dict(
                    family="Atkinson Hyperlegible",
                    size=14,
                    color=COLORS['text']
                )
            ),
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            row=row,
            col=col,
            tickfont=dict(
                family="Atkinson Hyperlegible",
                color=COLORS['text']
            )
        )

        fig.update_yaxes(
            title=dict(
                text=yaxis,
                font=dict(
                    family="Atkinson Hyperlegible",
                    size=14,
                    color=COLORS['text']
                )
            ),
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORS['grid'],
            zeroline=False,
            row=row,
            col=col,
            tickfont=dict(
                family="Atkinson Hyperlegible",
                color=COLORS['text']
            )
        )

        # Add currency formatting for relevant axes
        if "(€)" in yaxis or "(€)" in xaxis:
            if "(€)" in yaxis:
                fig.update_yaxes(tickformat="€,.0f", row=row, col=col)
            if "(€)" in xaxis:
                fig.update_xaxes(tickformat="€,.0f", row=row, col=col)
