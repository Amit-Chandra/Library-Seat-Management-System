# Library Seat Management System


### 1. **Student Signup API** (`POST /studentsignup/`)
This API registers a new student.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8001/studentsignup/`
- **Headers:**
  - `Content-Type: application/json`
- **Body: (raw JSON)**
  ```json
  {
      "username": "john_doe",
      "password": "password123",
      "email": "john.doe@example.com",
      "school": "Sample School",
      "class": "10th Grade",
      "date_of_birth": "2005-09-15",
      "contact_number": "1234567890"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
      "message": "Student registered successfully"
  }
  ```

---

### 2. **Student Profile API** (`GET /profileview/`)
This API fetches the profile of the authenticated user.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8001/profileview/`
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  {
      "user": {
          "username": "john_doe",
          "email": "john.doe@example.com"
      },
      "role": "student"
  }
  ```

### **Update Student Profile API** (`PUT /profileview/`)
This API updates the student profile.

- **Method:** `PUT`
- **URL:** `http://127.0.0.1:8001/profileview/`
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
      "school": "New School Name",
      "class": "11th Grade",
      "contact_number": "9876543210"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
      "message": "Profile updated successfully"
  }
  ```

---

### 3. **Library List API** (`GET /librarieslist/`)
Fetches a list of all libraries.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8001/librarieslist/`
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  [
      {
          "id": 1,
          "name": "Central Library",
          "location": "Main St",
          "total_seats": 100
      },
      {
          "id": 2,
          "name": "Community Library",
          "location": "5th Ave",
          "total_seats": 50
      }
  ]
  ```

---

### 4. **Seat Availability API** (`GET /librarieslist/<library_id>/seats/`)
Gets seat availability for a specific library.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8001/librarieslist/1/seats/` (example for library ID `1`)
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  {
      "library": "Central Library",
      "seats": [
          {
              "id": 1,
              "seat_number": "A1",
              "is_available": true
          },
          {
              "id": 2,
              "seat_number": "A2",
              "is_available": false
          }
      ]
  }
  ```

---

### 5. **Approve Student API** (`POST /studentsapproval/<student_id>/approve/`)
Approves a student if their payment is confirmed.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8001/studentsapproval/1/approve/` (example for student ID `1`)
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  {
      "message": "Student approved successfully"
  }
  ```
- **Response Example (400 Bad Request):**
  ```json
  {
      "error": "Payment not confirmed"
  }
  ```

---

### 6. **Create Library API** (`POST /libraries/create/`)
Creates a new library (for admin users).

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8001/libraries/create/`
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
      "name": "New Library",
      "location": "Sample St",
      "total_seats": 40
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
      "id": 3,
      "name": "New Library",
      "location": "Sample St",
      "total_seats": 40
  }
  ```

---

### 7. **Retrieve Library API** (`GET /libraries/<library_id>/`)
Retrieves a specific library by ID.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8001/libraries/1/` (example for library ID `1`)
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  {
      "id": 1,
      "name": "Central Library",
      "location": "Main St",
      "total_seats": 100
  }
  ```

---

### 8. **Update Library API** (`PUT /libraries/update/<library_id>/`)
Updates an existing library (for admin users).

- **Method:** `PUT`
- **URL:** `http://127.0.0.1:8001/libraries/update/1/` (example for library ID `1`)
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
      "name": "Updated Library Name",
      "location": "Updated Location"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
      "id": 1,
      "name": "Updated Library Name",
      "location": "Updated Location",
      "total_seats": 100
  }
  ```

---

### 9. **Delete Library API** (`DELETE /libraries/delete/<library_id>/`)
Deletes a specific library (for admin users).

- **Method:** `DELETE`
- **URL:** `http://127.0.0.1:8001/libraries/delete/1/` (example for library ID `1`)
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (204 No Content):**
  ```json
  {
      "message": "Library deleted successfully"
  }
  ```

---

### 10. **List All Libraries API** (`GET /libraries/all/`)
Fetches a list of all libraries (same as LibraryListAPI).

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8001/libraries/all/`
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (200 OK):**
  ```json
  [
      {
          "id": 1,
          "name": "Central Library",
          "location": "Main St",
          "total_seats": 100
      },
      {
          "id": 2,
          "name": "Community Library",
          "location": "5th Ave",
          "total_seats": 50
      }
  ]
  ```

---

### JWT Authentication

Before testing the protected APIs (e.g., fetching student profiles, libraries, etc.), you need to generate a valid JWT token:

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8001/api/token/`
- **Body: (raw JSON)**
  ```json
  {
      "username": "john_doe",
      "password": "password123"
  }
  ```
- **Response Example:**
  ```json
  {
      "refresh": "<REFRESH_TOKEN>",
      "access": "<ACCESS_TOKEN>"
  }
  ```

