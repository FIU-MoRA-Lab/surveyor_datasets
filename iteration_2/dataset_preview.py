import sys
import time
import h5py
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_structured_data(file_path):
    """Load structured HDF5 data into a pandas DataFrame."""
    with h5py.File(file_path, 'r') as f:
        structured_array = f['data'][:]
        print("Structured dtype:", structured_array.dtype)

    df = pd.DataFrame()
    for name in structured_array.dtype.names:
        col = structured_array[name]
        if col.ndim > 1:
            col = [x for x in col]  # Store multi-dimensional arrays as objects
        df[name] = col
    print("Data shape:", df.shape)
    return df


def setup_plot_layout(df):
    """Prepare matplotlib figure and subplots."""
    plt.ion()
    fig = plt.figure(figsize=(14, 8))

    ax_img = fig.add_subplot(1, 3, 1)

    ax_lidar = fig.add_subplot(1, 3, 2, polar=True) if 'Angles' in df.columns else None
    ax_gps = fig.add_subplot(1, 3, 3)

    # Compute GPS bounds ignoring zeros
    lat_valid = df['Latitude'][df['Latitude'] != 0]
    lon_valid = df['Longitude'][df['Longitude'] != 0]
    lat_bounds = (lat_valid.min(), lat_valid.max())
    lon_bounds = (lon_valid.min(), lon_valid.max())

    plt.tight_layout()
    plt.show()

    return fig, ax_img, ax_lidar, ax_gps, lat_bounds, lon_bounds


def visualize_dataset(file_path):
    df = load_structured_data(file_path)
    fig, ax_img, ax_lidar, ax_gps, (lat_min, lat_max), (lon_min, lon_max) = setup_plot_layout(df)

    for i, row in df.iterrows():
        # --- Image ---
        img_rgb = cv2.cvtColor(row['Image'], cv2.COLOR_BGR2RGB)
        ax_img.clear()
        ax_img.imshow(img_rgb)
        ax_img.set_title(f'Image {i}')
        ax_img.axis('off')

        # --- LiDAR ---
        if ax_lidar is not None :
            angles = np.array(row['Angles'])
            distances = np.array(row['Distances'])
            nonzero = distances > 0
            distances = distances[nonzero]
            angles = angles[nonzero]

            ax_lidar.clear()
            ax_lidar.set_theta_zero_location('N')
            ax_lidar.set_theta_direction(-1)
            ax_lidar.scatter(np.deg2rad(angles), distances, s=5)
            ax_lidar.set_title('LiDAR Measurements')
            if len(distances):
                ax_lidar.set_ylim(0, 15)
            else:
                ax_lidar.set_ylim(0, 1)

        # --- GPS ---
        ax_gps.clear()
        ax_gps.set_title('GPS Scatter (Lat vs Lon)')
        ax_gps.set_xlabel('Longitude')
        ax_gps.set_ylabel('Latitude')
        ax_gps.scatter(df['Longitude'][:i+1], df['Latitude'][:i+1], c='blue', s=5)
        ax_gps.scatter(row['Longitude'], row['Latitude'], c='red', label='Current', s=20)
        ax_gps.set_xlim(lon_min - 0.0005, lon_max + 0.0005)
        ax_gps.set_ylim(lat_min - 0.0005, lat_max + 0.0005)
        ax_gps.legend()

        # --- Print non-image and non-LiDAR columns ---
        print(f'\n--- Frame {i} ---')
        for col in df.columns:
            if col not in ['Image', 'Angles', 'Distances']:
                print(f'{col}: {row[col]}')

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)

    plt.ioff()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        visualize_dataset(sys.argv[1])
    else:
        print("Usage: python script.py <path_to_h5_file>")
