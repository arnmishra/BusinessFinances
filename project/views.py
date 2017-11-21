from project import app, db
from models import Employee, Customer, Vendor, PayrollEvents
from flask import render_template, url_for, request, redirect
from project.scripts.taxes import calculate_social_security_tax, calculate_medicare_tax, calculate_federal_tax, calculate_state_tax

@app.route("/", methods=['GET'])
def index():
    """ Renders Home page
    :return: index.html
    """
    return render_template("index.html")

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
