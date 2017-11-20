from project import db


class Employee(db.Model):
    """ User Model with all data about a specific user. """
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    social_security = db.Column(db.Integer)
    num_withholdings = db.Column(db.Integer)
    salary = db.Column(db.Integer)

    def __init__(self, last_name, first_name, address_line_1, address_line_2, city, 
                state, zip_code, social_security, num_withholdings, salary):
        self.last_name = last_name
        self.first_name = first_name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.social_security = social_security
        self.num_withholdings = num_withholdings
        self.salary = salary

    def __repr__(self):
        return "<Room(last_name='%s', first_name='%d', address_line_1='%d', address_line_2='%s', city='%s', \
                state='%d', zip_code='%d', social_security='%s', num_withholdings='%s', salary='%s')>" \
               % (self.last_name, self.first_name, self.address_line_1, self.address_line_2, self.city, 
                self.state, self.zip_code, self.social_security, self.num_withholdings, self.salary)

