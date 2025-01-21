# BrewBlog

BrewBlog is a Flask-based web application designed to manage and showcase breweries and their beers. The application provides a RESTful API for creating, retrieving, updating, and deleting breweries and beers. It also includes authentication and authorization using Auth0, and supports various beer styles.

The API has been deployed as a service to Render at the live URL https://brewblog-api.onrender.com/. Most routes require authentication, but a public example of the endpoint can be accessed at [https://brewblog-api.onrender.com/api/styles](https://brewblog-api.onrender.com/api/styles). See the [Postman](#postman) section for details on testing the live endpoints.

A React frontend is also configured, and is live at [https://brewblog-react.onrender.com/](https://brewblog-react.onrender.com/). The React project can be found at [https://github.com/mattgaskey/brewblog-react](https://github.com/mattgaskey/brewblog-react). See the [Auth0](#auth0) section for details on authenticating to the React frontend.

- [Features](#features)
- [Installation](#installation)
- [Deployment](#deployment)
- [Postman](#postman)
- [Auth0](#auth0)
  - [Drinker](#drinker)
  - [Brewer](#brewer)
- [API Endpoints](#api-endpoints)
  - [Breweries](#breweries)
  - [Beers](#beers)
  - [Styles](#styles)

## Features

- **Brewery Management**: Create, retrieve, and update breweries.
- **Beer Management**: Create, retrieve, and delete beers associated with breweries.
- **Beer Styles**: Predefined DB of beer styles.
- **Authentication and Authorization**: Secure API endpoints using Auth0.
- **Database**: Uses PostgreSQL for data storage.
- **Testing**: Unit tests for API endpoints.

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/mattgaskey/brewblog-api.git
    cd brewblog-api
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:

    Run the `setup.sh` script.

5. **Run the application**:

    You will need a running Postgres server in order to access db functionality.

    ```sh
    flask db migrate
    python3 seed.py
    flask run
    ```

### Dependencies

The following dependencies will be installed for the Falsk application:

```sh
alembic==1.14.0
Authlib==1.4.0
blinker==1.9.0
certifi==2024.12.14
cffi==1.17.1
charset-normalizer==3.4.1
click==8.1.8
cryptography==44.0.0
ecdsa==0.19.0
Flask==3.1.0
Flask-Cors==5.0.0
Flask-Login==0.6.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
greenlet==3.1.1
gunicorn==23.0.0
idna==3.10
itsdangerous==2.2.0
Mako==1.3.8
MarkupSafe==3.0.2
packaging==24.2
postgres==4.0
psycopg2-binary==2.9.10
psycopg2-pool==1.2
pyasn1==0.6.1
pycparser==2.22
PyJWT==2.10.1
python-dotenv==1.0.1
python-jose==3.3.0
requests==2.32.3
rsa==4.9
six==1.17.0
SQLAlchemy==2.0.36
typing_extensions==4.12.2
urllib3==2.3.0
Werkzeug==3.1.3
WTForms==3.2.1
```

## Deployment

The API is deployed as a service to [Render](https://render.com).  Steps to deploy are extremely simple:

1. Create a Render account if you haven't already.  There are free tiers for most services, so no payment is required.
2. Once you are logged in, you will be redirected to the Render Dashboard. Click the New PostgreSQL button to set up a Postgres cloud database.  Give the service a name, select the Free tier and deploy the DB service.
3. Once the database is set up, we can go back to Render Dashboard and create a new Web Service.
4. Connect this GitHub repo to the Web Service.  Choose Public Git Repository, and paste in `https://github.com/mattgaskey/brewblog-api`.
5. Once connected, give the service a name, select the Free tier, and enter the following command in the Build Command field:

  ```sh
  pip install -r requirements.txt && flask db upgrade && python3 seed.py
  ```

6. Add environment variables from the `setup.sh` file to the Web Service configuration.  Make sure to use DB credentials from the PostgresQL DB service we just created for `SQLALCHEMY_DATABASE_URI`. Save and deploy the service.

Any time the API code is updated and pushed to GitHub, the Web Service needs to be redeployed in Render.  From the service screen, select `Manual Deploy > Deploy Latest Commit`.  Should the service go to sleep (a factor with the Free Tier), you can restart the service selecting `Manual Deploy > Restart service`.

## Postman

To test the live API endpoint, import the `BrewBlog_API.postman_collection.json` file into Postman.  You can update the endpoint variable if you have deployed the app yourself, or leave it as is to test against my deployment.

## Auth0

This API is secured with Auth0 Roles and Permissions.  There are two roles defined for this applicaiton: Brewer and Drinker. The Brewer role has full permissions, and acts as a kind of admin for the site.  The Drinker role has limited permissions, analogous to an authenticated user role.  

The React app contains a public search feature that requires no authentication, and returns brewery search results from an open API source at [https://www.openbrewerydb.org/](https://www.openbrewerydb.org/).

A test account has been created for each role, the details of which can be found in the `auth0_details.json` file in this repo.  Use these credentials to log in to the application via Auth0 redirects.

### Drinker

Permissions for the Drinker role:

- `create:breweries`: Allows a user to save a Brewery from the search list to the DB.
- `create:beers`: Allows a user to add a Beer to an existing Brewery in the DB.
- `get:breweries`: Allows a user to get the list of existing Brewery entities in the DB.

### Brewer

A Brewer has all the permission a Drinker has, plus:

- `edit:breweries`: Allows a user to update the details of an exiting Brewery in the DB.
- `delete:beers`: Allows a user to delete a Beer from an existing Brewery in the DB.

## API Endpoints

API endpoints can be fully tested using the `BrewBlog_API.postman_collection.json` file in the repo. Simply import into Postman, and send the predefined requests. Auth Tokens are included in the environment.

### Breweries

- `GET /api/breweries`:
  - **Description**: Retrieve a list of breweries. Breweries are sorted into areas by City, State.
  - **Required Permissions**: `get:breweries`
  - **Response**: JSON array of breweries.

  ```json
  [
    {
      "id": "1",
      "name": "Test Brewery",
      "address": "123 Test St",
      "city": "Test City",
      "state": "ND",
      "phone": "123-456-7890",
      "website_link": "http://testbrewery.com",
      "beers": [
        {
          "beer_id": 1,
          "beer_name": "Test Beer",
          "beer_style": "IPA",
          "beer_description": "A test beer"
        }
      ],
      "beers_count": 1
    }
  ]
  ```

- `POST /api/breweries/create`:
  - **Description**: Create a new brewery.
  - **Required Permissions**: `create:breweries`
  - **Request Body**:

  ```json
  {
    "id": "string",
    "name": "string",
    "address": "string",
    "city": "string",
    "state": "string",
    "phone": "string",
    "website_link": "string"
  }
  ```  

  - **Response**: JSON object of the created brewery.

  ```json
  {
    "id": "2",
    "name": "New Brewery",
    "address": "456 New St",
    "city": "New City",
    "state": "NC",
    "phone": "987-654-3210",
    "website_link": "http://newbrewery.com",
    "beers": [],
    "beers_count": 0
  }
  ```

- `GET /api/breweries/<brewery_id>`:
  - **Description**: Retrieve details of a specific brewery.
  - **Required Permissions**: get:breweries
  - **Response**: JSON object of the brewery.

  ```json
  {
    "id": "1",
    "name": "Test Brewery",
    "address": "123 Test St",
    "city": "Test City",
    "state": "ND",
    "phone": "123-456-7890",
    "website_link": "http://testbrewery.com",
    "beers": [
      {
        "beer_id": 1,
        "beer_name": "Test Beer",
        "beer_style": "IPA",
        "beer_description": "A test beer"
      }
    ],
    "beers_count": 1
  }
  ```

- `PATCH /api/breweries/<brewery_id>/edit`:
  - **Description**: Update an existing brewery.
  - **Required Permissions**: `edit:breweries`
  - **Request Body**:

  ```json
  {
    "name": "string",
    "address": "string",
    "city": "string",
    "state": "string",
    "phone": "string",
    "website_link": "string"
  }
  ```

  - **Response**: JSON object of the updated brewery.

  ```json
  {
    "id": "1",
    "name": "Updated Brewery",
    "address": "123 Updated St",
    "city": "Updated City",
    "state": "US",
    "phone": "123-456-7890",
    "website_link": "http://updatedbrewery.com",
    "beers": [
      {
        "beer_id": 1,
        "beer_name": "Test Beer",
        "beer_style": "IPA",
        "beer_description": "A test beer"
      }
    ],
    "beers_count": 1
  }
  ```

### Beers

- `GET /api/breweries/<brewery_id>/beers`:
  - **Description**: Retrieve a list of beers for a specific brewery.
  - **Required Permissions**: get:breweries
  - **Response**: JSON array of beers.

  ```json
  [
    {
      "id": 1,
      "name": "Test Beer",
      "style": "IPA",
      "description": "A test beer",
      "brewery_id": "1"
    }
  ]
  ```

- `POST /api/beers/create`:
  - **Description**: Create a new beer.
  - **Required Permissions**: `create:beers`
  - **Request Body**:

  ```json
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "style_id": "string",
    "brewery_id": "string"
  }
  ```

  - **Response**: JSON object of the created beer.

  ```json
  {
    "id": "999",
    "name": "Cool New Beer",
    "style": "IPA",
    "description": "A cool new beer with a cool flavor profile.",
    "brewery_id": "64f90c02-c3f8-4dec-a7c1-ea176b161d88"
  }
  ```

- `POST /api/beers/<beer_id>/delete`:
  - **Description**: Delete a beer.
  - **Required Permissions**: `delete:beers`
  - **Response**: JSON object with a success message.

  ```json
  {
    "message": "Beer deleted successfully."
  }
  ```

### Styles

- `GET /api/styles`:
  - **Description**: Retrieve a list of beer styles.
  - **Response**: JSON array of beer styles.

  ```json
  [
    {
      "id": 1,
      "name": "IPA"
    },
    {
      "id": 2,
      "name": "Stout"
    }
  ]
  ```
