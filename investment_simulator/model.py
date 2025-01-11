"""
Investment Portfolio Simulator - Core Model
----------------------------------------
This module implements the core Monte Carlo simulation logic for investment portfolio growth.
It provides the main simulation engine that:
- Performs individual portfolio growth simulations
- Runs multiple Monte Carlo iterations
- Collects and processes simulation statistics

The model accounts for:
- Initial investment
- Monthly contributions
- Yearly bonuses
- Variable market returns
- Compound growth

Author: [Muhammad Abdelhamid]
Date: [2025-01-11]
"""

import numpy as np
from helpers import (
    get_random_returns,
    get_confidence_levels,
    get_yearly_percentiles
)


def perform_simulation(inputs: dict):
    """
    Performs a single simulation to find portfolio value after years of growth.
    """
    years = inputs['years']
    balance = inputs['initial_investment']
    returns = get_random_returns(
        years=years,
        estimated_roi=inputs['estimated_roi'],
        volatility=inputs['volatility']
    )
    mean_return = (np.mean(returns) - 1) * 100

    history = [balance]

    for i in range(years):
        annual_return = returns[i]
        monthly_rate = (annual_return - 1) / 12

        # Monthly contributions and growth
        for _ in range(12):
            balance += inputs['monthly_contribution']
            balance *= (1 + monthly_rate)

        # Add yearly bonus
        balance += inputs['yearly_bonus']
        history.append(balance)

    return balance, history, mean_return


def perform_monte_carlo(inputs: dict, n: int = 1000):
    """Run multiple simulations and collect statistics"""
    final_balances = []
    results = []
    mean_returns = []

    for _ in range(n):
        final_balance, history, mean_return = perform_simulation(inputs)
        final_balances.append(final_balance)
        results.append(history)
        mean_returns.append(mean_return)

    lower_confidence, upper_confidence = get_confidence_levels(final_balances)
    yearly_percentiles = get_yearly_percentiles(results, inputs)

    return {
        'final_balances': final_balances,
        'results': results,
        'yearly_percentiles': yearly_percentiles,
        'lower_confidence': lower_confidence,
        'upper_confidence': upper_confidence,
        'mean_returns': mean_returns
    }
