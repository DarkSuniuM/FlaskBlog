from flask import request, render_template, flash
from sqlalchemy.exc import IntegrityError

from app import db

from . import users
from .forms import RegisterForm
from .models import User


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            error_msg = 'Password and Confirm Password does not match.'
            form.password.errors.append(error_msg)
            form.confirm_password.errors.append(error_msg)
            return render_template('users/register.html', form=form)
        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('You created your account successfully.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Email is in use.', 'error')
    return render_template('users/register.html', form=form)
