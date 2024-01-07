import tempfile
import cv2
import numpy as np
import os
import time
from encryption_module import decrypt_file
from system_resource_analyser_module import get_cpu_usage, get_memory_usage, get_disk_usage

def preprocess_image(file_path):
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Equalize histogram to enhance contrast
    image = cv2.equalizeHist(image)

    # Apply Gaussian blur for noise reduction
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert to binary image using Otsu's thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary_image

def match_fingerprints(minutiae1, minutiae2):
    """
    (Optimized euclidean distance) Calculate distances between minutiae points using Euclidean distance:
    - np.array(minutiae1)[:, None, :2] - This converts the list of minutiae points in minutiae1 to a NumPy array and adds a new axis (None or np.newaxis) along the second dimension. The [:, :2] part is used to keep only the x and y coordinates of the minutiae points.
    - np.array(minutiae2)[None, :, :2] - Similar to the first part, this converts the list of minutiae points in minutiae2 to a NumPy array. The [None, :, :2] part adds a new axis along the first dimension.
    - Subtracting the two arrays - The code then subtracts the two arrays obtained in the first and second steps. This subtraction is element-wise, meaning it subtracts corresponding elements.
    np.linalg.norm(..., axis=-1):
    - Finally, the np.linalg.norm function calculates the Euclidean norm (distance) along the last axis (axis=-1). This results in an array of Euclidean distances between each pair of minutiae points from minutiae1 and minutiae2.
    """
    distances = np.linalg.norm(np.array(minutiae1)[:, None, :2] - np.array(minutiae2)[None, :, :2], axis=-1)
    
    # Calculate similarity score
    min_distances = np.min(distances, axis=1)
    similarity_score = np.mean(min_distances)

    return similarity_score

def extract_minutiae(binary_image):
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    minutiae = []
    for contour in contours:
        # Filter small contours
        if cv2.contourArea(contour) > 50:
            # Append minutiae points from the contour to the list
            minutiae.extend(contour[:, 0, :].tolist())

    return minutiae

def main():
    # Encryption key
    key = "PqV8juaCaTmXcAXXMIF8qAcuzO2oPzDXKvBXQAkAo40="
    key_encoded = key.encode()

    # Define the location of the fingerprint dataset
    fingerprint_dataset_location = "./fingerprint_dataset_encrypt"
    
    # Define the path to the reference fingerprint image
    reference_image_path = "101_2.tif"
    binary_image_reference = preprocess_image(reference_image_path)
    minutiae_reference = extract_minutiae(binary_image_reference)
    
    # Set a similarity threshold
    threshold = 5

    # Start time of execution
    start_time = time.time()

    # Iterate through each file in the dataset
    for file_enc in os.listdir(fingerprint_dataset_location):
        try:
            path = os.path.join(fingerprint_dataset_location, file_enc)
            decrypted_data = decrypt_file(path, key_encoded)
            
            # If has not access to the file skip this iteration
            if not decrypted_data:
                continue

            # Use tempfile to create a secure temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(decrypted_data)
            
            # Get the temporary file path with the decrypted image
            temp_file_path = temp_file.name
            
            # Preprocess the current fingerprint image
            binary_image_current = preprocess_image(temp_file_path)
            minutiae_current = extract_minutiae(binary_image_current)

            # Match fingerprints and calculate similarity score
            match_score = match_fingerprints(minutiae_reference, minutiae_current)

            # Compare the similarity score with the threshold
            if match_score < threshold:
                print(f"{file_enc}: Fingerprints match! Similarity Score: {match_score}")
                print("--- Found in %s seconds --" % (time.time() - start_time))
            else:
                print(f"{file_enc}: Fingerprints do not match! Similarity Score: {match_score}")
            
            # System Usage
            get_cpu_usage()
            get_memory_usage()
            get_disk_usage()
            
            print("\n")
            
            # Delete the temp file decrypted
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Error processing {file_enc}: {e}")

if __name__ == "__main__":
    main()