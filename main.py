import numpy as np
import pandas as pd
from typing import Optional, Tuple


class UserProfile:
    current_age: int
    retirement_age: int
    plan_end_age: int  #e.g., 90
    is_new_system_member: bool  #True if joined workforce AFTER 2024-07-03 with no prior contributions
    months_of_contrib_so_far: int #total contributory months to date
    starting_monthly_salary: float  #SAR, contributory wage
    annual_salary_growth: float  #nominal %, e.g., 0.03 for 3%
    monthly_investment: float  #SAR/month saved into private investments (besides GOSI)
    current_investments: float  #existing private portfolio (SAR)
    expected_portfolio_nominal_return: float  #user's own portfolio nominal expectation, used for feasibility check
class InflationAssumption:
    annual_cpi: float  # default around 0.02 (2%)

class MarketAssumptions:
    equity_real_return: float = 0.045  #4.5% real
    equity_vol: float = 0.20           #~20% standard deviation (real)
    sukuk_real_return: float = 0.010 #1.0% real
    sukuk_vol: float = 0.07          # sukuk volatility ~7% (real)
    cash_real_return: float = 0.000       #0% real
    cash_vol: float = 0.005               #~0.5% (real)

class GOSIParams:
    # Contribution rates (employee share) — current system
    employee_annuity_rate_current: float = 0.09 #9% of contributory wage
    employee_saned_rate_current: float = 0.0075 #0.75% (since 2022) of contributory wage
    # New system (for new entrants from 2024-07-03): pension branch rises from 9% to 11% over years 2–5
    employee_annuity_rate_new_start: float = 0.09  #starts at 9%
    employee_annuity_rate_new_target: float = 0.11 #rises to 11% (+2% total) by year 5
    # Wage bounds (official GOSI FAQ)
    min_contributory_wage: float = 400.0           # SAR/month - voluntary minimum
    max_contributory_wage: float = 45000.0         # SAR/month - statutory maximum
    # New-system pension formula details
    new_sys_pension_accrual_rate_per_year: float = 0.0225  # 2.25% per year
    avg_months_for_wage: int = 180  #highest 180 months average used
    early_ret_discount_per_year: float = 0.03  # default 3% per year early (user can change)

def estimate_new_system_pension(profile: UserProfile, gosi: GOSIParams,
                                start_year: int, df_contrib: pd.DataFrame,
                                early_years: int, override_discount: Optional[float] = None) -> float:
    # Build projected monthly wages (nominal), at least 180 months if available
    # Here we use df_contrib monthly_salary_nominal_SAR per year
    monthly_wages = np.repeat(df_contrib["monthly_salary_nominal_SAR"].values, repeats=12)
    months_of_service = min(len(monthly_wages), (profile.retirement_age - profile.current_age) * 12 + profile.months_of_contrib_so_far)
    # Highest 180 months average
    if len(monthly_wages) >= gosi.avg_months_for_wage:
        top_180 = np.sort(monthly_wages)[-gosi.avg_months_for_wage:]
        avg_top = float(np.mean(top_180))
    else:
        avg_top = float(np.mean(monthly_wages)) if len(monthly_wages) > 0 else profile.starting_monthly_salary

    years_of_service_total = months_of_service / 12.0
    pension_monthly = gosi.new_sys_pension_accrual_rate_per_year * avg_top * years_of_service_total

    # Early retirement reduction
    if early_years > 0:
        disc = override_discount if override_discount is not None else gosi.early_ret_discount_per_year
        pension_monthly *= max(0.0, 1.0 - disc * early_years)

    return pension_monthly

def horizon_years(current_age: int, retirement_age: int) -> int:
    return max(0, retirement_age - current_age)

def retirement_years(retirement_age: int, plan_end_age: int) -> int:
    return max(1, plan_end_age - retirement_age)

def monthly_series(years: int) -> int:
    return int(years * 12)

def accumulate_with_contributions(
    profile: UserProfile,
    infl: InflationAssumption,
    mkt: MarketAssumptions,
    gosi: GOSIParams,
    start_year: int = 2025,
) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    H_yrs = horizon_years(profile.current_age, profile.retirement_age)
    months_to_ret = monthly_series(H_yrs)
    if months_to_ret == 0:
        months_to_ret = 1
    years = np.arange(0, H_yrs + 1)
    salary_nominal = np.minimum(
        profile.starting_monthly_salary * (1 + profile.annual_salary_growth) ** years,
        gosi.max_contributory_wage
    )
    invest_contrib_nominal = np.full_like(years, profile.monthly_investment, dtype=float)

    df_contrib = pd.DataFrame({
        "year_index": years,
        "calendar_year": start_year + years,
        "monthly_salary_nominal_SAR": salary_nominal,
        "user_investment_per_month_SAR": invest_contrib_nominal
    })
    df_contrib["employee_GOSI_per_year_SAR"] = df_contrib["employee_GOSI_per_month_SAR"] * 12
    df_contrib["user_investment_per_year_SAR"] = df_contrib["user_investment_per_month_SAR"] * 12
    return df_contrib



def main():

    current_age = 30
    retirement_age = 60
    plan_end_age = 90
    is_new_system_member = True
    months_so_far = 0 #months in gosi
    starting_salary = 10000.0  #SAR/month
    salary_growth = 0.03  #3% nominal
    monthly_invest = 2000.0 #SAR/month
    current_port = 50000.0  #SAR
    expected_nom_ret = 0.06  #6% nominal


    mkt = MarketAssumptions()
    gosi = GOSIParams()
    profile = UserProfile(
            current_age=current_age,
            retirement_age=retirement_age,
            plan_end_age=plan_end_age,
            is_new_system_member=is_new_system_member,
            months_of_contrib_so_far=months_so_far,
            starting_monthly_salary=starting_salary,
            annual_salary_growth=salary_growth,
            monthly_investment=monthly_invest,
            current_investments=current_port,
            expected_portfolio_nominal_return=expected_nom_ret,
        )
