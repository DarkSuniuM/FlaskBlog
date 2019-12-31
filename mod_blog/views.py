from flask import render_template, request
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import or_

from . import blog
from .models import Post, Category
from .forms import SearchForm

@blog.route('/')
def index():
    page = request.args.get('p', default=1, type=int)
    search_form = SearchForm()
    posts = Post.query.paginate(page, 5)
    return render_template('blog/index.html', posts=posts, search_form=search_form)


@blog.route('/<string:slug>')
def single_post(slug):
    search_form = SearchForm()
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog/single_post.html', post=post, search_form=search_form)


@blog.route('/search')
def search_blog():
    search_form = SearchForm()
    search_query = request.args.get('search_query', '')
    title_cond = Post.title.ilike(f'%{search_query}%')
    summary_cond = Post.summary.ilike(f'%{search_query}%')
    content_cond = Post.content.ilike(f'%{search_query}%')
    found_posts = Post.query.filter(or_(title_cond,
                                        summary_cond,
                                        content_cond)).all()
    print(found_posts)
    return render_template('blog/search.html', posts=found_posts, search_form=search_form, search_query=search_query)


@blog.route('/category/<string:slug>')
def single_category(slug):
    search_form = SearchForm()
    category = Category.query.filter(Category.slug == slug).first_or_404()
    return render_template('blog/single_category.html', posts=category.posts, search_form=search_form, category_name=category.name)
