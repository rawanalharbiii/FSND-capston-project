# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. I am an Executive Producer within the company and am creating a system to simplify and streamline my process.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.


- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Running the server

From within the  directory first ensure you are working using your created virtual environment.

To run the server, execute:

source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

```
or just:

source setup.sh 
python app.py
```

## Roles and Permissions:
- Casting Assistant
    - Can view actors and movies
        - 'get:movies'
        - 'get:actors'    
 
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
        - 'post:actors'
        - 'delete: actors'
    - Modify actors or movies
        - 'patch:actors'
        - 'patch:movies'


- Executive Producer
   - All permissions a Casting Director has and…
   - Add or delete a movie from the database
        - 'post:movies'
        - 'delete:movie'

Note: Inssed `setup.sh` file we have a token for each role

## Deployment
The API is deployed on Heroku [project link](https://rawani.herokuapp.com/).

## Endpoints
- GET '/movies'
- GET '/actors'
- POST '/movies'
- POST '/actors'
- PATCH '/movies/<int:movie_id>'
- PATCH '/actors/<int:actor_id>'
- DELETE '/movies/<int:movie_id>'
- DELETE '/actors/<int:actor_id>'


GET '/movies'
- Fetches a dictionary of movies 
- Request Arguments: None
- Authentication: the roles that can acess are Casting Assistant, Casting Director and Executive Producer
- Returns: A JSON with list of movies objects, success value.

{
    "movies": [
        {
            "id": 8,
            "release date": "Thu, 21 Dec 2023 12:00:00 GMT",
            "title": "The Last Man Standing"
        },
        {
            "id": 9,
            "release date": "Thu, 21 Dec 2023 12:00:00 GMT",
            "title": "My ex wife"
        },
        {
            "id": 12,
            "release date": "Thu, 21 Dec 2023 12:00:00 GMT",
            "title": "The last ship"
        }
    ],
    "success": true
}
```

GET '/actors'
- Fetches a dictionary of actors 
- Request Arguments: None
- Authentication: the roles that can acess are Casting Assistant, Casting Director and Executive Producer
- Returns: A JSON with list of actors objects, success value.

{
    "actors": [
        {
            "age": 22,
            "gender": "Female",
            "id": 12,
            "name": "rawan"
        },
        {
            "age": 21,
            "gender": "Female",
            "id": 6,
            "name": "Elsa"
        }
    ],
    "success": true
}
```

POST '/movies'
- Post a movie and persist it to the database
- Request Arguments: A JSON with title, release_date  
- Authentication: Only the executive Executive Producer
- Returns : A JSON with success value and the id of the posted movie

{
    "movie id": 13,
    "success": true
}
```
POST '/actors'
- Post actor and persist it to the database
- Request Arguments: A JSON with name, age and gender  
- Authentication: Casting Director and  Executive Producer 
- Returns : A JSON with success value and the id of the posted actor

{
    "actor id": 13,
    "success": true
}
```
PATCH '/movies/<int:movie_id>'
- Updates a movie data based on the id 
- Request Arguments: A JSON with title and a release_date 
- Authentication: Casting Director and  Executive Producer 
- Returns : A JSON with success value and the id of the updated movie

{
    "movie_id": 2,
    "success": true
}
```
PATCH '/actors/<int:actor_id>'
- Updates an actor data based on the id 
- Request Arguments: A JSON with name, age and gender 
- Authentication: Casting Director and  Executive Producer 
- Returns : A JSON with success value and the id of the updated actor

{
    "actor id": 2,
    "success": true
}
```

DELETE '/movies/<int:movie_id>'
- Remove persistentle a movie from the database based on id 
- Request Arguments: id of the movie eg:'/movies/1'
- Returns: A JSON with success value and the id of the deleted movie

{
    "id": 2,
    "success": true
}
```
DELETE '/actors/<int:actor_id>'
- Remove persistentle an actor from the database based on id 
- Request Arguments: id of the actor eg:'/actors/1'
- Returns: A JSON with success value and the id of the deleted actror 


{
    "id": 12,
    "success": true
}
```

## API Testing
To run the tests:

python test_app.py

``` 

## Defined Error handlers:

400 - Bad reqest
401 - token expired / invalid claims / invalid header
404 - Resource not found
422 - Unprocessable entity

They have this format

{
    'success': False,
    'error': 404,
    'message': 'Resource not found'
}
