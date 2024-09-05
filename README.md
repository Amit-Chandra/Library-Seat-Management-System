# Library Seat Management System API

This API provides endpoints to manage libraries, seats, and user authentication in the Library Seat Management System. The system is built using Django and Django REST Framework, and it uses JWT (JSON Web Token) for authentication.

## Table of Contents

- [Authentication](#authentication)
  - [Obtain Token](#obtain-token)
  - [Refresh Token](#refresh-token)
- [Libraries](#libraries)
  - [List Libraries](#list-libraries)
  - [Create Library](#create-library)
  - [Retrieve Library Details](#retrieve-library-details)
  - [Update Library](#update-library)
  - [Delete Library](#delete-library)
- [Seats](#seats)
  - [List Seats](#list-seats)
  - [Create Seat](#create-seat)
  - [Retrieve Seat Details](#retrieve-seat-details)
  - [Update Seat](#update-seat)
  - [Delete Seat](#delete-seat)

## Authentication

### Obtain Token

Use this endpoint to obtain an access and refresh token by providing your username and password.

- **Endpoint**: `/api/token/`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **Response**:

  ```json
  {
    "refresh": "your_refresh_token",
    "access": "your_access_token"
  }
  ```

### Refresh Token

Use this endpoint to obtain a new access token using a refresh token.

- **Endpoint**: `/api/token/refresh/`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

- **Response**:

  ```json
  {
    "access": "new_access_token"
  }
  ```

## Libraries

### List Libraries

Retrieve a list of all libraries.

- **Endpoint**: `/library/api/libraries/`
- **Method**: `GET`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  [
    {
      "id": 1,
      "name": "Central Library",
      "location": "Main Campus",
      "total_seats": 100,
      "available_seats": 25
    },
    
  ]
  ```

### Create Library

Create a new library. Only super admins are allowed to create libraries.

- **Endpoint**: `/library/api/libraries/`
- **Method**: `POST`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Request Body**:

  ```json
  {
    "name": "New Library",
    "location": "South Campus",
    "total_seats": 50
  }
  ```

- **Response**:

  ```json
  {
    "id": 2,
    "name": "New Library",
    "location": "South Campus",
    "total_seats": 50,
    "available_seats": 50
  }
  ```

### Retrieve Library Details

Retrieve details of a specific library by its ID.

- **Endpoint**: `/library/api/libraries/{id}/`
- **Method**: `GET`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  {
    "id": 1,
    "name": "Central Library",
    "location": "Main Campus",
    "total_seats": 100,
    "available_seats": 25
  }
  ```

### Update Library

Update details of a specific library. Only super admins can update library details.

- **Endpoint**: `/library/api/libraries/{id}/`
- **Method**: `PUT`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Request Body**:

  ```json
  {
    "name": "Updated Library",
    "location": "North Campus",
    "total_seats": 150
  }
  ```

- **Response**:

  ```json
  {
    "id": 1,
    "name": "Updated Library",
    "location": "North Campus",
    "total_seats": 150,
    "available_seats": 150
  }
  ```

### Delete Library

Delete a specific library. Only super admins can delete a library.

- **Endpoint**: `/library/api/libraries/{id}/`
- **Method**: `DELETE`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  {
    "detail": "Library deleted successfully."
  }
  ```

## Seats

### List Seats

Retrieve a list of all seats in a specific library.

- **Endpoint**: `/library/api/libraries/{library_id}/seats/`
- **Method**: `GET`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  [
    {
      "id": 1,
      "number": "A-01",
      "is_booked": false
    },
    
  ]
  ```

### Create Seat

Create a new seat in a specific library. Only admins of that library or super admins can create seats.

- **Endpoint**: `/library/api/libraries/{library_id}/seats/`
- **Method**: `POST`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Request Body**:

  ```json
  {
    "number": "B-02"
  }
  ```

- **Response**:

  ```json
  {
    "id": 2,
    "number": "B-02",
    "is_booked": false
  }
  ```

### Retrieve Seat Details

Retrieve details of a specific seat by its ID.

- **Endpoint**: `/library/api/libraries/{library_id}/seats/{id}/`
- **Method**: `GET`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  {
    "id": 1,
    "number": "A-01",
    "is_booked": false
  }
  ```

### Update Seat

Update details of a specific seat. Only admins of that library or super admins can update seat details.

- **Endpoint**: `/library/api/libraries/{library_id}/seats/{id}/`
- **Method**: `PUT`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Request Body**:

  ```json
  {
    "number": "A-01",
    "is_booked": true
  }
  ```

- **Response**:

  ```json
  {
    "id": 1,
    "number": "A-01",
    "is_booked": true
  }
  ```

### Delete Seat

Delete a specific seat. Only admins of that library or super admins can delete a seat.

- **Endpoint**: `/library/api/libraries/{library_id}/seats/{id}/`
- **Method**: `DELETE`
- **Headers**:

  ```http
  Authorization: Bearer your_access_token
  ```

- **Response**:

  ```json
  {
    "detail": "Seat deleted successfully."
  }
  ```
