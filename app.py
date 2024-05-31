from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (adjust connection string if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credisync.db'
db = SQLAlchemy(app)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String(200), nullable=False)  # Consider using UUID for unique IDs
    salary = db.Column(db.Integer, nullable=False)
    loan_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), default="pending")  # Add status (pending, approved, rejected)

    def __repr__(self):
        return f"<LoanApplication {self.id} - {self.applicant_id}>"  # Improved representation


@app.route('/loan_application', methods=['GET', 'POST'])
def loan_application():
    if request.method == 'POST':
        # Extract data from the form
        applicant_id = request.form['applicant_id']
        salary = int(request.form['salary'])
        loan_amount = int(request.form['loan_amount'])

        # Create a new loan application
        new_application = LoanApplication(applicant_id=applicant_id, salary=salary, loan_amount=loan_amount)

        # Add the application to the database and commit changes
        db.session.add(new_application)
        db.session.commit()

        # Flash message for successful creation (optional)
        # flash('Loan application submitted successfully!')

        return redirect(url_for('loan_applications'))  # Redirect to applications list
    else:
        # Render the loan application form
        return render_template('loan_application.html')


@app.route('/loan_applications')
def loan_applications():
    # Retrieve all loan applications from the database
    applications = LoanApplication.query.all()

    return render_template('loan_applications.html', applications=applications)


@app.route('/loan_application/<int:application_id>/approve')
def approve_application(application_id):
    # Get the application by ID
    application = LoanApplication.query.get(application_id)

    if application:
        application.status = "approved"
        db.session.commit()

        # Flash message for approval (optional)
        # flash('Loan application approved successfully!')

        return redirect(url_for('loan_applications'))
    else:
        # Handle case where application ID is not found
        return f"Loan application with ID {application_id} not found."


@app.route('/loan_application/<int:application_id>/reject')
def reject_application(application_id):
    # Get the application by ID
    application = LoanApplication.query.get(application_id)

    if application:
        application.status = "rejected"
        db.session.commit()

        # Flash message for rejection (optional)
        # flash('Loan application rejected successfully!')

        return redirect(url_for('loan_applications'))
    else:
        # Handle case where application ID is not found
        return f"Loan application with ID {application_id} not found."


# Consider adding a route for deleting applications with proper confirmation handling

if __name__ == "__main__":
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
