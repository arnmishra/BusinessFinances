MEDICARE_TAX_LOW = 0.0145
MEDICARE_TAX_HIGH = 0.0235
MEDICARE_WAGE_DIVISION = 200000
SOCIAL_SECURITY_TAX = 0.062
SOCIAL_SECURITY_MAX_TAX = 118500
NUMBER_PAY_PERIODS_YEAR = 12 # Monthly Payment
SEMI_MONTHLY_EXEMPTION = 168.8


def calculate_social_security_tax(salary):
	""" Calculates the social security tax withholding based on salary

	http://payroll.wsu.edu/cgi-bin/taxcalc2017.htm
	:param salary: employee's current salary
	:return: social security tax withholdings
	"""
	tax = salary * SOCIAL_SECURITY_TAX
	if tax > SOCIAL_SECURITY_MAX_TAX:
		tax = SOCIAL_SECURITY_MAX_TAX
	return tax

def calculate_medicare_tax(salary):
	""" Calculates the medicare tax withholding based on salary

	http://payroll.wsu.edu/cgi-bin/taxcalc2017.htm
	:param salary: employee's current salary
	:return: medicare tax withholding
	"""
	if salary > MEDICARE_WAGE_DIVISION:
		tax = salary * MEDICARE_TAX_HIGH
	else:
		tax = salary * MEDICARE_TAX_LOW
	return tax

def calculate_federal_tax(salary, marital_status, federal_withholdings):
	""" Calculates the federal tax withholding based on salary, marital status, 
	and federal withholdings

	http://payroll.wsu.edu/taxes/howto.htm
	:param salary: employee's current salary
	:param marital_status: employee's current marital status
	:param federal_withholdings: employee's federal withholdings
	:return: Federal Tax Withholdings
	"""
	taxable_salary = salary - federal_withholdings * SEMI_MONTHLY_EXEMPTION
	if marital_status == "single":
		if taxable_salary > 17529:
			tax = (taxable_salary - 1759) * 0.396 + 5062.69
		elif taxable_salary > 17458:
			tax = (taxable_salary - 17458) * 0.35 + 5037.84
		elif taxable_salary > 8081:
			tax = (taxable_salary - 8081) * 0.33 + 1943.43
		elif taxable_salary > 3925:
			tax = (taxable_salary - 3925) * 0.28 + 779.75
		elif taxable_salary > 1677:
			tax = (taxable_salary - 1677) * 0.25 + 217.75
		elif taxable_salary > 484:
			tax = (taxable_salary - 484) * 0.15 + 38.8
		elif taxable_salary > 96:
			tax = (taxable_salary - 96) * 0.1
		else:
			tax = 0
	else:
		if taxable_salary > 19973:
			tax = (taxable_salary - 19973) * 0.396 + 5484.54
		elif taxable_salary > 17723:
			tax = (taxable_salary - 17723) * 0.35 + 4697.04
		elif taxable_salary > 10083:
			tax = (taxable_salary - 10083) * 0.33 + 2175.84
		elif taxable_salary > 6740:
			tax = (taxable_salary - 6740) * 0.28 + 1239.8
		elif taxable_salary > 3523:
			tax = (taxable_salary - 3523) * 0.25 + 435.55
		elif taxable_salary > 1138:
			tax = (taxable_salary - 1138) * 0.15 + 77.8
		elif taxable_salary > 360:
			tax = (taxable_salary - 360) * 0.1
		else:
			tax = 0

	return tax

def calculate_state_tax(salary, state_line1_withholdings, state_line2_withholdings):
	""" Calculates state tax withholdings for state of Illinois
	Source: http://www.revenue.state.il.us/Publications/Bulletins/2018/FY-2018-03.pdf

	:param salary: employee's current salary
	:param state_line1_withholdings: employee's line 1 withholdings (i.e. dependents)
	:param state_line2_withholdings: employee's line 2 withholdings (i.e. old age/blind)
	:return: Illinois State Tax Withholdings
	"""
	return max(0,0.0495 * (salary - (state_line1_withholdings * 2175 + state_line2_withholdings * 1000)/NUMBER_PAY_PERIODS_YEAR))