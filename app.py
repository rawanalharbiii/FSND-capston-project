import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth, get_token_auth_header


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE')
        return response

    @app.route('/')
    def index():
        return 'Hello, Welcome Capstone project'

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = list(map(Movies.format, Movies.query.all()))
        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        actors = list(map(Actors.format, Actors.query.all()))
        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        movie = Movies.query.get(movie_id)
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'id': movie_id
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        actor = Actors.query.get(actor_id)
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'id': actor_id
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):
        body = request.get_json()
        if body:
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            if(new_title) and (new_release_date):
                new_movie = Movies(
                    title=new_title, release_date=new_release_date)
                try:
                    new_movie.insert()
                    succcess = True
                except:
                    abort(422)

                return jsonify({
                    'success': True,
                    'movie id': new_movie.id
                })
            else:
                abort(400)
        else:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):
        body = request.get_json()
        if body:
            new_name = body.get('name', None)
            new_age = int(body.get('age', 0))
            new_gender = body.get('gender', None)

            if (new_name) and (new_gender) and (new_age >= 0):
                new_actor = Actors(
                    name=new_name, age=new_age, gender=new_gender)
                try:
                    new_actor.insert()
                    succcess = True
                except:
                    abort(422)

                return jsonify({
                    'success': True,
                    'actor id': new_actor.id
                })
            else:
                abort(400)
        else:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):
        movie = Movies.query.get(movie_id)

        if movie is None:
            abort(404)

        body = request.get_json()
        if body:
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)
            if (new_title) and (new_release_date):
                movie.title = new_title
                movie.release_date = new_release_date

                try:
                    movie.update()

                except:
                    abort(422)

                return jsonify({
                    'success': True,
                    'movie_id': movie_id
                })
            else:
                abort(400)
        else:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):
        actor = Actors.query.get(actor_id)
        if actor is None:
            abort(404)
        body = request.get_json()
        if body:
            new_name = body.get('name', None)
            new_age = int(body.get('age', 0))
            new_gender = body.get('gender', None)

            if (new_name) and (new_gender) and (new_age >= 0):
                actor.name = new_name
                actor.age = new_age
                actor.gender = new_gender
                try:
                    actor.update()
                except:
                    abort(422)

                return jsonify({
                    'success': True,
                    'actor id': actor_id
                })
            else:
                abort(400)

        else:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'method not allowed'
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
