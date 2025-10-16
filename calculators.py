"""
Calculation modules for the Redeployable Value Dashboard
All core business logic for different stakeholder value calculations
"""

import numpy as np
from typing import Dict, List, Tuple


def generate_hvac_load_profile(hvac_consumption: float, hvac_peak_time: int, hvac_load_shape: int) -> List[float]:
    """
    Generate a 24-hour HVAC load profile using a Gaussian distribution.

    Args:
        hvac_consumption: Peak HVAC consumption in kW
        hvac_peak_time: Hour of day when peak occurs (0-23)
        hvac_load_shape: Shape parameter (1-10), higher = more peaky

    Returns:
        List of 24 hourly usage values in kWh
    """
    spread = 11 - hvac_load_shape
    hourly_usage = []

    for hour in range(24):
        profile = np.exp(-((hour - hvac_peak_time) ** 2) / (2 * (spread**2)))
        usage = profile * hvac_consumption
        hourly_usage.append(usage)

    return hourly_usage


def calculate_hourly_rates(
    pricing_model: str,
    peak_rate: float = 0.28,
    off_peak_rate: float = 0.12,
    peak_start: int = 14,
    peak_end: int = 19,
    hourly_prices: List[float] = None,
) -> List[float]:
    """
    Calculate hourly electricity rates based on pricing model.

    Args:
        pricing_model: 'tou' or 'rtp'
        peak_rate: TOU peak rate ($/kWh)
        off_peak_rate: TOU off-peak rate ($/kWh)
        peak_start: Start hour of peak period
        peak_end: End hour of peak period
        hourly_prices: List of 24 hourly prices for RTP model

    Returns:
        List of 24 hourly rates
    """
    if pricing_model == "rtp" and hourly_prices:
        # Ensure we have 24 prices
        if len(hourly_prices) < 24:
            last_price = hourly_prices[-1] if hourly_prices else 0
            hourly_prices.extend([last_price] * (24 - len(hourly_prices)))
        return hourly_prices[:24]

    # TOU model
    rates = []
    for hour in range(24):
        if peak_start <= hour < peak_end:
            rates.append(peak_rate)
        else:
            rates.append(off_peak_rate)
    return rates


def optimize_battery_dispatch(
    hvac_usage: List[float],
    rates: List[float],
    battery_capacity: float,
    min_soc: float,
    max_soc: float,
    discharge_duration: int,
    battery_power: float,
    battery_efficiency: float,
) -> Dict:
    """
    Optimize battery charging and discharging schedule.

    Args:
        hvac_usage: 24-hour HVAC usage profile (kWh)
        rates: 24-hour electricity rates ($/kWh)
        battery_capacity: Usable battery capacity (kWh)
        min_soc: Minimum state of charge (0-1)
        max_soc: Maximum state of charge (0-1)
        discharge_duration: Number of hours to discharge
        battery_power: Max charge/discharge power (kW)
        battery_efficiency: Round-trip efficiency (0-1)

    Returns:
        Dictionary with charge_plan, discharge_plan, and costs
    """
    effective_capacity = battery_capacity * (max_soc - min_soc)

    # Find highest-price hours for discharging
    prices_with_hours = [(rate, hour) for hour, rate in enumerate(rates)]
    prices_with_hours.sort(reverse=True)
    discharge_hours = [hour for _, hour in prices_with_hours[:discharge_duration]]

    # Calculate energy needed for discharge hours
    energy_needed = sum(hvac_usage[hour] for hour in discharge_hours)

    # Determine energy to store (limited by capacity)
    energy_to_store = min(energy_needed, effective_capacity)
    energy_to_charge = energy_to_store / battery_efficiency

    # Find lowest-price hours for charging
    prices_with_hours.sort()
    charge_plan = [0.0] * 24
    remaining_charge = energy_to_charge

    for rate, hour in prices_with_hours:
        if remaining_charge > 0:
            can_charge = min(remaining_charge, battery_power)
            charge_plan[hour] = can_charge
            remaining_charge -= can_charge
        else:
            break

    # Discharge planning
    discharge_plan = [0.0] * 24
    energy_stored = energy_to_store

    for hour in discharge_hours:
        if energy_stored > 0:
            discharge_amount = min(hvac_usage[hour], energy_stored, battery_power)
            discharge_plan[hour] = discharge_amount
            energy_stored -= discharge_amount

    return {"charge_plan": charge_plan, "discharge_plan": discharge_plan, "energy_stored": energy_to_store}


def calculate_homeowner_savings(params: Dict) -> Dict:
    """
    Calculate homeowner savings from battery system.

    Args:
        params: Dictionary containing all input parameters

    Returns:
        Dictionary with daily savings, costs breakdown, and hourly data
    """
    # Extract parameters with defaults
    pricing_model = params.get("pricingModel", "tou")
    peak_rate = params.get("peakRate", 0.28)
    off_peak_rate = params.get("offPeakRate", 0.12)
    peak_start = params.get("peakStart", 14)
    peak_end = params.get("peakEnd", 19)
    hourly_prices = params.get("hourlyPrices", [])

    hvac_consumption = params.get("hvacConsumption", 3.5)
    hvac_peak_time = params.get("hvacPeakTime", 16)
    hvac_load_shape = params.get("hvacLoadShape", 5)

    battery_capacity = params.get("batteryCapacity", 10)
    min_soc = params.get("minSoC", 0.1)
    max_soc = params.get("maxSoC", 0.9)
    discharge_duration = params.get("dischargeDuration", 4)
    battery_power = params.get("batteryPower", 5)
    battery_efficiency = params.get("batteryEfficiency", 0.85)

    # Generate load profile
    hvac_usage = generate_hvac_load_profile(hvac_consumption, hvac_peak_time, hvac_load_shape)

    # Get hourly rates
    rates = calculate_hourly_rates(pricing_model, peak_rate, off_peak_rate, peak_start, peak_end, hourly_prices)

    # Calculate cost without battery
    total_hvac_usage = sum(hvac_usage)
    cost_without_battery = sum(usage * rate for usage, rate in zip(hvac_usage, rates))

    # Calculate peak/off-peak breakdown
    peak_cost_no_battery = sum(hvac_usage[h] * rates[h] for h in range(24) if peak_start <= h < peak_end)
    off_peak_cost_no_battery = cost_without_battery - peak_cost_no_battery

    # Optimize battery dispatch
    battery_result = optimize_battery_dispatch(
        hvac_usage, rates, battery_capacity, min_soc, max_soc, discharge_duration, battery_power, battery_efficiency
    )

    charge_plan = battery_result["charge_plan"]
    discharge_plan = battery_result["discharge_plan"]

    # Calculate cost with battery
    charge_cost = sum(charge * rate for charge, rate in zip(charge_plan, rates))

    hvac_from_grid = [usage - discharge for usage, discharge in zip(hvac_usage, discharge_plan)]

    peak_cost_with_battery = sum(hvac_from_grid[h] * rates[h] for h in range(24) if peak_start <= h < peak_end)
    off_peak_cost_with_battery = sum(
        hvac_from_grid[h] * rates[h] for h in range(24) if not (peak_start <= h < peak_end)
    )

    cost_with_battery = charge_cost + peak_cost_with_battery + off_peak_cost_with_battery
    daily_savings = cost_without_battery - cost_with_battery

    return {
        "dailySavings": round(daily_savings, 2),
        "totalHVACUsage": round(total_hvac_usage, 2),
        "costWithoutBattery": round(cost_without_battery, 2),
        "costWithBattery": round(cost_with_battery, 2),
        "energyShifted": round(battery_result["energy_stored"], 2),
        "breakdown": {
            "peakCostNoBattery": round(peak_cost_no_battery, 2),
            "offPeakCostNoBattery": round(off_peak_cost_no_battery, 2),
            "chargeCostWithBattery": round(charge_cost, 2),
            "peakCostWithBattery": round(peak_cost_with_battery, 2),
            "offPeakCostWithBattery": round(off_peak_cost_with_battery, 2),
        },
        "hourlyData": {
            "rates": [round(r, 4) for r in rates],
            "hvacUsage": [round(h, 3) for h in hvac_usage],
            "hvacFromGrid": [round(h, 3) for h in hvac_from_grid],
            "chargePlan": [round(c, 3) for c in charge_plan],
            "dischargePlan": [round(d, 3) for d in discharge_plan],
        },
    }


def calculate_yearly_simulation(params: Dict) -> Dict:
    """
    Calculate blended annual savings across different day types.

    Args:
        params: Dictionary with base params plus hot_days, mild_days, and presets

    Returns:
        Dictionary with annual savings and energy metrics
    """
    hot_days = params.get("hotDays", 90)
    mild_days = params.get("mildDays", 180)
    winter_days = 365 - hot_days - mild_days

    # Preset configurations
    presets = {
        "hot": {"hvacConsumption": 3.5, "hvacPeakTime": 16, "hvacLoadShape": 5},
        "mild": {"hvacConsumption": 1.5, "hvacPeakTime": 15, "hvacLoadShape": 3},
        "winter": {"hvacConsumption": 2.5, "hvacPeakTime": 7, "hvacLoadShape": 6},
    }

    # Calculate for each day type
    base_params = params.copy()
    results = {}

    for day_type, preset in presets.items():
        day_params = {**base_params, **preset}
        results[day_type] = calculate_homeowner_savings(day_params)

    # Calculate weighted annual values
    total_savings = (
        hot_days * results["hot"]["dailySavings"]
        + mild_days * results["mild"]["dailySavings"]
        + winter_days * results["winter"]["dailySavings"]
    )

    total_energy_shifted = (
        hot_days * results["hot"]["energyShifted"]
        + mild_days * results["mild"]["energyShifted"]
        + winter_days * results["winter"]["energyShifted"]
    )

    avg_daily_energy_shifted = total_energy_shifted / 365

    return {
        "blendedAnnualSavings": round(total_savings, 2),
        "totalEnergyShifted": round(total_energy_shifted, 2),
        "avgDailyEnergyShifted": round(avg_daily_energy_shifted, 2),
        "dayTypeResults": {
            "hot": results["hot"],
            "mild": results["mild"],
            "winter": results["winter"],
        },
    }


def calculate_rep_value(params: Dict) -> Dict:
    """
    Calculate REP (Retail Electricity Provider) value proposition.

    CRITICAL: Avoids double-counting by properly accounting for:
    1. Revenue loss = Homeowner's actual savings (dynamically calculated)
    2. Wholesale cost change = Based on actual energy flow changes
    3. Net margin = Wholesale savings - Revenue loss

    The homeowner's savings already account for all rate complexity, so we use
    that directly rather than recalculating with simplified assumptions.

    Args:
        params: Dictionary with REP parameters and homeowner results
            - blendedAnnualSavings: Total homeowner savings per year (REQUIRED)
            - totalEnergyShifted: Total kWh shifted per home per year (REQUIRED)

    Returns:
        Dictionary with REP value breakdown
    """
    rep_homes = params.get("repHomes", 10000)
    wholesale_peak = params.get("wholesalePeak", 250) / 1000  # $/kWh
    wholesale_off_peak = params.get("wholesaleOffPeak", 30) / 1000  # $/kWh
    ancillary_value = params.get("ancillaryValue", 2.5)  # $/kW-month
    capacity_contribution = params.get("capacityContribution", 4)  # kW

    # Homeowner results from yearly simulation
    homeowner_annual_savings = params.get("blendedAnnualSavings", 0)  # $ per home per year
    total_energy_shifted = params.get("totalEnergyShifted", 0)  # kWh per home per year
    avg_daily_energy_shifted = total_energy_shifted / 365 if total_energy_shifted > 0 else 0

    # Fleet-wide calculations
    fleet_annual_savings = homeowner_annual_savings * rep_homes  # Total homeowner savings
    fleet_annual_shift = total_energy_shifted * rep_homes  # Total kWh shifted
    fleet_avg_daily_shift = avg_daily_energy_shifted * rep_homes

    # === REP ECONOMIC ANALYSIS (avoiding double-counting) ===

    # REVENUE IMPACT:
    # Every dollar the homeowner saves = one less dollar REP collects
    # This is already dynamically calculated in homeowner tab (accounts for all complexity!)
    retail_revenue_loss = fleet_annual_savings

    # WHOLESALE COST IMPACT:
    # REP's procurement pattern changes due to battery:
    # - Without battery: REP buys energy matching homeowner's consumption (peak-heavy)
    # - With battery: REP buys energy matching homeowner's total draw (more off-peak)
    #
    # Simplified model: Assume shifted energy moves from peak wholesale to off-peak wholesale
    # (In reality, it's more complex, but this captures the first-order effect)
    wholesale_cost_without_battery = fleet_annual_shift * wholesale_peak
    wholesale_cost_with_battery = fleet_annual_shift * wholesale_off_peak
    wholesale_cost_savings = wholesale_cost_without_battery - wholesale_cost_with_battery

    # NET MARGIN IMPROVEMENT for REP:
    # = (Wholesale Cost Savings) - (Retail Revenue Loss)
    #
    # Note: This can be NEGATIVE if retail spread > wholesale spread!
    # Example: If retail spread is $0.16/kWh but wholesale spread is only $0.05/kWh,
    #          REP loses more revenue than they save in costs.
    net_margin_improvement = wholesale_cost_savings - retail_revenue_loss

    # Ancillary services revenue (new revenue stream from VPP capabilities)
    ancillary_revenue = rep_homes * capacity_contribution * ancillary_value * 12

    # Total REP value = Net margin improvement + New ancillary revenue
    total_value = net_margin_improvement + ancillary_revenue

    return {
        "avgDailyEnergyShifted": round(avg_daily_energy_shifted, 2),
        "avgDailyFleetShifted": round(fleet_avg_daily_shift, 2),
        "totalEnergyShifted": round(fleet_annual_shift / 1000, 2),  # MWh
        # Detailed breakdown (avoiding double-counting)
        "wholesaleCostSavings": round(wholesale_cost_savings, 2),
        "retailRevenueLoss": round(retail_revenue_loss, 2),
        "netMarginImprovement": round(net_margin_improvement, 2),
        "ancillaryRevenue": round(ancillary_revenue, 2),
        # Total value
        "totalValue": round(total_value, 2),
        # Legacy field for backward compatibility
        "wholesaleSavings": round(wholesale_cost_savings, 2),
    }


def calculate_ci_value(params: Dict) -> Dict:
    """
    Calculate C&I (Commercial & Industrial) business value.

    Args:
        params: Dictionary with C&I parameters

    Returns:
        Dictionary with annualized NPV for different project sizes
    """
    ebitda_per_mw = params.get("ebitdaPerMW", 1.0) * 1_000_000  # $M to $
    time_savings = params.get("timeSavings", 2)  # years
    discount_rate = params.get("discountRate", 10) / 100  # percentage to decimal
    op_horizon = params.get("opHorizon", 10)  # years

    project_loads = [10, 20, 30]  # MW
    results = []

    for load_mw in project_loads:
        total_ebitda = load_mw * ebitda_per_mw

        # Calculate NPV with VPP (earlier start)
        npv_with_vpp = sum(total_ebitda / ((1 + discount_rate) ** year) for year in range(1, op_horizon + 1))

        # Calculate NPV without VPP (delayed start)
        npv_without_vpp = sum(
            total_ebitda / ((1 + discount_rate) ** (year + time_savings)) for year in range(1, op_horizon + 1)
        )

        npv_advantage = npv_with_vpp - npv_without_vpp
        annualized_npv = npv_advantage / op_horizon

        results.append(
            {
                "loadMW": load_mw,
                "annualizedNPV": round(annualized_npv / 1_000_000, 2),  # in $M
            }
        )

    return {"cases": results}


def calculate_payback_period(params: Dict) -> Dict:
    """
    Calculate payback period for battery system.

    Args:
        params: Dictionary with cost and savings parameters

    Returns:
        Dictionary with payback calculations
    """
    total_cost = params.get("totalCost", 3500)
    federal_itc = params.get("federalITC", 30) / 100
    state_rebates = params.get("stateRebates", 0)
    utility_rebate = params.get("utilityRebate", 500)
    annual_savings = params.get("annualSavings", 0)

    federal_credit = total_cost * federal_itc
    net_cost = total_cost - federal_credit - state_rebates - utility_rebate

    if annual_savings > 0:
        payback_years = net_cost / annual_savings
    else:
        payback_years = 0

    return {
        "netCost": round(net_cost, 2),
        "annualSavings": round(annual_savings, 2),
        "paybackYears": round(payback_years, 1),
    }
