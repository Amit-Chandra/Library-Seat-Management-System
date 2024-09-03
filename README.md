Certainly! Below are example requests for each of the APIs using Postman. I will provide you with the details for each request, including the HTTP method, URL, headers, and body where applicable.

### 1. **StudentSignupAPI**

- **Method:** POST
- **URL:** `http://localhost:8000/api/students/signup/`
- **Headers:**
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "username": "student_user",
    "password": "password123",
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### 2. **StudentProfileAPI**

- **Method:** GET
- **URL:** `http://localhost:8000/api/students/profile/`
- **Headers:**
  - Authorization: Bearer <your-token>
- **Body:** None

- **Method:** PUT
- **URL:** `http://localhost:8000/api/students/profile/`
- **Headers:**
  - Authorization: Bearer <your-token>
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "newemail@example.com"
  }
  ```

### 3. **LibraryListAPI**

- **Method:** GET
- **URL:** `http://localhost:8000/api/libraries/`
- **Headers:**
  - Authorization: Bearer <your-token>
- **Body:** None

### 4. **SeatAvailabilityAPI**

- **Method:** GET
- **URL:** `http://localhost:8000/api/libraries/{library_id}/seats/`
- **Headers:**
  - Authorization: Bearer <your-token>
- **Body:** None

### 5. **ApproveStudentAPI**

- **Method:** POST
- **URL:** `http://localhost:8000/api/students/{student_id}/approve/`
- **Headers:**
  - Authorization: Bearer <your-admin-token>
- **Body:** None

### 6. **CreateLibraryAPI**

- **Method:** POST
- **URL:** `http://localhost:8000/api/libraries/create/`
- **Headers:**
  - Authorization: Bearer <your-admin-token>
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "name": "New Library",
    "location": "123 Library St",
    "capacity": 100
  }
  ```

### 7. **RetrieveLibraryAPI**

- **Method:** GET
- **URL:** `http://localhost:8000/api/libraries/{library_id}/`
- **Headers:**
  - Authorization: Bearer <your-token>
- **Body:** None

### 8. **UpdateLibraryAPI**

- **Method:** PUT
- **URL:** `http://localhost:8000/api/libraries/{library_id}/update/`
- **Headers:**
  - Authorization: Bearer <your-admin-token>
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "name": "Updated Library Name",
    "capacity": 150
  }
  ```

### 9. **DeleteLibraryAPI**

- **Method:** DELETE
- **URL:** `http://localhost:8000/api/libraries/{library_id}/delete/`
- **Headers:**
  - Authorization: Bearer <your-admin-token>
- **Body:** None

### 10. **ListLibrariesAPI**

- **Method:** GET
- **URL:** `http://localhost:8000/api/libraries/list/`
- **Headers:**
  - Authorization: Bearer <your-token>
- **Body:** None

In these examples, replace `<your-token>` and `<your-admin-token>` with actual tokens you obtain from the authentication process. Similarly, replace `{library_id}` and `{student_id}` with actual IDs from your database.

Feel free to adjust the URLs and payloads as necessary based on your actual setup.












To test your APIs with Postman, you'll need to provide sample requests for each endpoint defined in your api_views.py. Below, I'll give you a brief description of each API and provide sample requests for testing them in Postman.

### 1. *Student Signup API*
*Endpoint:* /api/signup/  
*Method:* POST

#### Sample Request Body:
json
{
  "username": "john_doe",
  "password": "password123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",  // Possible values: "superadmin", "admin", "student"
  "dob": "2000-01-01",
  "hobbies": "Reading, Coding",
  "contact_number": "1234567890",
  "address": "123 Main St",
  "geo_location": "37.7749,-122.4194",
  "library": 1  // Assuming a library with ID 1 exists
}


### 2. *Student Profile API*
*Endpoint:* /api/profile/  
*Method:* GET

#### Sample Request Headers:
- *Authorization*: Token <your_token> (Replace <your_token> with a valid authentication token if required)

*Note:* This API assumes the user is already authenticated and will retrieve the profile data of the currently logged-in user.

### 3. *Library List API*
*Endpoint:* /api/libraries/  
*Method:* GET

#### Sample Request:
No request body is needed for this endpoint.

#### Sample Request Headers:
- *Authorization*: Token <your_token> (if authentication is required)

### 4. *Seat Availability API*
*Endpoint:* /api/libraries/<int:library_id>/seats/  
*Method:* GET

#### Sample Request:
Replace <int:library_id> with an actual library ID.

For example, if you want to check the seat availability for a library with ID 1:

GET /api/libraries/1/seats/


#### Sample Request Headers:
- *Authorization*: Token <your_token> (if authentication is required)

### 5. *Approve Student API*
*Endpoint:* /api/approve_student/<int:student_id>/  
*Method:* POST

#### Sample Request:
Replace <int:student_id> with the ID of the student you want to approve.

For example, if you want to approve a student with ID 3:

POST /api/approve_student/3/


#### Sample Request Headers:
- *Authorization*: Token <your_token> (if authentication is required)

#### Sample Request Body:
json
{
  "approved": true  // Set to true or false based on whether you're approving or rejecting the student
}


### Testing with Postman

1. *Open Postman*: Ensure you have Postman installed. If not, download it from the [Postman website](https://www.postman.com/).

2. *Create a New Request*: Click on "New" and select "Request".

3. *Set the Request Type*: Choose the appropriate HTTP method (GET, POST) from the dropdown next to the URL field.

4. *Enter the URL*: Type the full URL of the API endpoint you want to test (e.g., http://127.0.0.1:8000/api/signup/).

5. *Add Headers* (if needed):
   - If authentication is required, add an Authorization header with the value Token <your_token>.

6. *Enter the Request Body* (for POST requests):
   - Click on the "Body" tab.
   - Select "raw" and set the type to "JSON".
   - Paste the sample JSON request body provided above.

7. *Send the Request*: Click the "Send" button.

8. *View the Response*: Check the response pane in Postman to see the API's output, including status codes and response data.

### Notes:
- *Authentication*: If your APIs are protected and require authentication, ensure that you use valid tokens or credentials.
- *Testing Data*: Make sure the data you're sending in your requests aligns with what's expected by the backend. For instance, ensure that IDs like library and student_id exist in your database.
- *CORS*: If you're testing from a different origin than your Django server, ensure CORS (Cross-Origin Resource Sharing) is properly set up in your Django settings.

By following the steps and using the sample requests provided, you should be able to effectively test each API endpoint in Postman.