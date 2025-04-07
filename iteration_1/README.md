# Iteration 1 Datasets

This directory contains datasets collected during the first iteration of our data collection process. The datasets are categorized based on the sensors used during collection.

## Subdirectories

- `state_camera/`: Contains datasets with synchronized state and camera data.
- `state_lidar_camera/`: Contains datasets with synchronized state, LiDAR, and camera data.

## Dataset Structure

Each dataset is organized in a folder named with the collection date and time in the format `dataset_YYYYMMDD_HHMMSS`. Within each dataset folder, you will find the following files:

- `image_data.h5`: HDF5 file containing image data in format BGR.
- `state_data.csv`: CSV file containing state information (IMU + timestamp + Exo2 data).
- `lidar_data.json`: JSON file containing LiDAR measurements (present only in `state_lidar_camera` datasets), each line is a dictionary `{'distances' : list, 'angles' : list}`. Discard the measurements in between 90 and 270 degrees; they are pointing towards the boat.

## Data Collection Details

- **State Data (`state_data.csv`)**: Contains timestamped state information of the robot during data collection.
- **Image Data (`image_data.h5`)**: Stores images captured during data collection. Images are in BGR format.
- **LiDAR Data (`lidar_data.json`)**: Contains LiDAR measurements with distance and angle information (only in `state_lidar_camera` datasets).

## Usage Notes

- Ensure that you have the necessary software to read HDF5, CSV, and JSON files.
- For image data, note that the images are stored in BGR format, which may require conversion to RGB for certain applications.

- To visualize the examples run:
```
python3 dataset_preview.py <path_to_dataset_folder>
```