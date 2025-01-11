# Investment Calculator

A sophisticated investment calculator built with Python and Streamlit that helps users analyze and visualize investment scenarios using Monte Carlo simulations.

## Features

- Investment growth simulation with variable returns
- Monte Carlo analysis for risk assessment
- Interactive visualizations including:
  - Portfolio growth projections
  - Distribution of final balances
  - Safe withdrawal analysis
- Customizable parameters:
  - Initial investment
  - Monthly contributions
  - Investment timeframe
  - Expected return rates and volatility
- Safe withdrawal calculations based on the 4% rule
- Modern UI with Atkinson Hyperlegible font for improved readability

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser, where you can:

1. Input your investment parameters
2. View interactive visualizations
3. Analyze different investment scenarios
4. Calculate safe withdrawal rates

## Project Structure

- `app.py` - Main Streamlit application
- `model.py` - Core investment calculation logic
- `helpers.py` - Utility functions
- `plots.py` - Visualization functions

## Dependencies

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly

## Currency

All monetary values are displayed in Euros (€).

## License

This project is open source and available under the MIT License.
