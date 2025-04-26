from flask import Flask, request, jsonify
from deepface import DeepFace
import os
import logging

app = Flask(__name__)

# Paths
employee_images_path = '/home/public_html/api.x.com/assets/uploads/documents/face_attendance/'
temp_images_path = '/home/public_html/api.x.com/face_attendance/tmp/'
log_file_path = '/home/public_html/api.x.com/face_attendance/error_log.txt'

# Setup logging
logging.basicConfig(filename=log_file_path, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure temp directory exists
if not os.path.exists(temp_images_path):
    os.makedirs(temp_images_path)

# Use a faster model for better performance
model_name = "SFace" # 'ArcFace', 'Facenet', 'Facenet512', 'VGG-Face',

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    temp_image_path = None

    try:
        image = request.files.get('image')
        employee_id = request.form.get('employee_id')

        if not image or not employee_id:
            logging.error("Employee ID and image are required")
            return jsonify({"error": "Employee ID and image are required"}), 400

        # Save temporary image
        temp_image_path = os.path.join(temp_images_path, f"{employee_id}_temp_image.jpg")
        image.save(temp_image_path)

        # Find the employee reference image
        folder_path = os.path.join(employee_images_path, str(employee_id))
        if not os.path.exists(folder_path):
            logging.error(f"Folder not found for employee_id: {employee_id}")
            return jsonify({"error": "Employee face not added yet!"}), 404

        reference_image = None
        for file in os.listdir(folder_path):
            if file.startswith('face_') and file.endswith('.jpg'):
                reference_image = os.path.join(folder_path, file)
                break

        if not reference_image or not os.path.exists(reference_image):
            logging.error(f"Employee face image not found for employee_id: {employee_id}")
            return jsonify({"error": "Employee face image not found"}), 404

        # Perform verification 
        result = DeepFace.verify(
            img1_path=temp_image_path,
            img2_path=reference_image,
            model_name=model_name,
            enforce_detection=False
        )

        if result.get('verified'):
            #analysis = DeepFace.analyze(temp_image_path, actions=['age', 'gender', 'emotion', 'race'])
            os.remove(temp_image_path)
            return jsonify({
                "message": "Face recognized successfully",
                "employee_id": employee_id,
                "verification_result": result
            }), 200
        else:
            logging.error(f"Face not recognized for employee_id: {employee_id}")
            os.remove(temp_image_path)
            return jsonify({"message": "Face not recognized"}), 400

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        if temp_image_path and os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
