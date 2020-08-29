import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

ASSISTENT_TOKEN = str('Bearer ' + os.environ['ASSISTENT_TOKEN'])
DIRECTOR_TOKEN = str('Bearer ' + os.environ['DIRECTOR_TOKEN'])
PRODUCER_TOKEN = str('Bearer ' + os.environ['PRODUCER_TOKEN'])


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'rawan1'
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres',
                                                             '1111', 'localhost:5432', self.database_name)

        self.assistant = {'Content-Type': 'application/json',
                          'Authorization': ASSISTENT_TOKEN}
        self.director = {'Content-Type': 'application/json',
                         'Authorization': DIRECTOR_TOKEN}
        self.producer = {'Content-Type': 'application/json',
                         'Authorization': PRODUCER_TOKEN}
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_401_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_404_get_movies(self):
        Movies.query.delete()
        response = self.client().get('/movies', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        movie = Movies(title='The Last Man Standing',
                       release_date='12-21-23 12:00 pm')
        movie.insert()
        response = self.client().get('/movies', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_404_get_actors(self):
        Actors.query.delete()
        response = self.client().get('/actors', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        actor = Actors(name='Elsa',
                       age=21, gender='Female')
        actor.insert()
        response = self.client().get('/actors', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_movie(self):
        response = self.client().delete('/movies/1', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_404_delete_movie(self):
        response = self.client().delete('/movies/100000', headers=self.producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        movie = Movies(title='The Last Man Standing',
                       release_date='12-21-23 12:00 pm')
        movie.insert()
        movie_id = movie.id
        response = self.client().delete('/movies/'+str(movie_id)+'', headers=self.producer)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_actor(self):
        response = self.client().delete('/actors/1', headers=self.assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_404_delete_actor(self):
        response = self.client().delete('/actors/100000', headers=self.producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        actor = Actors(name='Elsa',
                       age=21, gender='Female')

        actor.insert()
        actor_id = actor.id
        response = self.client().delete('/actors/'+str(actor_id)+'', headers=self.producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_add_movie(self):
        response = self.client().post('/movies', headers=self.assistant,
                                      json={'title': 'My ex', 'release_date': '12-21-23 12:00 pm'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_400_add_movie(self):
        response = self.client().post('/movies', headers=self.producer,
                                      json={'title': 'My ex'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_add_movie(self):
        response = self.client().post('/movies', headers=self.producer,
                                      json={'title': 'My ex wife', 'release_date': '12-21-23 12:00 pm'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_add_actor(self):
        response = self.client().post('/actors', headers=self.assistant,
                                      json={'name': 'Elsai',
                                            'age': 21, 'gender': 'Female'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_400_add_actor(self):
        response = self.client().post('/actors', headers=self.producer,
                                      json={'age': -71, 'gender': 'Female'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_add_actor(self):
        response = self.client().post('/actors', headers=self.producer,
                                      json={'name': 'rawan',
                                            'age': 21, 'gender': 'Female'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_update_movie(self):
        response = self.client().patch('/movies/1', headers=self.assistant,
                                       json={'title': 'The last ship', 'release_date': '12-21-23 12:00 pm'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_400_update_movie(self):
        movie = Movies(title='The Last Man Standing',
                       release_date='12-21-23 12:00 pm')
        movie.insert()
        movie_id = movie.id
        response = self.client().patch('/movies/'+str(movie_id)+'', headers=self.director)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        movie = Movies(title='The Last Man Standing',
                       release_date='12-21-23 12:00 pm')
        movie.insert()
        movie_id = movie.id

        response = self.client().patch('/movies/'+str(movie_id) + '', headers=self.director,
                                       json={'title': 'The last ship', 'release_date': '12-21-23 12:00 pm'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_update_actor(self):
        response = self.client().patch('/actors/1', headers=self.assistant,
                                       json={'name': 'rawan',
                                             'age': 22, 'gender': 'female'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_400_update_actor(self):
        actor = Actors(name='Elsa', age=21, gender='Female')
        actor.insert()
        actor_id = actor.id
        response = self.client().patch('/actors/'+str(actor_id)+'', headers=self.director)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        actor = Actors(name='Elsa ', age=21, gender='Female')
        actor.insert()
        actor_id = actor.id
        response = self.client().patch('/actors/'+str(actor_id)+'', headers=self.director,
                                       json={'name': 'rawan',
                                             'age': 21, 'gender': 'female'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
