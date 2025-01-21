# BrewBlog

BrewBlog is a Flask-based web application designed to manage and showcase breweries and their beers. The application provides a RESTful API for creating, retrieving, updating, and deleting breweries and beers. It also includes authentication and authorization using Auth0, and supports various beer styles.

The API can be accessed live at [https://brewblog-api.onrender.com/](https://brewblog-api.onrender.com/). A React frontend is also configured, and is live at [https://brewblog-react.onrender.com/](https://brewblog-react.onrender.com/). The React project can be found at [https://github.com/mattgaskey/brewblog-react](https://github.com/mattgaskey/brewblog-react).

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

## Auth0

This API is secured with Auth0 Roles and Permissions.  There are two roles defined for this applicaiton: Brewer and Drinker. The Brewer role has full permissions, and acts as a kind of admin for the site.  The Drinker role has limited permissions, analogous to an authenticated user role.  

The React app contains a public search feature that requires no authentication, and returns brewery search results from an open API source at [https://www.openbrewerydb.org/](https://www.openbrewerydb.org/).

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
