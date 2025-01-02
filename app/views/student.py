from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.sql import text
from app.models import db, Student

student = Blueprint('student', __name__)

# View all students


@student.route('/')
def student_list():
    students = Student.query.all()
    return render_template('student_list.html', students=students)

# Add a new student


@student.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = int(request.form['age'])
        course = request.form['course']
        
        # Find the next available ID
        last_student = Student.query.order_by(Student.id.desc()).first()
        next_id = (last_student.id + 1) if last_student else 1


        new_student = Student(id=next_id,name=name, email=email, age=age, course=course)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('student.student_list'))

    return render_template('add_student.html')

# Edit student details


@student.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.age = int(request.form['age'])
        student.course = request.form['course']
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('student.student_list'))

    return render_template('edit_student.html', student=student)

# Delete a student


@student.route('/delete_student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    # Delete the student with the given id
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()

        # Fetch remaining students and reset their IDs
        students = Student.query.order_by(Student.id).all()
        for index, student in enumerate(students, start=1):
            student.id = index
        db.session.commit()

        flash("Student deleted successfully", "success")
    else:
        flash("Student not found!", "error")

    return redirect(url_for('student.student_list'))
