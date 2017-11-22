from project import db

class Employee(db.Model):
    """ Employee Model with all data about business Employees. """
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    social_security = db.Column(db.String)
    federal_withholdings = db.Column(db.Integer)
    state_line1_withholdings = db.Column(db.Integer)
    state_line2_withholdings = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    marital_status = db.Column(db.String)

    def __init__(self, last_name, first_name, address_line_1, address_line_2, city, state, zip_code, social_security, 
        federal_withholdings, state_line1_withholdings, state_line2_withholdings, salary, marital_status):
        self.last_name = last_name
        self.first_name = first_name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.social_security = social_security
        self.federal_withholdings = federal_withholdings
        self.state_line1_withholdings = state_line1_withholdings
        self.state_line2_withholdings = state_line2_withholdings
        self.salary = salary
        self.marital_status = marital_status

    def __repr__(self):
        return "<Employee(last_name='%s', first_name='%s', address_line_1='%s', address_line_2='%s', city='%s', state='%s', \
            zip_code='%d', social_security='%s', federal_withholdings='%d', state_line1_withholdings='%s', \
            state_line2_withholdings'%s', salary='%d', marital_status='%s')>" \
               % (self.last_name, self.first_name, self.address_line_1, self.address_line_2, self.city, self.state, 
                self.zip_code, self.social_security, self.federal_withholdings, self.state_line1_withholdings,
                self.state_line2_withholdings, self.self.salary, self.marital_status)

class Customer(db.Model):
    """ Customer Model with all data about Customers. """
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)

    def __init__(self, company, last_name, first_name, address_line_1, address_line_2, city, state, zip_code, price):
        self.company = company
        self.last_name = last_name
        self.first_name = first_name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return "<Customer(company='%s', last_name='%s', first_name='%s', address_line_1='%s', address_line_2='%s', \
                city='%s', state='%s', zip_code='%d')>" \
               % (self.company, self.last_name, self.first_name, self.address_line_1, self.address_line_2,
                self.city,  self.state, self.zip_code)

class Vendor(db.Model):
    """ Vendor Model with all data about Vendor. """
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String)
    part = db.Column(db.String)
    price = db.Column(db.Integer)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)

    def __init__(self, company, part, price, address_line_1, address_line_2, city, state, zip_code):
        self.company = company
        self.part = part
        self.price = price
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return "<Vendor(company='%s', part='%s', price='%d', address_line_1='%s', address_line_2='%s',city='%s', \
                state='%s', zip_code='%d')>" \
               % (self.company, self.part, self.price, self.address_line_1, self.address_line_2, self.city, 
                self.state, self.zip_code)

class PayrollEvents(db.Model):
    """ PayrollEvents Model with all the different payroll events that happen stored. """
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer)
    bounce = db.Column(db.Integer)
    federal_tax_withholding = db.Column(db.Integer)
    state_tax_withholding = db.Column(db.Integer)
    social_security_tax = db.Column(db.Integer)
    medicare_tax = db.Column(db.Integer)
    employee_name = db.Column(db.String)
    total_paid = db.Column(db.Integer)

    def __init__(self, salary, bounce, federal_tax_withholding, state_tax_withholding, social_security_tax, medicare_tax, 
                employee_name, total_paid):
        self.salary = salary
        self.bounce = bounce
        self.federal_tax_withholding = federal_tax_withholding
        self.state_tax_withholding = state_tax_withholding
        self.social_security_tax = social_security_tax
        self.medicare_tax = medicare_tax
        self.employee_name = employee_name
        self.total_paid = total_paid

    def __repr__(self):
        return "<PayrollEvents(salary='%d', bounce='%d', federal_tax_withholding='%d', state_tax_withholding='%d', \
                social_security_tax='%d',medicare_tax='%d', employee_name='%s', total_paid='%d')>" \
               % (self.salary, self.bounce, self.federal_tax_withholding, self.state_tax_withholding,
                self.social_security_tax, self.medicare_tax,  self.employee_name, self.total_paid)

class Parts(db.Model):
    """ Parts Model keeps an inventory of what the company has. """
    id = db.Column(db.Integer, primary_key=True)
    part = db.Column(db.Integer)
    price_per_unit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    value = db.Column(db.String)

    def __init__(self, part, price_per_unit, quantity, value):
        self.part = part
        self.price_per_unit = price_per_unit
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return "<Parts(part='%d', price_per_unit='%d', quantity='%d', value='%d')>" \
               % (self.part, self.price_per_unit, self.quantity, self.value)

class InvoiceHistory(db.Model):
    """ InvoiceHistory Model keeps the history of past invoices """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    customer = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, date, customer, quantity, price_per_unit, total):
        self.date = date
        self.customer = customer
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.total = total

    def __repr__(self):
        return "<InvoiceHistory(date='%d', customer='%d', quantity='%d', price_per_unit='%d', total='%d')>" \
               % (self.date, self.customer, self.quantity, self.price_per_unit, self.total)

class POHistory(db.Model):
    """ POHistory Model keeps the history of past invoices """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    supplier = db.Column(db.String)
    part = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, date, supplier, part, quantity, price_per_unit, total):
        self.date = date
        self.supplier = supplier
        self.part = part
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.total = total

    def __repr__(self):
        return "<POHistory(date='%d', supplier='%d', part='%d', quantity='%d', price_per_unit='%d', total='%d')>" \
               % (self.date, self.supplier, self.part, self.quantity, self.price_per_unit, self.total)