import os
from skimage import io
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
import numpy as np
import cv2

def calculate_image_similarity(image1, image2):
    # Convert images to grayscale
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)

    # Apply Gaussian blur to reduce noise
    gray_image1 = cv2.GaussianBlur(gray_image1, (5, 5), 0)
    gray_image2 = cv2.GaussianBlur(gray_image2, (5, 5), 0)

    # Calculate the SSIM (Structural Similarity Index)
    similarity = ssim(gray_image1, gray_image2, data_range=gray_image2.max() - gray_image2.min())
    return similarity

def calculate_lower_similarity(image1, image2, lower_percentage=20):
    # Calculate the height at which to start comparing (lower 20%)
    height, width = image1.shape[:2]
    lower_height = int(height * (1 - lower_percentage / 100))

    # Crop the lower part of the images for comparison
    lower_image1 = image1[lower_height:, :]
    lower_image2 = image2[lower_height:, :]

    # Calculate the SSIM for the lower part of the images
    lower_similarity = calculate_image_similarity(lower_image1, lower_image2)
    return lower_similarity

def delete_similar_frames(folder_path, threshold=0.95, lower_similarity_threshold=0.95, other_folder_path=None):
    file_list = sorted(os.listdir(folder_path))
    prev_frame = None

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        # Read the current frame
        print(f"Reading {file_path}")
        current_frame = io.imread(file_path)

        # Compare the current frame with the previous frame
        if prev_frame is not None:
            similarity = calculate_image_similarity(prev_frame, current_frame)
            print(f"Similarity to previous = {similarity}")

            # If the similarity is above the threshold, delete the current frame
            if similarity >= threshold:
                # Check the lower part of the frames' similarity
                lower_similarity = calculate_lower_similarity(prev_frame, current_frame)
                print(f"Lower similarity to previous = {lower_similarity}")
                # If the overall similarity is above the threshold and the lower part similarity is also above its threshold, delete the current frame
                if lower_similarity >= lower_similarity_threshold:
                    print("Similar frame detected. Deleting frame.")
                    os.remove(file_path)
                    
                    # Delete the corresponding file in the other folder
                    if other_folder_path:
                        other_file_path = os.path.join(other_folder_path, file_name)
                        if os.path.exists(other_file_path):
                            os.remove(other_file_path)
                else:
                    print("Lower part of the frame was different. Keeping frame.")
                    prev_frame = current_frame
            else:
                prev_frame = current_frame
        else:
            prev_frame = current_frame

if __name__ == "__main__":
    folder_path = "C:/Users/framebot/bots/pokemonFrames/s1e1sub"
    other_folder_path = "C:/Users/framebot/bots/pokemonFrames/s1e1"  # Specify the path to another folder such as a captionless one (Optional - Set to none if you don't have one)
    delete_similar_frames(folder_path, other_folder_path=other_folder_path)
