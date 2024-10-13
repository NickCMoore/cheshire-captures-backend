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

### Resolved Bugs

1. **Profile deletion issue**: During testing, deleting profiles did not remove the associated photos. This was resolved by adding a cascading delete on the `Photo` model.
2. **Duplicate likes**: Users were able to like a photo more than once due to a missing uniqueness constraint on the `Like` model. This was resolved by adding a unique constraint between `user` and `photo`.
3. **Rating system**: Initially, users could rate a photo multiple times. After updating the `PhotoRating` model with a uniqueness constraint for `user` and `photo`, this issue was resolved.

![Resolved Bug Example](images/resolved-bug.png)

For more details on testing and deployment, return to the [README file](README.md).
