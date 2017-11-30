from project import app, db
from models import Employee, Customer, Vendor, PayrollEvents, Parts, InvoiceHistory, POHistory, Units
from flask import render_template, url_for, request, redirect, jsonify
from project.scripts.taxes import calculate_social_security_tax, calculate_medicare_tax, calculate_federal_tax, calculate_state_tax

DATE = 1
MONTHS = [["Feb", 31], ["Mar", 28], ["Apr", 31], ["May", 30], ["June", 31], ["July", 30], ["Aug", 31], 
        ["Sept", 31], ["Oct", 30], ["Nov", 31], ["Dec", 30], ["Jan", 31]]
PAID_OFF = ["Jan", 2017]
INITIALIZED = False
ANNUAL_EXPENSE = 0
income_statement = {"sales": 0, "cogs": 0, "payroll": 0, "payroll_withholding": 0, "bills": 0, "annual_expenses": 0,
                    "other_income": 0}
balance_sheet = {"cash": 0, "accounts_receivable": 0, "inventory": 0, "land": 0, "equipment": 0, "furniture": 0, 
                "accounts_payable": 0, "notes_payable": 0, "accruals": 0, "mortgage": 0, "net_worth": 0}

@app.route("/", methods=['GET'])
def index():
    """ Renders either business initialization page or home page depending on status

    :return: initialize business or home page
    """
    global INITIALIZED
    if not INITIALIZED:
        INITIALIZED = True
        return redirect("/initialize_business")
    return redirect("/home")

@app.route("/initialize_business", methods=['GET', 'POST'])
def initialize_business():
    """ Renders the business initialization page to get information about
    the income statement, balance sheet, and units prior to starting the business 

    :return: initialize_business.html
    """
    global ANNUAL_EXPENSE
    if request.method == "GET":
        return render_template("initialize_business.html")
    income_statement["sales"] = float(request.form["sales"])
    income_statement["cogs"] = float(request.form["cogs"])
    income_statement["payroll"] = float(request.form["payroll"])
    income_statement["payroll_withholding"] = float(request.form["payroll_withholding"])
    income_statement["bills"] = float(request.form["bills"])
    income_statement["annual_expenses"] = float(request.form["annual_expenses"])
    ANNUAL_EXPENSE = float(request.form["annual_expenses"])
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
    global DATE, INITIALIZED
    if not INITIALIZED:
        INITIALIZED = True
        return redirect("/initialize_business")
    str_date = get_str_date()
    return render_template("home.html", date=str_date)

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
    new_customer = Customer(company, last_name, first_name, address_line_1, address_line_2, city, state, zip_code)
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
        monthly_salary = round(float(employee.salary/12.0),2)
        name = '%s %s' % (employee.first_name, employee.last_name)
        social_security_tax = round(calculate_social_security_tax(monthly_salary),2)
        medicare_tax = round(calculate_medicare_tax(monthly_salary),2)
        federal_tax_withholding = round(calculate_federal_tax(monthly_salary, employee.marital_status, employee.federal_withholdings),2)
        state_tax_withholding = round(calculate_state_tax(monthly_salary, employee.state_line1_withholdings, employee.state_line2_withholdings),2)
        total_paid = monthly_salary - social_security_tax - federal_tax_withholding - medicare_tax - state_tax_withholding
        payroll_event = PayrollEvents(monthly_salary, 0, federal_tax_withholding, state_tax_withholding, social_security_tax, medicare_tax, name, total_paid)
        db.session.add(payroll_event)
        income_statement["payroll"] += total_paid
        income_statement["payroll_withholding"] += social_security_tax + federal_tax_withholding + medicare_tax + state_tax_withholding
        balance_sheet["cash"] -= total_paid
        balance_sheet["net_worth"] -= total_paid
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
    Illinois Corporate Tax Rate = 7%: http://www.chicagotribune.com/news/ct-illinois-income-tax-hike-2017-htmlstory.html

    :return: view_pl_statement.html
    """
    gross_profit = income_statement["sales"] - income_statement["cogs"]
    total_expenses = income_statement["payroll"] + income_statement["bills"]  + income_statement["annual_expenses"]
    operating_income = gross_profit - total_expenses
    pre_tax_income = income_statement["other_income"] + operating_income
    income_taxes = round(pre_tax_income * 0.07,2)
    net_income = pre_tax_income - income_taxes

    return render_template("view_pl_statement.html", income_statement=income_statement, operating_income=operating_income,
            total_expenses=total_expenses, gross_profit=gross_profit, income_taxes=income_taxes, date=get_str_date(), 
            net_income=net_income)

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
            total_liabilities_net_worth=total_liabilities_net_worth, date=get_str_date())

@app.route("/view_inventory", methods=['GET'])
def view_inventory():
    """ Renders Inventory View page

    :return: view_inventory.html
    """
    units = Units.query.all()
    inventory = Parts.query.all()
    return render_template("view_inventory.html", units=units, inventory=inventory)

@app.route("/view_po_history", methods=['GET'])
def view_po_history():
    """ Renders Purchase Order History page

    :return: view_po_history.html
    """
    pos = POHistory.query.all()
    return render_template("view_po_history.html", pos=pos)

@app.route("/create_po", methods=['GET', 'POST'])
def create_po():
    """ Renders Create Purchase Order page

    :return: view_po_history.html
    """
    global DATE
    if request.method == "GET":
        vendors = Vendor.query.all()
        return render_template("create_po.html", vendors=vendors)
    part = request.form["part"]
    quantity = float(request.form["quantity"])
    existing_part = Parts.query.filter_by(part=part).first()
    vendor = Vendor.query.filter_by(part=part).first()
    if existing_part:
        existing_part.quantity += quantity
        existing_part.value = existing_part.quantity*existing_part.price_per_unit
        price_per_unit = existing_part.price_per_unit
    else:
        price_per_unit = vendor.price
        value = quantity * price_per_unit
        new_parts = Parts(part, vendor.price, quantity, value)
        db.session.add(new_parts)
    total = quantity * price_per_unit
    new_po = POHistory(get_str_date(), vendor.company, part, quantity, price_per_unit, total)
    db.session.add(new_po)
    db.session.commit()
    balance_sheet["accounts_payable"] += total
    balance_sheet["inventory"] += total
    return redirect("/view_po_history")

@app.route("/view_invoice_history", methods=['GET'])
def view_invoice_history():
    """ Renders Invoice Order History page

    :return: view_invoice_history.html
    """
    invoices = InvoiceHistory.query.all()
    return render_template("view_invoice_history.html", invoices=invoices)

@app.route("/create_invoice", methods=['GET', 'POST'])
def create_invoice():
    """ Renders Create Invoice page

    :return: view_invoice_history.html
    """
    global DATE
    if request.method == "GET":
        customers = Customer.query.all()
        units = Units.query.all()
        return render_template("create_invoice.html", customers=customers, units=units)
    customer = request.form["customer"]
    unit_id = request.form["unit"]
    quantity = float(request.form["quantity"])
    unit = Units.query.filter_by(id=unit_id).first()
    unit.quantity -= quantity
    total = unit.price_per_unit * quantity
    new_invoice = InvoiceHistory(get_str_date(), customer, unit.unit_name, quantity, unit.price_per_unit, total)
    db.session.add(new_invoice)
    db.session.commit()
    income_statement["sales"] += total
    income_statement["cogs"] += quantity * unit.cost_per_unit
    balance_sheet["accounts_receivable"] += total
    balance_sheet["net_worth"] += total
    return redirect("/view_invoice_history")

@app.route("/build_units", methods=['GET', 'POST'])
def build_units():
    """ Build Product Units to Sell 

    :return: inventory.html 
    """
    if request.method == "GET":
        parts = Parts.query.all()
        return render_template("build_units.html", parts=parts)
    unit_name = request.form["unit_name"]
    price_per_unit = float(request.form["price_per_unit"])
    parts = request.form.getlist("parts")
    cost_per_unit = 0
    build_quantity = float(request.form["quantity"])
    for part in parts:
        queried_part = Parts.query.filter_by(id=part).first()
        quantity_per_part = float(request.form[part])
        queried_part.quantity -= quantity_per_part*build_quantity
        queried_part.value = queried_part.quantity*queried_part.price_per_unit
        cost_per_unit += quantity_per_part*queried_part.price_per_unit
    new_unit = Units(unit_name, price_per_unit, cost_per_unit, build_quantity)
    db.session.add(new_unit)
    db.session.commit()
    return redirect('/view_inventory')

@app.route("/increment_date", methods=['POST'])
def increment_date():
    """ Asynchronously Increments the Date """
    global DATE, MONTHS
    if "num_days" in request.form:
        DATE += int(request.form["num_days"])
    else:
        DATE += 1
    str_date = get_str_date()
    return jsonify({"date": str_date})

def get_str_date():
    """ Converts Date to String Version
    Handles Recurring Expenses depending on the date

    :return: String Representation of Date
    """
    global DATE, MONTHS, PAID_OFF
    calc_year = 2017
    calc_month = "Jan"
    calc_date = DATE
    if calc_date > 365:
        calc_year += calc_date/365
        calc_date = calc_date%365
    for month in MONTHS:
        if calc_date - month[1] > 0:
            calc_date = calc_date - month[1]
            calc_month = month[0]
        else:
            break
    if calc_year != PAID_OFF[1]:
        handle_yearly_expenses(calc_year - PAID_OFF[1])
        handle_monthly_expenses()
        PAID_OFF = [calc_month, calc_year]
    if calc_month != PAID_OFF[0]:
        handle_monthly_expenses()
        PAID_OFF = [calc_month, calc_year]
    return "%s %d, %d" % (calc_month, calc_date, calc_year)

def handle_monthly_expenses():
    """ Handles Monthly Transactions (Accounts Receivable and Accounts Payable)"""
    balance_sheet["cash"] = balance_sheet["cash"] + balance_sheet["accounts_receivable"] - balance_sheet["accounts_payable"]
    balance_sheet["accounts_receivable"] = 0
    balance_sheet["accounts_payable"] = 0

def handle_yearly_expenses(multiplier):
    """ Handles Yearly Expenses """
    global ANNUAL_EXPENSE
    added_expenses = ANNUAL_EXPENSE*multiplier
    income_statement["annual_expenses"] += added_expenses
    balance_sheet["net_worth"] -= added_expenses
    balance_sheet["cash"] -= added_expenses
