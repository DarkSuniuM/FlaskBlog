from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import uuid


from app import db
from mod_blog.forms import PostForm, CategoryForm
from mod_blog.models import Post, Category
from mod_users.forms import LoginForm, RegisterForm
from mod_users.models import User
from mod_uploads.models import File
from mod_uploads.forms import FileUploadForm

from . import admin
from .utils import admin_only_view


@admin.route('/')
@admin_only_view
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first()
        if not user:
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=form)
        if not user.is_admin():
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return redirect(url_for('admin.index'))
    if session.get('role') == 1:
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/', methods=['GET'])
@admin_only_view
def logout():
    session.clear()
    flash('You logged out successfully.', 'warning')
    return redirect(url_for('admin.login'))


@admin.route('/users/', methods=['GET'])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', users=users)


@admin.route('/users/new/', methods=['GET'])
@admin_only_view
def get_create_user():
    form = RegisterForm()
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/new/', methods=['POST'])
@admin_only_view
def post_create_user():
    form = RegisterForm(request.form)
    if not form.validate_on_submit():
        return render_template('admin/create_user.html', form=form)
    if not form.password.data == form.confirm_password.data:
        error_msg = 'Password and Confirm Password does not match.'
        form.password.errors.append(error_msg)
        form.confirm_password.errors.append(error_msg)
        return render_template('admin/create_user.html', form=form)
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
    return render_template('admin/create_user.html', form=form)


@admin.route('/posts/new/', methods=['GET', 'POST'])
@admin_only_view
def create_post():
    form = PostForm(request.form)
    categories = Category.query.order_by(Category.id.asc()).all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    if request.method == 'POST':
        if not form.validate_on_submit():
            return "Form validation error!"
        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        new_post.categories = [Category.query.get(category_id) for category_id in form.categories.data]
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated.')
    return render_template('admin/create_post.html', form=form)


@admin.route('/posts/', methods=['GET'])
@admin_only_view
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>/', methods=['GET'])
@admin_only_view
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted.')
    return redirect(url_for('admin.list_posts'))


@admin.route('/posts/modify/<int:post_id>/', methods=['GET', 'POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    categories = Category.query.order_by(Category.id.asc()).all()
    form.categories.choices = [(category.id, category.name) for category in categories]
    if request.method != 'POST':
        form.categories.data = [category.id for category in post.categories]
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.categories = [Category.query.get(category_id) for category_id in form.categories.data]
        try:
            db.session.commit()
            flash('Post modified!')
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated.')
    return render_template('admin/modify_post.html', form=form, post=post)


@admin.route('/categories/new/', methods=['GET', 'POST'])
@admin_only_view
def create_category():
    form = CategoryForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return "1"
        new_category = Category()
        new_category.name = form.name.data
        new_category.slug = form.slug.data
        new_category.description = form.description.data
        try:
            db.session.add(new_category)
            db.session.commit()
            flash('Category created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated.')
    return render_template('admin/create_category.html', form=form)


@admin.route('/categories/', methods=['GET'])
@admin_only_view
def list_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    print(categories)
    return render_template('admin/list_categories.html', categories=categories)


@admin.route('/categories/delete/<int:category_id>/', methods=['GET'])
@admin_only_view
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category Deleted.')
    return redirect(url_for('admin.list_categories'))


@admin.route('/categories/modify/<int:category_id>/', methods=['GET', 'POST'])
@admin_only_view
def modify_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_category.html', form=form, category=category)
        category.name = form.name.data
        category.description = form.description.data
        category.slug = form.slug.data
        try:
            db.session.commit()
            flash('Category modified!')
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated.')
    return render_template('admin/modify_category.html', form=form, category=category)



@admin.route('/library/upload', methods=['GET', 'POST'])
@admin_only_view
def upload_file():
    form = FileUploadForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return "1"
        filename = f'{uuid.uuid1()}_{secure_filename(form.file.data.filename)}'
        new_file = File()
        new_file.filename = filename
        try:
            db.session.add(new_file)
            db.session.commit()
            form.file.data.save(f'static/uploads/{filename}')
            flash(f'File Uploaded on {url_for("static", filename="uploads/"+filename, _external=True)}')
        except IntegrityError:
            db.session.rollback()
            flash('Upload failed', 'error')
    return render_template('admin/upload_file.html', form=form)
