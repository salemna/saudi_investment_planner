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
