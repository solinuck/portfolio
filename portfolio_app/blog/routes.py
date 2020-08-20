from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort,
)
from flask_login import login_required, current_user

from portfolio_app import db
from portfolio_app.blog.forms import PostForm
from portfolio_app.models import Post
from portfolio_app.blog.utils import search_func, save_image


today = datetime.today()
if len(str(today.month)) == 1:
    today_month = "0" + str(today.month)
else:
    today_month = str(today.month)


today_year = str(today.year)[2:]

blog = Blueprint("blog", __name__, url_prefix="/blog")


@blog.route(
    "/",
    defaults={
        "search": None,
        "year": today_year,
        "month": today_month,
        "expandsearch": False,
    },
    methods=("GET", "POST"),
)
@blog.route(
    "/<year>/<month>/expand<expandsearch>",
    defaults={"search": None},
    methods=("GET", "POST"),
)
@blog.route(
    "/<year>/<month>/expand<expandsearch>/<search>",
    methods=("GET", "POST"),
)
@blog.route(
    "/<search>",
    defaults={
        "year": today_year,
        "month": today_month,
        "expandsearch": False,
    },
    methods=("GET", "POST"),
)
def bloglist_view(search, expandsearch, year, month):
    months = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "Oktober",
        "11": "November",
        "12": "December",
    }

    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=6
    )

    all_posts = Post.query.all()
    all_topics = []
    for post in all_posts:
        all_topics.append(eval(post.tags))
    print(all_topics)

    tags = []
    body = []
    for post in posts.items:
        tags.append(eval(post.tags))
        body.append(eval(post.body))

    if search is None:
        search_posts = posts.items
    else:
        if request.method == "POST":
            search = request.form["search"]
        if search.replace(" ", "") != "":
            search_posts = search_func(posts, search)

    return render_template(
        "blog/bloglist.html",
        posts=posts,
        topics=all_topics,
        all_posts=all_posts,
        tags=tags,
        body=body,
        search_posts=search_posts,
        search=search,
        months=months,
        year=year,
        month=month,
        expandsearch=expandsearch,
    )


@blog.route("/<title>-<int:id>/")
def single_article_view(id, title):
    curr_post = Post.query.get_or_404(id)
    curr_tags = eval(curr_post.tags)
    curr_body = eval(curr_post.body)

    prev_post = Post.query.get(id - 1)
    prev_tags = None
    if prev_post:
        prev_tags = eval(prev_post.tags)

    next_tags = None
    next_post = Post.query.get(id + 1)
    if next_post:
        next_tags = eval(next_post.tags)

    return render_template(
        "blog/article.html",
        post=curr_post,
        tags=curr_tags,
        body=curr_body,
        prev_post=prev_post,
        prev_tags=prev_tags,
        next_post=next_post,
        next_tags=next_tags,
    )


@blog.route("/create", methods=["GET", "POST"])
@login_required
def create_view():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data)
        tags = [
            request.form[f"tag{n}"]
            for n in range(5)
            if f"tag{n}" in request.form
        ]
        html_body = str(form.body.data.replace("\r", "").split("\n"))

        post = Post(
            title=form.title.data,
            author=current_user,
            intro=form.intro.data,
            image_file=image_file,
            body=html_body,
            tags=repr(tags),
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("blog.bloglist_view"))

    return render_template(
        "blog/create_article.html", legend="New Post", form=form
    )


@blog.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_view(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            post.image_file = image_file

        post.title = form.title.data
        post.intro = form.intro.data
        post.body = str(form.body.data.replace("\r", "").split("\n"))
        post.tags = repr(
            [
                request.form[f"tag{n}"]
                for n in range(5)
                if f"tag{n}" in request.form
            ]
        )
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("blog.bloglist_view"))
    elif request.method == "GET":
        form.title.data = post.title
        form.intro.data = post.intro
        body_string = ""
        for i, p in enumerate(eval(post.body)):
            if p == "":
                p = "\n"
            body_string += p
        form.body.data = body_string
        form.image.data = post.image_file
        form.tag0.data = eval(post.tags)[0]

    return render_template(
        "blog/create_article.html",
        legend="Update Post",
        form=form,
        tags=eval(post.tags),
        image_file=True,
    )


@blog.route("<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_view(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        print("test")
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for("blog.bloglist_view"))
