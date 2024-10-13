# **Cheshire Captures API**

# Testing

## Table of Contents

* [**Testing**](<#testing>)
    * [Code Validation](<#code-validation>)
    * [Automatic Testing](<#automatic-testing>)
    * [Manual Testing](<#manual-testing>)
    * [Known Bugs](<#known-bugs>)

## Code Validation 

### PEP8

The Cheshire Captures API has been validated using PEP8 compliance checks. Here are the steps I followed for validation using pycodestyle:

1. Install pycodestyle using the command: `pip3 install pycodestyle`
2. Press `Ctrl+Shift+P` in GitPod.
3. Type "linter" and select `Python: Select Linter`.
4. Choose `pycodestyle` from the list.
5. Open the "Problems" tab to see PEP8 violations, if any.

### API Files

* **Permissions**: No issues or warnings found.
* **Serializers**: No issues or warnings found.
* **Views**: No issues or warnings found.
* **Models**: No issues or warnings found.
* **Urls**: No issues or warnings found.

### App-Specific Files

#### Photographers App:
* **models.py**: No issues or warnings found.
* **serializers.py**: No issues or warnings found.
* **views.py**: No issues or warnings found.
* **urls.py**: No issues or warnings found.
* **tests.py**: No issues or warnings found.

#### Photos App:
* **models.py**: No issues or warnings found.
* **serializers.py**: No issues or warnings found.
* **views.py**: No issues or warnings found.
* **urls.py**: No issues or warnings found.
* **tests.py**: No issues or warnings found.

#### Comments App:
* **models.py**: No issues or warnings found.
* **serializers.py**: No issues or warnings found.
* **views.py**: No issues or warnings found.
* **urls.py**: No issues or warnings found.
* **tests.py**: No issues or warnings found.

#### Likes App:
* **models.py**: No issues or warnings found.
* **serializers.py**: No issues or warnings found.
* **views.py**: No issues or warnings found.
* **urls.py**: No issues or warnings found.
* **tests.py**: No issues or warnings found.

#### Ratings App:
* **models.py**: No issues or warnings found.
* **serializers.py**: No issues or warnings found.
* **views.py**: No issues or warnings found.
* **urls.py**: No issues or warnings found.
* **tests.py**: No issues or warnings found.

## Automated Testing

Automated tests were written to cover various user stories and functionality within the Cheshire Captures API. 

In addition to Django's built-in testing framework, the API was tested with **Postman** to ensure that the endpoints returned the correct responses, and **Swagger** was integrated to provide an easy-to-navigate API documentation and test interface.

![Automatic Test Summary](images/test-summary.png)

### **Profiles**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Profile is automatically created on user registration. |
| &check; | Can retrieve profile using valid ID. |
| &check; | Cannot retrieve profile with invalid ID. |
| &check; | Can update own profile. |
| &check; | Cannot update someone else's profile. |
| &check; | Can delete own profile. |
| &check; | Cannot delete someone else's profile. |

### **Photos**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can list all photos. |
| &check; | Logged in user can upload photo. |
| &check; | Cannot retrieve photo with invalid ID. |
| &check; | Can update own photo. |
| &check; | Cannot update someone else's photo. |
| &check; | Can delete own photo. |
| &check; | Cannot delete someone else's photo. |

### **Likes**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can like a photo. |
| &check; | Can remove like from a photo. |
| &check; | Cannot like a photo more than once. |

### **Comments**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can post a comment. |
| &check; | Can delete own comment. |
| &check; | Cannot delete someone else's comment. |

### **Ratings**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can rate a photo. |
| &check; | Cannot rate the same photo twice. |
| &check; | Can update own rating. |

### **Followers**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can follow a photographer. |
| &check; | Can unfollow a photographer. |
| &check; | Cannot follow the same photographer twice. |

## Manual Testing

In addition to the automated tests, I performed manual testing using **Postman** to verify the behavior of the API under different conditions, such as ensuring that invalid requests return appropriate error responses and that correct data is returned when valid requests are made. Swagger also provided a convenient way to manually interact with the API.

### **Profiles**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can filter profile list by number of followers. |
| &check; | Can sort profiles by number of photos uploaded. |
| &check; | Can sort profiles by location. |

### **Photos**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can filter photos by category. |
| &check; | Can search photos by title and tags. |
| &check; | Can sort photos by date uploaded. |

### **Comments**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Comments can be filtered by photo. |

### **Ratings**
| Status | Test Description |
|:-------:|:----------------|
| &check; | Can filter ratings by photo. |

## Known Bugs

Bug tracking for the Cheshire Captures project has been closely monitored using the GitHub Project Board. All bugs and feature requests are organized into various states such as "To Do," "In Progress," "Testing," and "Done" to ensure efficient project management and prioritization.

### Tracking Bugs on GitHub Project Board

The following bugs were identified during the development of Cheshire Captures:

- **Not possible to add comments to photos** – Bug related to the comment functionality where users cannot leave comments on photos.
- **Like button non-functional** – The like button on photo details pages does not trigger the required backend functionality.
- **Filter not working on My Photos page** – Filter functionality on the "My Photos" page is not returning the correct results.
- **Unfollow option not available** – A bug prevents users from unfollowing photographers due to an issue with the follow button.
- **Unable to unlike a photo** – Users face an authentication error when trying to unlike a previously liked photo.
- **Cannot edit or delete comments** – Authentication-related issue causing users to be unable to edit or delete their own comments.
- **Followers page not returning** – Clicking on the "View Followers" option does not display the correct followers page.
- **Can't submit a rating** – Users are unable to submit ratings for photos due to a server-side issue.

### Additional Bugs from the GitHub Board:

- **Profile NavBar** – Issues with the navbar layout when viewing profiles.
- **Search functionality not working** – Search does not work on the Gallery and Popular Photographers pages.
- **Unable to sign out** – Users face an error when trying to sign out.
- **Unable to change password** – Authentication error prevents users from changing their passwords.
- **Initial home page load presents 401 error** – A 401 authentication error occurs when loading the home page before a user is authenticated.

These bugs were tracked and categorized according to severity, and each was assigned to a developer for resolution. You can view the full backlog, roadmap, and specific bug details on the GitHub Project Board. This allowed for efficient tracking and ensured that bugs were either addressed or marked for future iterations based on priority.

### Resolved Bugs

1. **Profile deletion issue** – Deleting profiles did not remove associated photos. This was resolved by adding cascading delete functionality to the `Photo` model.
2. **Duplicate likes** – Users could like a photo multiple times. This was fixed by implementing a uniqueness constraint on the `Like` model.
3. **Rating system bug** – Users could rate a photo more than once. The issue was resolved by enforcing uniqueness constraints between `user` and `photo` in the `PhotoRating` model.

![Resolved Bug Example](images/resolved-bug.png)

For a full list of bugs and features, please refer to the [GitHub Project Board](https://github.com/users/NickCMoore/projects/2).


For more details on testing and deployment, return to the [README file](README.md).
