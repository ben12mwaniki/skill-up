
# skillUp
## Introduction
This application is a platform for developers to create and share learning resources (video, book, course, blog, podcast, forum etc). The resources are shared as a hyperlink and additional details can be added when the resource is created to help with querying. No account is needed to search resources. However, an account is necessary to be able to create, save or rate a resource. 
The web app can be found [here](https://skillup-1-a33a20b30d96.herokuapp.com/).

## Prerequisites
* Python 3
* pip
* See [Configuring database](#configuring-database-and-environment-variables)

## Set-up and configuration
* Fork repository
* Create a virtual environment while in project root `py -m venv .venv`

_Important: Always a good idea to work in a virtual environment to not mess up with other python installations or dependencies_

* Activate the virtual environment

  <div align="center">

  | OS | How |
  | ---- | ----------- |
  | Windows | .venv\Scripts\activate |
  | Linux/Mac    |source .venv/bin/activate |

  </div>

Use `deactivate` to deactivate the virtual environment anytime

* While in root, install dependencies in `requirements.txt` by running `pip install -r requirements.txt`

* Navigate to skillup `cd skillup`
* Run the server using `python manage.py runserver`

If `python` doesn't work, try `python3`

### Configuring database and environment variables
A database must be configured for the server to be run successfully. This project is set to use a `.env` file to connect to databases. In fact 2 databases are used: MongoDB for resources, Postgres for user authentication and profile models. Your `.env` file should have these variables:

<div align="center">

  | Variable | Value| Purpose |
  | ---- | ----------- | ----- |
  | SECRET_KEY | a random string with >= 50 characters | Ensure integrity and authenticity of signed data e.g. session cookies |
  | MONGO_URI   | MongoDB connection information | Connecting with MongoDB which stores resources collection |
  | POSTGRES_URI   | Postgres connection information | Connecting with Postgres database which stores user and profile data |

</div>

_Note: You can use different databases/connection variables i.e. `HOST`, `USER`, `DATABASE` etc. However, you have to modify the project. Specifically, navigate to `settings.py` and `views.py` and change places with `os.getenv(<str>)` accordingly._

## Project Status
Some features to be added:
* Authentication with socials
* Add machine learning for making recommendations based on user activity

## Known Issues
* Dark mode not retained when navigating to another page

Feel free to report other issues to ben12mwaniki@proton.me


