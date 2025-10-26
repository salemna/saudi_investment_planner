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
