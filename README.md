# easy-face-recognition-api
Flask-Based Face Recognition API Using DeepFace for Employee Verification

# 📌 Title:
**Flask-Based Face Recognition API Using DeepFace for Employee Verification**

# 📃 Description:
This Python Flask application provides an API endpoint to verify an employee's identity by comparing a submitted face image against a stored reference image.  
It uses the **DeepFace** library with the **SFace** model for fast and accurate face verification.  
The API receives an employee ID and an image through a POST request, temporarily saves the image, matches it with the stored employee reference photo, and responds whether the face was recognized or not.  
All errors are logged for troubleshooting.


# 📑 Documentation:

## 1. Requirements
- Python 3.7+
- Flask
- DeepFace
- TensorFlow backend (DeepFace dependency)
- A structured directory where employee face images are stored.

### Install Required Packages:
```bash
pip install Flask deepface
```

---

## 2. Directory Structure

- `/home/public_html/api.x.com/assets/uploads/documents/face_attendance/`
  - Contains folders named after each `employee_id`
  - Each folder contains an image file starting with `face_` (e.g., `face_1.jpg`)

- `/home/public_html/api.x.com/face_attendance/tmp/`
  - Temporary storage for uploaded images for comparison.

- `/home/public_html/api.x.com/face_attendance/error_log.txt`
  - Error log file to store any issues that occur.

---

## 3. API Endpoint

### **POST** `/recognize_face`

**Request Body:**
- `employee_id` (form field, required): ID of the employee whose face is being verified.
- `image` (form file, required): Image file of the employee's face.

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/recognize_face \
  -F "employee_id=1234" \
  -F "image=@/path/to/test_image.jpg"
```

---

**Success Response:**
```json
{
  "message": "Face recognized successfully",
  "employee_id": "1234",
  "verification_result": {
    "verified": true,
    "distance": 0.3123,
    "model": "SFace",
    "similarity_metric": "cosine"
  }
}
```

**Failure Response (Face not matched):**
```json
{
  "message": "Face not recognized"
}
```

**Error Response (Missing fields or internal error):**
```json
{
  "error": "Employee ID and image are required"
}
```

**HTTP Status Codes:**
- `200 OK` - Face verified successfully.
- `400 Bad Request` - Missing input or face not matched.
- `404 Not Found` - Employee face image folder or file not found.
- `500 Internal Server Error` - Unexpected server error (also logged to file).

---

## 4. Features

- 🧠 Fast Face Verification using **SFace** model
- 🛡️ Error handling with detailed logging
- 🧹 Automatic cleanup of temporary images
- 🔒 Secure: Does not keep user-uploaded images after processing
- 🛠️ Easy to extend (e.g., age, gender detection with DeepFace's `analyze` feature)

---

## 5. Notes
- You can enable extra analysis (like age, emotion, race) by uncommenting this line:
  ```python
  # analysis = DeepFace.analyze(temp_image_path, actions=['age', 'gender', 'emotion', 'race'])
  ```
- `enforce_detection=False` allows the system to continue even if the face is not very clear; you can set it to `True` for stricter validation.
- It’s good practice to monitor the `error_log.txt` regularly to detect any API issues.

---

## 6. Security Recommendations
- Limit the file size for uploads.
- Validate image MIME types before saving.
- Use authentication tokens if exposing the API publicly.

---
