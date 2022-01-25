# CRUD Users handling coding challenge

The following deposit contains the code required for the coding challenge to handle CRUD on Users with their informations (IBAN, ...).

This project used Django and the Django REST Framework as well as Docker and PostgreSQL.

## Preparing and launching the project and tests

### Set your own user, password and database for PostgreSQL

You can set your own user, password and database name for PostgreSQL by editing the `docker-compose.yml` file and updating the following environment variables for *both* containers (backend and db): `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.


### Running and executing the tests
From the README folder.

Running the server :

```
$> docker-compose up
```
The server can then be accessed through https://localhost:8000/

Running the test (as the container is running, in a second terminal):
```
$> docker-compose exec backend sh
# python manage.py test
```

## Endpoints
`/__admin__/`: Classical Django administration page.\\
NB: A default admin is created (root/password)

`/admins/`: List of admin created.

`/admins/<admin_id>`: Get informations on a specific admin

`/users/` : Get a list of users created (GET) or create a new user (POST)

The admin needs to be authenticated to create a new user.

Expected input should be formatted as follows:
```json
{
    "first_name": "Firstname",
    "last_name": "Lastname",
    "iban": "IBANWITHNUMBERS12312"
}
```

`/users/<user_id>` : Get a specific user (GET), update it (PUT) or delete it (DELETE)
Only the admin that created the user can update it or delete it.

## Details on the project's architecture

The main app is `users_handler`.

/users/ and /admins/ endpoints are handled in a separated app (`users_bank`).


## Generates documentation

Classes and methods were documented using docstring.
Sphinx can be used to generate a user-friendly code documentation from this.


