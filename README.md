# SkillUp

SkillUp is a tech learning-resource sharing platform built with Django. It allows developers to discover, organize, and share educational resources such as courses, books, videos, blogs, podcasts, and forums.

Users can browse and search resources without an account. Registered users can create resources, save resources to their profile, rate and comment on resources, and manage the resources they have created.

**Live application:** 
[SkillUp](https://skill-up-pf3i.onrender.com/)

## Features

* **User accounts** — Register, log in, and securely manage sessions using Django's authentication system.
* **User profiles** — Maintain an About section and view saved and created resources.
* **Resource creation** — Share learning resources with a title, type, link, subjects, and description.
* **Resource discovery** — Search resources using keywords or filter by resource type.
* **Full-text search** — Search across resource titles, subjects, and descriptions.
* **Save resources** — Bookmark resources for quick access from a personal profile.
* **Ratings** — Rate resources from 1–5 stars and update an existing rating.
* **Comments** — Add comments and interact with shared resources.
* **Resource management** — Authors can delete resources they have created.
* **Access control** — Authentication and authorization rules protect user-specific actions and resource ownership.

## Technology Stack

| Technology              | Purpose                                    |
| ----------------------- | ------------------------------------------ |
| Python                  | Application programming language           |
| Django 4.2.30           | Web framework and application architecture |
| PostgreSQL              | User authentication and profile data       |
| MongoDB                 | Learning resource data                     |
| Psycopg                 | PostgreSQL database connectivity           |
| HTML / CSS / JavaScript | Frontend                                   |
| WhiteNoise              | Static file serving                        |
| Gunicorn                | Production application server              |
| Render                  | Application hosting                        |

### Data Architecture

SkillUp uses both PostgreSQL and MongoDB, with each database serving a different purpose:

* **PostgreSQL** stores Django's built-in user accounts and the application's `Profile` records.
* **MongoDB** stores learning resources, including their metadata, ratings, and comments.

This architecture allowed the application to leverage Django's built-in authentication while retaining MongoDB's flexible document model for resource content.

## Getting Started

### Prerequisites

* Python 3
* pip
* PostgreSQL
* MongoDB
* Git

### Installation

1. Clone or fork the repository.

2. Create a virtual environment from the project root:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.

   **Windows:**

   ```bash
   .venv\Scripts\activate
   ```

   **macOS / Linux:**

   ```bash
   source .venv/bin/activate
   ```

4. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and configure the required environment variables.

6. Navigate to the Django project:

   ```bash
   cd skillup
   ```

7. Apply the Django migrations:

   ```bash
   python manage.py migrate
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`.

## Configuration

SkillUp uses environment variables for sensitive configuration and database connection information.

Create a `.env` file in the project root:

| Variable       | Purpose                                                               |
| -------------- | --------------------------------------------------------------------- |
| `SECRET_KEY`   | Django secret key used for cryptographic signing and session security |
| `POSTGRES_URI` | PostgreSQL connection string used by Django                           |
| `MONGO_URI`    | MongoDB connection string used for learning resources                 |

Example:

```env
SECRET_KEY=your-django-secret-key
POSTGRES_URI=postgresql://username:password@host:5432/database
MONGO_URI=mongodb+srv://username:password@host/database
```

Do not commit the `.env` file or expose database credentials in source control.

## Database Setup

PostgreSQL must be available before running the Django migrations:

```bash
python manage.py migrate
```

Django creates the tables required for authentication and user profiles.

MongoDB does not require Django migrations. The application connects to the configured MongoDB instance and uses the `skillupdb` database and `resources` collection for learning resources.

The application also creates a MongoDB text index covering:

* `title`
* `subjects`
* `description`

This index supports the platform's full-text resource search.

## User Workflow

### Discovering resources

Visitors can search for learning resources without creating an account. Searches can be performed using keywords, resource type, or both.

### Creating an account

Creating an account enables access to user-specific features such as saving, rating, and commenting on resources.

### Sharing a resource

Authenticated users can create a resource by providing:

* Title
* Resource type
* Link
* Subjects
* Description

The resource is associated with its author and stored in MongoDB.

### Saving and rating

Authenticated users can save resources to their profile and rate resources from 1–5 stars.

Users cannot save or rate resources they created themselves.

### Managing resources

Authors can delete their own resources. When a resource is deleted, it is also removed from users' saved-resource lists to prevent stale references.

## Project Status

SkillUp is a completed personal project demonstrating full-stack web development with Django, PostgreSQL, and MongoDB.

Potential future improvements include:

## Future Improvements
* Semantic search — Add vector-based search to identify resources based on the meaning and context of a user's query rather than relying solely on keyword matching.
* Improved result ranking — Rank search results using resource ratings alongside search relevance, allowing highly rated resources to receive greater visibility while remaining relevant to the user's query.
* Social authentication — Allow users to register and sign in using third-party identity providers.
* Personalized recommendations — Recommend resources based on user activity, saved resources, and other engagement signals.
* Persistent UI preferences — Retain interface preferences such as dark mode across sessions and navigation.

## Known Issues

* Dark mode preferences are not currently retained when navigating between pages.
* The application currently relies on separate PostgreSQL and MongoDB databases, which adds deployment and configuration requirements.

## Contributors
* Ben Mwaniki (Project Lead)
* Yuvraj Singh 

## License

This project is available for educational and portfolio purposes.
