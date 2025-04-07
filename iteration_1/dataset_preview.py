import argparse
import os
import h5py
import json
import csv
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

def main(folder_path):
    # --- File paths ---
    h5_file_path = os.path.join(folder_path, 'image_data.h5')
    json_file_path = os.path.join(folder_path, 'lidar_data.json')
    csv_file_path = os.path.join(folder_path, 'state_data.csv')

    # --- Load data ---
    with h5py.File(h5_file_path, 'r') as h5f:
        images = h5f['images'][:]  # Adjust dataset name if needed

    with open(csv_file_path, 'r') as cf:
        csv_lines = list(csv.reader(cf))

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as jf:
            lidar_data = [json.loads(line.strip()) for line in jf if line.strip()]
    else:
        lidar_data = [None] * len(images)  # Placeholder for missing LiDAR data

    # --- Setup figure and subplots ---
    plt.ion()
    fig = plt.figure(figsize=(10, 4))

    # Image subplot
    ax_img = fig.add_subplot(1, 2, 1)

    # LiDAR subplot (only if data exists)
    if any(lidar_data):
        ax_lidar = fig.add_subplot(1, 2, 2, polar=True)
    else:
        ax_lidar = None

    plt.tight_layout()
    plt.show()

    # --- Main loop ---
    for i in range(min(len(images), len(csv_lines))):
        img = images[i]
        robot_state = csv_lines[i]

        # Convert BGR to RGB for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Update image plot
        ax_img.clear()
        ax_img.imshow(img_rgb)
        ax_img.set_title(f'Image {i}')
        ax_img.axis('off')

        # Update LiDAR plot if data exists
        if lidar_data[i] is not None and ax_lidar is not None:
            lidar, angles = lidar_data[i].values()
            ax_lidar.clear()
            ax_lidar.set_theta_zero_location('N')
            ax_lidar.set_theta_direction(-1)
            ax_lidar.scatter(np.deg2rad(angles), lidar, s=5)
            ax_lidar.set_title('LiDAR Measurements')
            ax_lidar.set_ylim(0, max(lidar) * 1.1)

        # Draw and update
        fig.canvas.draw()
        fig.canvas.flush_events()

        print(f'Robot State {i}: {robot_state}')
        time.sleep(0.25)

    plt.ioff()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and visualize dataset.")
    parser.add_argument("folder_path", type=str, help="Path to the dataset folder")
    args = parser.parse_args()

    main(args.folder_path)
