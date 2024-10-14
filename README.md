# **Cheshire Captures API**

## Table of Contents

- [Project](#project)
  * [Objective](#objective)
  * [Links to Deployed Project](#links-to-deployed-project)
- [Project Structure](#project-structure)
  * [Developer User Stories](#developer-user-stories)
    + [Profiles](#profiles)
    + [Photos](#photos)
    + [Comments](#comments)
    + [Likes](#likes)
    + [Followers](#followers)
    + [Search and Filter](#search-and-filter)
    + [Ratings and Reviews](#ratings-and-reviews)
- [Database Design](#database-design)
  * [Models](#models)
- [Features](#features)
  * [Homepage](#homepage)
  * [Profile Data](#profile-data)
  * [Photos Data](#photos-data)
  * [Comments Data](#comments-data)
  * [Likes Data](#likes-data)
  * [Followers Data](#followers-data)
  * [Ratings and Reviews Data](#ratings-and-reviews-data)
- [Agile Workflow](#agile-workflow)
  * [Github Project Board](#github-project-board)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

# **Project**

## Objective

**Cheshire Captures API** provides a backend database to manage user profiles, photo uploads, comments, likes, follows, and reviews for the Cheshire Captures platform. The API allows photographers and enthusiasts to interact with each other by sharing their work, following profiles, leaving comments, and rating photos.

The API includes search and filter functionality to enhance user experience, enabling users to easily find photographers or photos of interest.

## Links to Deployed Project

  + The project is deployed on Heroku: [Deployed Cheshire Captures API](https://cheshire-captures-backend-084aac6d9023.herokuapp.com/)
  + The front-end of the project is available at: [Cheshire Captures Front End](https://cheshire-captures-4a500dc7ab0a.herokuapp.com/)

## Project Structure

The structure of this project follows the **Code Institute DRF Walkthrough** for backend API development and the **Moments Walkthrough** for building a React front-end. Additional custom models and logic have been developed to tailor this platform to its unique purpose of sharing and showcasing photography.

## Developer User Stories

### Profiles

- As a user, I can create a profile upon registration, so that my profile is automatically generated and displayed.
- As a user, I can view all profiles to discover photographers on the platform.
- As a user, I can follow/unfollow other profiles to stay updated on their latest photos.
- As a user, I can edit my profile to update my bio, profile picture, and social links.

### Photos

- As a user, I can upload photos, so that they are displayed in the gallery.
- As a user, I can view all photos in the gallery to discover new work.
- As a user, I can search for specific photos by keywords or photographer names.
- As a user, I can filter photos by category to find photos related to my interests.

### Comments

- As a user, I can leave comments on photos to engage with the photographer's work.
- As a user, I can edit or delete my comments.
- As a user, I can view all comments on a specific photo to see what others are saying.

### Likes

- As a user, I can like photos to show appreciation for the content.
- As a user, I can remove my like if I change my mind.

### Followers

- As a user, I can follow/unfollow photographers to keep up with their work.
- As a user, I can view a list of all the users I follow.

### Search and Filter

- As a user, I can search for photos or photographers by keyword to find content that interests me.
- As a user, I can filter photos by category to narrow down my search results.

### Ratings and Reviews

- As a user, I can rate a photo from 1 to 5 stars to express my opinion on its quality.
- As a user, I can leave a review with a star rating for photos.

## Database Design

### Models

The following models have been developed for the Cheshire Captures API:

- **User**: Extends Django's User model.
- **Profile**: Automatically created upon user registration to store additional user information like bio and profile picture.
- **Photo**: Stores information related to each uploaded image.
- **Comment**: Allows users to comment on photos.
- **Like**: Tracks users who like specific photos.
- **Follow**: Handles the follower relationship between profiles.
- **Rating**: Stores star ratings for photos.
- **Review**: Stores user reviews with star ratings for photos.

The relationships between these models are illustrated in the following entity relationship diagram:
![ERD](https://link-to-your-ERD-image)

## Features

### Homepage

The API's root route welcomes users and provides links to the main API endpoints.

### Profile Data

Users can view and update their profiles. Profile data includes the user’s bio, profile picture, followers, and more.

### Photos Data

Users can upload, view, edit, and delete their photos. The gallery allows all users to browse the photos shared by the community.

### Comments Data

Users can view, add, edit, and delete comments on photos to engage with photographers and their work.

### Likes Data

Users can like photos to show appreciation and remove likes if desired.

### Followers Data

Users can follow/unfollow other photographers, helping them keep up with their favorite photographers' work.

### Ratings and Reviews Data

Users can rate and review photos to provide feedback to photographers. These ratings contribute to the "Top-Rated Photos" section.

## Agile Workflow

### GitHub Project Board

The project was managed using GitHub’s Kanban board to organize tasks based on user stories and development goals. Each feature was tracked and prioritized using the MoSCoW method.

![GitHub Project Board](https://github.com/users/NickCMoore/projects/3)

## Testing

Please refer to the [Testing Documentation](TESTING.md) for more detailed information on the testing process.

## Technologies Used

### Backend

- **Django (v5.1.2)**: The core Python web framework used to develop the backend of the application, enabling rapid and secure development.
- **Django REST Framework (v3.14.0)**: Provides powerful tools to create the RESTful API that connects the backend to the React frontend.
- **PostgreSQL**: A relational database system used to manage all data related to users, photos, comments, and interactions.
- **Cloudinary (v1.41.0)**: A cloud-based service used for storing and managing image uploads, making it easier to serve user-uploaded media across the platform.
- **Heroku**: The cloud platform used for deploying the backend of the project, ensuring scalability and reliable hosting.
- **Gunicorn (v20.1.0)**: A Python WSGI HTTP server used to run the Django application on Heroku in production.
- **Whitenoise (v6.7.0)**: Ensures efficient serving of static files directly from the Django application in production environments.

## Deployment

The project was deployed on Heroku. Below are the steps to deploy:

1. Create a new Heroku app.
2. Connect the Heroku app to your GitHub repository.
3. Add environment variables such as `DATABASE_URL`, `CLOUDINARY_URL`, and `SECRET_KEY`.
4. Deploy the app via Heroku’s manual deploy or enable automatic deploys from the `main` branch.

For more detailed instructions, please see the [Deployment Documentation](DEPLOYMENT.md).

## Credits

- The project structure was inspired by the **Code Institute DRF** and **Moments Walkthrough** projects.
- Special thanks to **Unsplash** for providing free, high-quality images for the platform.
- Thanks to **Cloudinary** for enabling seamless media file storage and hosting.
- Stack Overflow and other online resources provided valuable support throughout the development process.
