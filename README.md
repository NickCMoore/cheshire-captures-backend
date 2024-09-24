# Cheshire Captures - Backend API

Welcome to Cheshire Captures - a content-sharing platform designed to allow users to browse, comment, like, and share their photographic experiences with the Cheshire community. This project uses the Django REST Framework to build a robust backend API, providing a data interface for the front-end application built with React.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [API Endpoints](#api-endpoints)
5. [Database Schema](#database-schema)

## Project Overview

Cheshire Captures provides a platform for users to create, view, comment on, and like photographic content. Users can also follow each other to stay updated with the latest posts. The backend API supports all these functionalities and serves data to the front-end React application.

## Features

- **User Authentication:** Register, login, and manage user accounts.
- **Content Management:** Create, read, update, and delete posts.
- **User Interactions:** Comment on posts, like posts, and follow users.
- **Pagination:** Efficient data handling through pagination for all list views.
- **JWT Authentication:** Secure user authentication using JSON Web Tokens.
- **Search and Filter:** Search posts and filter by categories, popularity, and more.

## Technologies Used

- **Backend Framework:** Django REST Framework
- **Authentication:** Django AllAuth, dj-rest-auth, SimpleJWT
- **Database:** PostgreSQL (for production), SQLite (for development)
- **Storage:** Cloudinary for image storage
- **Deployment:** Heroku
- **Others:** Django Filters, CORS Headers

## API Endpoints

### Authentication

- `POST /dj-rest-auth/login/` - Login a user.
- `POST /dj-rest-auth/logout/` - Logout a user.
- `POST /dj-rest-auth/registration/` - Register a new user.

### Posts

- `GET /posts/` - Retrieve a list of posts with pagination.
- `POST /posts/` - Create a new post.
- `GET /posts/<id>/` - Retrieve a specific post.
- `PUT /posts/<id>/` - Update a specific post.
- `DELETE /posts/<id>/` - Delete a specific post.

### Comments

- `GET /comments/` - Retrieve a list of comments with pagination.
- `POST /comments/` - Create a new comment.
- `GET /comments/<id>/` - Retrieve a specific comment.
- `PUT /comments/<id>/` - Update a specific comment.
- `DELETE /comments/<id>/` - Delete a specific comment.

### Likes

- `POST /likes/` - Like a post.
- `DELETE /likes/<id>/` - Unlike a post.

### Followers

- `POST /followers/` - Follow a user.
- `DELETE /followers/<id>/` - Unfollow a user.
