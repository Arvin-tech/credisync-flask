from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"

# Configure database connection (adjust connection string if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/testingdb'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your employee model using Flask-SQLAlchemy
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Employee {self.name}>"


@app.route('/')
def index():
    # Retrieve all employees from the database
    employees = Employee.query.all()

    return render_template('index.html', employees=employees)


@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        # Create a new employee object
        new_employee = Employee(name=name, email=email, phone=phone)

        # Add the employee to the database and commit changes
        db.session.add(new_employee)
        db.session.commit()

        # Flash message for successful creation (optional)
        flash('Employee Added successfully!')

        return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    # Get the employee by ID
    employee = Employee.query.get(id)

    if employee is None:
        flash('Employee not found!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        employee.name = name
        employee.email = email
        employee.phone = phone

        # Update the employee in the database and commit changes
        db.session.commit()

        flash('Employee Updated successfully!')

        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    # Get the employee by ID
    employee = Employee.query.get(id)

    if employee is None:
        flash('Employee not found!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Delete the employee from the database and commit changes
        db.session.delete(employee)
        db.session.commit()

        flash('Employee Removed successfully!')

        return redirect(url_for('index'))

    return render_template('delete.html', employee=employee)  # Consider confirmation template


# Create database tables if they don't exist (optional)
@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)