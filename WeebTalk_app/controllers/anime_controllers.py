from WeebTalk_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
import requests
import os
from dotenv import load_dotenv
from WeebTalk_app.models.users import Users
from WeebTalk_app.models.animes import Animes
from WeebTalk_app.models.reviews import Reviews
from WeebTalk_app.models.likes import Likes

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')

@app.route('/weebtalk')
def home():
    if "logged_in" not in session:
        return redirect ('/weebtalk/login')
    
    user = Users.get_one_by_id(session["logged_in"])
    reviews = Reviews.get_all_reviews()

    for review in reviews:
                upvotes = Likes.get_all_upvotes(review.id)
                for upvote in upvotes:
                    review.total_upvotes += upvote.upvotes
                    
    return render_template('dashboard.html', user=user, reviews=reviews)

@app.route('/anime_details/<int:mal_id>/add_review')
def add_review(mal_id):
    if "logged_in" not in session:
        return redirect ('/weebtalk/login')
    user = Users.get_one_by_id(session["logged_in"])
    anime = Animes.get_one_by_mal_id(mal_id)
    if "errors" in session and session["errors"] == True:
        score = session.pop("score", None)
        review = session.pop("review", None)
        session["errors"] = False
        return render_template('add_review.html', anime=anime, user=user, score=score, review=review)
    return render_template('add_review.html', anime=anime, user=user)

@app.route('/anime_details/<int:anime_id>/add_review/process', methods=['POST'])
def process_review(anime_id):
    anime = Animes.get_one_by_id(anime_id)

    if not Reviews.validate_review(request.form):
        session["errors"] = True
        session["score"]= request.form["score"]
        session["review"]= request.form["review"]
        return redirect(f'/anime_details/{anime.mal_id}/add_review')

    data = {
        "score": request.form['score'],
        "review": request.form['review'],
        "user_id": session["logged_in"],
        "anime_id": anime_id
    }
    Reviews.save(data)

    return redirect(f'/anime_details/{anime.mal_id}')

@app.route('/weebtalk/my_reviews/<int:user_id>')
def my_reviews(user_id):
    if "logged_in" not in session:
        return redirect ('/weebtalk/login')
    
    user = Users.get_one_by_id(session["logged_in"])
    reviews = Reviews.get_all_reviews_by_user_id(user_id)

    return render_template('my_reviews.html', user=user, reviews=reviews)

@app.route('/weebtalk/edit_review/<int:review_id>')
def edit_review(review_id):
    if "logged_in" not in session:
        return redirect ('/weebtalk')
    
    user = Users.get_one_by_id(session["logged_in"])
    data = {
        "id": review_id
    }

    review = Reviews.get_one(data)
    reviews = Reviews.get_all_reviews_by_anime_id(review.anime_id)
    anime = Animes.get_one_by_id(review.anime_id)

    sum = 0
    for review in reviews:
        sum += review.score
    average_score = sum/len(reviews)

    if "errors" in session and session["errors"] == True:
        score = session.pop("score", None)
        review_session = session.pop("review", None)
        session["errors"] = False
        return render_template('edit_review.html', user=user, score=score, review=review, review_session=review_session, anime=anime, average_score=average_score)
    
    return render_template('edit_review.html', user=user, anime=anime, review=review, average_score=average_score)

@app.route('/weebtalk/edit_review/<int:review_id>/process', methods=['POST'])
def process_review_edit(review_id):

    if not Reviews.validate_review(request.form):
        session["errors"] = True
        session["score"]= request.form["score"]
        session["review"]= request.form["review"]
        return redirect(f'/weebtalk/edit_review/{review_id}')

    data = {
        "score": request.form['score'],
        "review": request.form['review'],
        "user_id": session["logged_in"],
        "id": review_id
    }

    Reviews.update(data)

    return redirect(f'/weebtalk/my_reviews/{session["logged_in"]}')

@app.route('/weebtalk/delete_review/<int:review_id>')
def delete_review(review_id):
    data = {"id": review_id}
    Reviews.delete(data)
    return redirect(f'/weebtalk/my_reviews/{session["logged_in"]}')

@app.route('/weebtalk/user_reviews/<int:user_id>')
def user_reviews(user_id):
    if "logged_in" not in session:
        return redirect ('/weebtalk/login')
    
    user = Users.get_one_by_id(session["logged_in"])
    user_reviews = Users.get_one_by_id(user_id)
    reviews = Reviews.get_all_reviews_by_user_id(user_id)

    for review in reviews:
            upvotes = Likes.get_all_upvotes(review.id)
            for upvote in upvotes:
                review.total_upvotes += upvote.upvotes

    return render_template('user_reviews.html', user=user, reviews=reviews, user_reviews=user_reviews)