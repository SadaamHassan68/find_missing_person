import cv2
import numpy as np
import face_recognition
import base64

# Helper to load image from file path or numpy array
def load_image(image):
    if isinstance(image, str):
        # Assume it's a file path
        return face_recognition.load_image_file(image)
    elif isinstance(image, np.ndarray):
        # Convert BGR (OpenCV) to RGB
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError('Unsupported image format for face recognition')

def compare_faces(img1, img2, tolerance=0.6):
    """
    Compare two images (numpy arrays or file paths). Returns (is_match, accuracy_score).
    accuracy_score is 1.0 for perfect match, 0.0 for no match, or a value based on face distance.
    """
    try:
        image1 = load_image(img1)
        image2 = load_image(img2)

        # Get face encodings
        encodings1 = face_recognition.face_encodings(image1)
        encodings2 = face_recognition.face_encodings(image2)

        if not encodings1 or not encodings2:
            print('No face found in one of the images')
            return False, 0.0  # No face found in one of the images

        # Compute face distance
        face_distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
        is_match = face_distance <= tolerance
        # Convert distance to accuracy (1.0 = perfect match, 0.0 = worst)
        accuracy = max(0.0, 1.0 - face_distance)
        print(f"Face distance: {face_distance:.3f}, Match: {is_match}, Accuracy: {accuracy:.3f}, Tolerance: {tolerance}")
        return is_match, accuracy
    except Exception as e:
        print(f"Error in compare_faces: {e}")
        return False, 0.0 