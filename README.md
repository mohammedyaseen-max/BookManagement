# Book Management System

A web-based Book Management System built with Flask and PostgreSQL. The application is containerized using Docker and Docker Compose and published on Docker Hub.

## Features

- Add books with a title and author.
- View all stored books.
- Delete books.
- Automatically create the database table when the application starts.
- Persist database data using a Docker named volume.
- Run the application and database in separate containers.

## Technologies

- Python
- Flask
- PostgreSQL 16
- psycopg2
- Gunicorn
- Docker
- Docker Compose

## Project Structure

```text
BookManagement/
|-- app.py
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- .dockerignore
|-- .gitignore
|-- .env.example
|-- .env (created locally; not committed)
`-- README.md
```

## Docker Hub

Repository: https://hub.docker.com/r/mohammedmoneer1998/book-management

Image: `mohammedmoneer1998/book-management:v1.1`

Pull the image:

```bash
docker pull mohammedmoneer1998/book-management:v1.1
```

## Requirements

- Docker Desktop
- Docker Compose
- A web browser

## Configuration

Create a local `.env` file in the project directory using `.env.example` as a template. Do not commit `.env` or publish real credentials.

Example configuration:

```dotenv
POSTGRES_DB=bookdb
POSTGRES_USER=bookuser
POSTGRES_PASSWORD=replace_with_a_strong_password
DATABASE_URL=postgresql://bookuser:replace_with_a_strong_password@db:5432/bookdb
```

The username, password, and database name in `DATABASE_URL` must match the PostgreSQL configuration.

Use a strong password for real deployments.

## Run the Application

1. Open a terminal in the project directory.
2. Create and configure the `.env` file.
3. Start the services:

```bash
docker compose up -d
```

4. Check the service status:

```bash
docker compose ps
```

5. Open the application in your browser:

http://localhost:5000

## Database

The application connects to PostgreSQL using `DATABASE_URL`.

The `books` table contains:

- `id`: Auto-generated primary key.
- `title`: Book title, up to 200 characters.
- `author`: Author name, up to 150 characters.

The application initializes the table when it starts.

## Data Persistence

Docker Compose uses the named volume `postgres_data` to store PostgreSQL data. Data persists when containers are stopped or recreated, as long as the volume is retained.

**Warning:** Do not use `docker compose down -v` unless you intend to delete the database volume and its stored data.

## Useful Commands

Check running services:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs --tail=100 web
```

View database logs:

```bash
docker compose logs --tail=100 db
```

Restart services:

```bash
docker compose restart
```

Stop and remove containers without deleting the named volume:

```bash
docker compose down
```

## Security

- Never commit `.env` or publish real credentials.
- Keep `.env` excluded through `.gitignore` and `.dockerignore`.
- Use strong database passwords.
- Do not expose PostgreSQL publicly unless required and properly secured.

## Author

Mohammed Muneer Yaseen