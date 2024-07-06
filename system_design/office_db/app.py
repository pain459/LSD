from flask import Flask, render_template, request, redirect, url_for
from database import db
from forms import EmployeeForm, SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    from models import Employee
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_employee():
    form = SearchForm()
    employees = []
    if form.validate_on_submit():
        search_term = form.search.data
        employees = Employee.query.filter(
            (Employee.first_name.ilike(f'%{search_term}%')) |
            (Employee.middle_name.ilike(f'%{search_term}%')) |
            (Employee.last_name.ilike(f'%{search_term}%')) |
            (Employee.designation.ilike(f'%{search_term}%')) |
            (Employee.employee_id.ilike(f'%{search_term}%'))
        ).all()
    return render_template('search_employee.html', form=form, employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            sex=form.sex.data,
            age=form.age.data,
            designation=form.designation.data,
            employee_id=form.employee_id.data
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_employee.html', form=form, employee=employee)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
