# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Module, TestCase
import os

main = Blueprint('main', __name__)

# Dashboard route - Home page showing modules and test cases
@main.route('/dashboard')
def dashboard():
    modules = Module.query.filter_by(parent_id=None).all()  # Get root modules
    return render_template('dashboard.html', modules=modules)

@main.route('/add_test_case', methods=['GET', 'POST'])
def add_test_case():
    if request.method == 'POST':
        # Get the input directly from the form
        module_id = request.form['module_id']  # Now it's an input field, not a dropdown
        summary = request.form['summary']
        description = request.form['description']

        # Handle file upload (if any)
        file = request.files['attachment']
        attachment = os.path.join('uploads', file.filename) if file else None
        if file:
            file.save(attachment)

        # Save the test case
        test_case = TestCase(module_id=module_id, summary=summary, description=description, attachment=attachment)
        db.session.add(test_case)
        db.session.commit()

        flash('Test Case Added Successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('test_case_form.html')
