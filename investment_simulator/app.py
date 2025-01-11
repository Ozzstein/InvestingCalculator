"""
Investment Portfolio Simulator - Streamlit Web Application
-----------------------------------------------------
This module implements the web interface for the Monte Carlo investment simulator.
It provides an interactive interface for users to:
- Input investment parameters
- View simulation results
- Explore different investment scenarios

Uses Streamlit for the web interface and interactive components.

Author: [Muhammad Abdelhamid]
Date: [2025-01-11]
"""

import streamlit as st
from model import perform_monte_carlo
from plots import create_simulation_plots


def format_currency(value: float) -> str:
    """Format number as currency string"""
    return f"€{value:,.0f}"


def format_percent(value: float) -> str:
    """Format number as percentage string"""
    return f"{value:.1f}%"


def get_user_inputs():
    """Collect user inputs for simulation parameters"""
    st.sidebar.header("Investment Parameters")

    inputs = {}

    # Simulation settings
    inputs['num_simulations'] = st.sidebar.number_input(
        "Number of Simulations",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        format="%d",
        help="More simulations provide more accurate results but take longer to compute"
    )

    st.sidebar.markdown("---")  # Add a separator

    # Investment amounts
    inputs['initial_investment'] = st.sidebar.number_input(
        "Initial Investment (€)",
        min_value=0,
        value=50000,
        step=1000,
        format="%d"
    )

    inputs['monthly_contribution'] = st.sidebar.number_input(
        "Monthly Contribution (€)",
        min_value=0,
        value=1000,
        step=100,
        format="%d"
    )

    inputs['yearly_bonus'] = st.sidebar.number_input(
        "Yearly Bonus (€)",
        min_value=0,
        value=5000,
        step=1000,
        format="%d"
    )

    # Time horizon and returns
    inputs['years'] = st.sidebar.number_input(
        "Investment Period (Years)",
        min_value=1,
        max_value=50,
        value=20,
        step=1,
        format="%d"
    )

    inputs['estimated_roi'] = st.sidebar.number_input(
        "Estimated Annual Return (%)",
        min_value=0,
        max_value=30,
        value=8,
        step=1,
        format="%d"
    ) / 100  # Convert to decimal

    # Optional volatility input
    inputs['volatility'] = st.sidebar.number_input(
        "Market Volatility (%)",
        min_value=5,
        max_value=50,
        value=15,
        step=1,
        format="%d"
    ) / 100  # Convert to decimal

    return inputs


def display_statistics(results: dict, inputs: dict):
    """Display key statistics from simulation results"""
    st.header("Investment Statistics")

    # Calculate total investment
    total_invested = (inputs['initial_investment'] +
                      (inputs['monthly_contribution'] * 12 +
                      inputs['yearly_bonus']) * inputs['years'])

    # Create two columns for statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Invested", format_currency(total_invested))
        st.metric("Median Final Balance",
                  format_currency(results['yearly_percentiles']['median'].iloc[-1]))
        st.metric("Average Return",
                  format_percent(sum(results['mean_returns']) / len(results['mean_returns'])))

    with col2:
        st.metric("95th Percentile",
                  format_currency(results['yearly_percentiles']['95th'].iloc[-1]))
        st.metric("5th Percentile",
                  format_currency(results['yearly_percentiles']['5th'].iloc[-1]))
        confidence_range = format_currency(results['lower_confidence']) + " to " + \
            format_currency(results['upper_confidence'])
        st.metric("95% Confidence Range", confidence_range)

    # Add Safe Withdrawal section
    st.subheader("Safe Withdrawal")

    # Calculate safe withdrawal amounts (using 4% rule)
    median_balance = results['yearly_percentiles']['median'].iloc[-1]
    safe_withdrawal_rate = 0.04  # 4% rule

    yearly_withdrawal = median_balance * safe_withdrawal_rate
    monthly_withdrawal = yearly_withdrawal / 12

    # Create two columns for withdrawal rates
    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Maximum Monthly Withdrawal",
            format_currency(monthly_withdrawal),
            help="Based on the 4% rule - a widely used guideline for retirement withdrawals"
        )

    with col4:
        st.metric(
            "Maximum Yearly Withdrawal",
            format_currency(yearly_withdrawal),
            help="4% of your median final balance - adjust based on your risk tolerance and market conditions"
        )

    # Add explanatory note about safe withdrawal
    st.markdown("""
    ℹ️ **Safe Withdrawal Notes:**
    - The 4% rule suggests withdrawing 4% of your portfolio in the first year of retirement
    - This rate is designed to provide steady income while maintaining portfolio value
    - Actual safe withdrawal rates may vary based on market conditions and life expectancy
    - Consider consulting a financial advisor for personalized withdrawal strategies
    """)


def main():
    # Set page config and custom CSS for fonts
    st.set_page_config(
        page_title="Investment Portfolio Simulator",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add custom CSS to use Atkinson Hyperlegible font
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
        
        /* Target all elements */
        * {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        
        /* Target Streamlit specific elements */
        .stApp, .stMarkdown, .stText, .stTitle, .stHeader, 
        .stAlert, .stDataFrame, .stTable, .stMetric, 
        .stNumberInput, .stSelectbox, .stSidebar, 
        .stButton, .stRadio, .stCheckbox, .stTextInput,
        .stProgress, .stDownloadButton, .stFileUploader,
        .stMultiSelect, .stTextArea, .stDateInput, .stTimeInput,
        .stColorPicker, div[data-testid="stToolbar"] {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        
        /* Target metric values and labels */
        .stMetric label, .stMetric .css-1wivap2, 
        .stMetric [data-testid="stMetricValue"], 
        .stMetric [data-testid="stMetricDelta"] {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        
        /* Target headers and titles */
        h1, h2, h3, h4, h5, h6, .css-10trblm, .css-1q8dd3e {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        
        /* Target sidebar elements */
        .css-1d391kg, .css-1v0mbdj {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        
        /* Target input labels and values */
        .css-81oif8, .css-qrbaxs {
            font-family: 'Atkinson Hyperlegible', sans-serif !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Investment Portfolio Simulator")

    # Get user inputs
    inputs = get_user_inputs()

    # Run simulation with user-specified number of simulations
    results = perform_monte_carlo(inputs, n=inputs['num_simulations'])

    # Create and display plots
    fig = create_simulation_plots(results, inputs)
    st.plotly_chart(fig, use_container_width=True)

    # Display statistics
    display_statistics(results, inputs)

    # Add explanatory notes
    st.markdown("""
    ### Notes:
    - Simulations use historical market patterns to generate random returns
    - Returns follow a weighted distribution favoring moderate outcomes
    - The 95% confidence range represents the most likely outcomes
    - Past performance does not guarantee future results
    """)


if __name__ == "__main__":
    main()
