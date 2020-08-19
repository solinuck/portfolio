import os
import re
import secrets
from flask import current_app


def search_func(posts, search):
    search_words = re.sub("[^A-Za-z0-9 ]+", "", search.lower())
    search_words = search_words.split()
    ids = []
    for post in posts.items:
        title = post.title
        tags = [
            tag_word
            for tag in eval(post.tags)
            for tag_word in tag.lower().split()
        ]
        title_words = title.lower().replace("-", " ").split()
        all_words = title_words + tags
        print(all_words)

        for search_word in search_words:
            if search_word in all_words:
                ids.append(post.id)
        print([post for post in posts.items if post.id in ids])
    return [post for post in posts.items if post.id in ids]


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.config["BLOG_UPLOADS"], picture_fn
    )
    form_image.save(picture_path)
    return picture_fn
