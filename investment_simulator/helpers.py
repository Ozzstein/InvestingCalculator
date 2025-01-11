"""
Investment Portfolio Simulator - Helper Functions
----------------------------------------------
This module contains utility functions for the Monte Carlo simulation results.
It provides functions for:
- Generating random returns based on estimated ROI and volatility
- Calculating confidence intervals
- Computing yearly percentiles and statistics

Author: [Muhammad Abdelhamid]
Date: [2025-01-11]
"""

import random
import numpy as np
import pandas as pd


def get_random_returns(years: int, estimated_roi: float, volatility: float = 0.15):
    """
    Generates random returns based on estimated ROI and volatility.

    Args:
        years: Number of years to simulate
        estimated_roi: Expected average annual return (as decimal, e.g., 0.08 for 8%)
        volatility: Standard deviation of returns (default 15%)
    """
    # Generate random returns using normal distribution
    returns = np.random.normal(
        loc=estimated_roi,
        scale=volatility,
        size=years
    )

    # Convert to return multipliers (e.g., 0.08 -> 1.08)
    return returns + 1


def get_confidence_levels(final_balances):
    """Calculate confidence intervals for final balances"""
    upper_confidence = np.percentile(final_balances, 97.5)
    lower_confidence = np.percentile(final_balances, 2.5)
    return lower_confidence, upper_confidence


def get_yearly_percentiles(results, inputs) -> pd.DataFrame:
    """Calculate yearly percentiles for all simulations"""
    results_rotated = list(zip(*results))

    year = []
    percentiles = {
        '95th': [],
        '75th': [],
        'median': [],
        '25th': [],
        '5th': [],
        'invested': []
    }

    for i, year_results in enumerate(results_rotated):
        year.append(i)
        percentiles['95th'].append(np.percentile(year_results, 95))
        percentiles['75th'].append(np.percentile(year_results, 75))
        percentiles['median'].append(np.percentile(year_results, 50))
        percentiles['25th'].append(np.percentile(year_results, 25))
        percentiles['5th'].append(np.percentile(year_results, 5))
        percentiles['invested'].append(
            inputs['initial_investment'] +
            (inputs['monthly_contribution'] * 12 + inputs['yearly_bonus']) * i
        )

    return pd.DataFrame({
        'year': year,
        **percentiles
    })
