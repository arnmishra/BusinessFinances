from project import app, db
from models import Employee, Customer, Vendor, PayrollEvents
from flask import render_template, url_for, request, redirect
from project.scripts.taxes import calculate_social_security_tax, calculate_medicare_tax, calculate_federal_tax, calculate_state_tax

initialized = False
income_statement = {"sales": 0, "cogs": 0, "payroll": 0, "payroll_withholding": 0, "bills": 0, "annual_expenses": 0,
                    "other_income": 0}
balance_sheet = {"cash": 0, "accounts_receivable": 0, "inventory": 0, "land": 0, "equipment": 0, "furniture": 0, 
                "accounts_payable": 0, "notes_payable": 0, "accruals": 0, "mortgage": 0, "net_worth": 0}

@app.route("/", methods=['GET'])
def index():
    """ Renders either business initialization page or home page depending on status

    :return: initialize business or home page
    """
    global initialized
    if not initialized:
        initialized = True
        return redirect("/initialize_business")
    return redirect("/home")

@app.route("/initialize_business", methods=['GET', 'POST'])
def initialize_business():
    """ Renders the business initialization page to get income sheet/balance statement
    information prior to starting the business 

    :return: initialize_business.html
    """
    if request.method == "GET":
        return render_template("initialize_business.html")
    income_statement["sales"] = float(request.form["sales"])
    income_statement["cogs"] = float(request.form["cogs"])
    income_statement["payroll"] = float(request.form["payroll"])
    income_statement["payroll_withholding"] = float(request.form["payroll_withholding"])
    income_statement["bills"] = float(request.form["bills"])
    income_statement["annual_expenses"] = float(request.form["annual_expenses"])
    income_statement["other_income"] = float(request.form["other_income"])
    balance_sheet["cash"] = float(request.form["cash"])
    balance_sheet["accounts_receivable"] = float(request.form["accounts_receivable"])
    balance_sheet["inventory"] = float(request.form["inventory"])
    balance_sheet["land"] = float(request.form["land"])
    balance_sheet["equipment"] = float(request.form["equipment"])
    balance_sheet["furniture"] = float(request.form["furniture"])
    balance_sheet["accounts_payable"] = float(request.form["accounts_payable"])
    balance_sheet["notes_payable"] = float(request.form["notes_payable"])
    balance_sheet["accruals"] = float(request.form["accruals"])
    balance_sheet["mortgage"] = float(request.form["mortgage"])
    balance_sheet["net_worth"] = float(request.form["net_worth"])
    return redirect("/home")

@app.route("/home", methods=['GET'])
def home():
    """ Renders the home page

    :return: home.html
    """
    return render_template("home.html")

@app.route("/view_employees", methods=['GET'])
def view_employees():
    """ Renders Employee View page

    :return: view_employees.html
    """
    employees = Employee.query.all()
    return render_template("view_employees.html", employees=employees)

@app.route("/add_employee", methods=['GET', 'POST'])
def add_employee():
    """ Renders Employee Add page

    :return: add_employee.html
    """
    if request.method == "GET":
        return render_template("add_employee.html")
    last_name = request.form["last_name"]
    first_name = request.form["first_name"]
    address_line_1 = request.form["address_line_1"]
    address_line_2 = request.form["address_line_2"]
    city = request.form["city"]
    state = request.form["state"]
    zip_code = float(request.form["zip_code"])
    social_security_1 = request.form["social_security_1"]
    social_security_2 = request.form["social_security_2"]
    social_security_3 = request.form["social_security_3"]
    social_security = "%s-%s-%s" % (social_security_1, social_security_2, social_security_3)
    federal_withholdings = float(request.form["federal_withholdings"])
    state_line1_withholdings = float(request.form["state_line1_withholdings"])
    state_line2_withholdings = float(request.form["state_line2_withholdings"])
    salary = float(request.form["salary"])
    marital_status = request.form["marital_status"]
    new_employee = Employee(last_name, first_name, address_line_1, address_line_2, city, state, zip_code, social_security,
                    federal_withholdings, state_line1_withholdings, state_line2_withholdings, salary, marital_status)
    db.session.add(new_employee)
    db.session.commit()
    return redirect("/view_employees")

@app.route("/view_customers", methods=['GET'])
def view_customers():
    """ Renders Customer View page

    :return: view_customers.html
    """
    customers = Customer.query.all()
    return render_template("view_customers.html", customers=customers)

@app.route("/add_customer", methods=['GET', 'POST'])
def add_customer():
    """ Renders Customer Add page

    :return: add_customer.html
    """
    if request.method == "GET":
        return render_template("add_customer.html")
    company = request.form["company"]
    last_name = request.form["last_name"]
    first_name = request.form["first_name"]
    address_line_1 = request.form["address_line_1"]
    address_line_2 = request.form["address_line_2"]
    city = request.form["city"]
    state = request.form["state"]
    zip_code = float(request.form["zip_code"])
    price = float(request.form["price"])
    new_customer = Customer(company, last_name, first_name, address_line_1, address_line_2, city, state, zip_code, price)
    db.session.add(new_customer)
    db.session.commit()
    return redirect("/view_customers")

@app.route("/view_vendors", methods=['GET'])
def view_vendors():
    """ Renders Vendor View page

    :return: view_vendors.html
    """
    vendors = Vendor.query.all()
    return render_template("view_vendors.html", vendors=vendors)

@app.route("/add_vendor", methods=['GET', 'POST'])
def add_vendor():
    """ Renders Vendor Add page

    :return: add_vendor.html
    """
    if request.method == "GET":
        return render_template("add_vendor.html")
    company = request.form["company"]
    part = request.form["part"]
    price = float(request.form["price"])
    address_line_1 = request.form["address_line_1"]
    address_line_2 = request.form["address_line_2"]
    city = request.form["city"]
    state = request.form["state"]
    zip_code = float(request.form["zip_code"])
    new_vendor = Vendor(company, part, price, address_line_1, address_line_2, city, state, zip_code)
    db.session.add(new_vendor)
    db.session.commit()
    return redirect("/view_vendors")

@app.route("/pay_employees", methods=['GET', 'POST'])
def pay_employees():
    """ Renders Pay Employee page

    :return: pay_employees.html
    """
    if request.method == "GET":
        employees = Employee.query.all()
        return render_template("pay_employees.html", employees=employees)
    employee_ids = request.form.getlist("employee")
    for employee_id in employee_ids:
        employee = Employee.query.filter_by(id=employee_id).first()
        salary = employee.salary
        name = '%s %s' % (employee.first_name, employee.last_name)
        social_security_tax = calculate_social_security_tax(salary)
        medicare_tax = calculate_medicare_tax(salary)
        federal_tax_withholding = calculate_federal_tax(salary, employee.marital_status, employee.federal_withholdings)
        state_tax_withholding = calculate_state_tax(salary, employee.state_line1_withholdings, employee.state_line2_withholdings)
        total_paid = salary - social_security_tax - federal_tax_withholding - medicare_tax - state_tax_withholding
        payroll_event = PayrollEvents(salary, 0, federal_tax_withholding, state_tax_withholding, social_security_tax, medicare_tax, name, total_paid)
        db.session.add(payroll_event)
    db.session.commit()
    return redirect("/view_payroll_events")

@app.route("/view_payroll_events", methods=['GET'])
def view_payroll_events():
    """ Renders Payroll Events page

    :return: view_payroll_events.html
    """
    payroll_events = PayrollEvents.query.all()
    return render_template("view_payroll_events.html", payroll_events=payroll_events)

@app.route("/view_pl_statement", methods=['GET'])
def view_pl_statement():
    """ Renders P&L (Income) Statement page

    :return: view_pl_statement.html
    """
    gross_profit = income_statement["sales"] + income_statement["cogs"]
    total_expenses = income_statement["payroll"] + income_statement["payroll_withholding"] 
    operating_income = gross_profit - total_expenses
    income_taxes = operating_income * 0.07 # Illinois Corporate Tax Rate = 7%: http://www.chicagotribune.com/news/ct-illinois-income-tax-hike-2017-htmlstory.html
    net_income = operating_income + income_statement["other_income"] - income_taxes

    return render_template("view_pl_statement.html", income_statement=income_statement, operating_income=operating_income,
            total_expenses=total_expenses, gross_profit=gross_profit, income_taxes=income_taxes, net_income=net_income)

@app.route("/view_balance_sheet", methods=['GET'])
def view_balance_sheet():
    """ Renders Balance Sheet page

    :return: view_balance_sheet.html
    """
    total_current_assets = balance_sheet["cash"] + balance_sheet["accounts_receivable"] + balance_sheet["inventory"]
    total_fixed_assets = balance_sheet["land"] + balance_sheet["equipment"] + balance_sheet["furniture"]
    total_assets = total_current_assets + total_fixed_assets
    total_current_liabilities = balance_sheet["accounts_payable"] + balance_sheet["notes_payable"] + balance_sheet["accruals"]
    total_long_term_debt = balance_sheet["mortgage"]
    total_liabilities = total_current_liabilities + total_long_term_debt
    total_liabilities_net_worth = total_liabilities + balance_sheet["net_worth"]

    return render_template("view_balance_sheet.html", balance_sheet=balance_sheet, total_current_assets=total_current_assets,
            total_fixed_assets=total_fixed_assets, total_assets=total_assets, total_long_term_debt=total_long_term_debt, 
            total_liabilities=total_liabilities, total_current_liabilities=total_current_liabilities, 
            total_liabilities_net_worth=total_liabilities_net_worth)
