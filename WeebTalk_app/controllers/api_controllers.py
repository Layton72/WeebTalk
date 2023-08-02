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


@app.route('/search/process', methods=['POST'])
def get_search_string():
    session['search_string'] = request.form['search']
    return redirect('/search/anime')

@app.route('/search/anime')
def searchAnime():
    user = Users.get_one_by_id(session["logged_in"])
    search_string = session['search_string']

    if search_string == "":
        return redirect('/weebtalk')
    
    url = f'https://api.myanimelist.net/v2/anime?q={search_string}&limit=3'

    response = requests.get(url, headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID
        })

    response.raise_for_status()
    anime_dict = response.json()
    response.close()
    anime_list = anime_dict['data']
    session['next_page'] = anime_dict['paging']['next']

    return render_template('search_results.html', anime_list=anime_list, user=user)

@app.route('/search/anime/next')
def next_page():
    user = Users.get_one_by_id(session["logged_in"])
    url = session.pop('next_page', None)

    response = requests.get(url, headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID
        })

    response.raise_for_status()
    anime_dict = response.json()
    response.close()
    anime_list = anime_dict['data']
    session['next_page'] = anime_dict['paging']['next']

    return render_template('search_results.html', anime_list=anime_list, user=user)

@app.route('/anime_details/<int:mal_id>')
def anime_details(mal_id):
    user = Users.get_one_by_id(session["logged_in"])
    url = f'https://api.myanimelist.net/v2/anime/{mal_id}?fields=id,title,main_picture,alternative_titles,synopsis'

    print(CLIENT_ID)
    response = requests.get(url, headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID
        })

    response.raise_for_status()
    anime = response.json()
    response.close()

    animes = Animes.get_all_animes()
    for show in animes:
        if show.mal_id == mal_id:
            anime_id = Animes.get_one_by_mal_id(mal_id).id
            reviews = Reviews.get_all_reviews_by_anime_id(anime_id)

            # Calculates average user score
            sum = 0
            for review in reviews:
                sum += review.score
            if sum != 0:
                average_score = sum/len(reviews)
            else: average_score = ""

            # Calculates total upvote score for a single review

            for review in reviews:
                upvotes = Likes.get_all_upvotes(review.id)
                for upvote in upvotes:
                    review.total_upvotes += upvote.upvotes

            return render_template('anime_details.html', anime=anime, user=user, reviews=reviews, average_score=average_score)
        
    data = {
        "mal_id": mal_id,
        "title": anime["alternative_titles"]["en"],
        "thumbnail": anime["main_picture"]["large"],
        "synopsis": anime["synopsis"]
    }
    Animes.save(data)

    return render_template('anime_details.html', anime=anime, user=user)

# reference for how search data is returned from API
# {'data': 
#     [
#         {'node': 
#             {'id': 72, 
#             'title': 'Full Metal Panic? Fumoffu', 
#             'main_picture': 
#                 {'medium': 'https://cdn.myanimelist.net/images/anime/4/75260.jpg', 
#                 'large': 'https://cdn.myanimelist.net/images/anime/4/75260l.jpg'}
#             }
#         }
#     ], 
#     'paging': {'next': 'https://api.myanimelist.net/v2/anime?offset=1&q=full+metal&limit=1'}
#     }