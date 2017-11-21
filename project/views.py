from project import app, db
from models import Employee, Customer, Vendor, PayrollEvents
from flask import render_template, url_for, request, redirect

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
    print employees
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
    num_withholdings = float(request.form["num_withholdings"])
    salary = float(request.form["salary"])
    new_employee = Employee(last_name, first_name, address_line_1, address_line_2, city, state, zip_code, social_security,
                    num_withholdings, salary)
    db.session.add(new_employee)
    db.session.commit()
    employees = Employee.query.all()
    return redirect("/view_employees")