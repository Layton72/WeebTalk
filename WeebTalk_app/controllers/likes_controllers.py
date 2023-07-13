from WeebTalk_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from WeebTalk_app.models.users import Users
from WeebTalk_app.models.animes import Animes
from WeebTalk_app.models.reviews import Reviews
from WeebTalk_app.models.likes import Likes


@app.route('/weebtalk/like/<int:review_id>/<int:mal_id>')
def upvote_anime_details(review_id, mal_id):
    mal_id = mal_id

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.upvote(data)
    return redirect(f'/anime_details/{mal_id}')

@app.route('/weebtalk/dislike/<int:review_id>/<int:mal_id>')
def downvote_anime_details(review_id, mal_id):
    mal_id = mal_id

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.downvote(data)
    return redirect(f'/anime_details/{mal_id}')

@app.route('/weebtalk/like/dashboard/<int:review_id>')
def upvote_dashboard(review_id):

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.upvote(data)
    return redirect('/weebtalk')

@app.route('/weebtalk/dislike/dashboard/<int:review_id>')
def downvote_dashboard(review_id):

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.downvote(data)
    return redirect('/weebtalk')

@app.route('/weebtalk/like/user_reviews/<int:review_id>/<int:user_reviews_id>')
def upvote_user_reviews(review_id, user_reviews_id):
    user_reviews_id = user_reviews_id

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.upvote(data)
    return redirect(f'/weebtalk/user_reviews/{user_reviews_id}')

@app.route('/weebtalk/dislike/user_reviews/<int:review_id>/<int:user_reviews_id>')
def downvote_user_reviews(review_id, user_reviews_id):
    user_reviews_id = user_reviews_id

    data = {
        "user_id": session["logged_in"],
        "review_id": review_id
    }

    upvotes = Likes.get_all_upvotes(review_id)
    for upvote in upvotes:
        if session["logged_in"] == upvote.user_id:
            Likes.delete(data)

    Likes.downvote(data)
    return redirect(f'/weebtalk/user_reviews/{user_reviews_id}')