# Iteration 1 Datasets

This directory contains datasets collected during the first iteration of our data collection process. The datasets are categorized based on the sensors used during collection.

## Dataset Structure

Each file in the format `YYYYMMDD_HHMMSS` and contains image, lidar, water quality measurements and state data. Each file contains a dataset named `data` which contains a series of numpy structured arrays. Each array contains the data similar to a Python dictionary to see details about this inspect the file `dataset_preview.py`.

## Data Collection Details

- **State Data** : Contains timestamped state information of the robot during data collection, IMU information and coordinates.
- **Image Data**: Stores images captured during data collection. Images are in BGR format.
- **LiDAR Data**: Contains LiDAR measurements with distance (in meters) and angle information (in degrees).
- **EXO2 Data**: Contains EXO2 Data measurements of water quality features (e.g., temperature, oxygen, turbidity).

## Usage Notes

- To visualize the examples run:
```
python3 dataset_preview.py <path_to_dataset_folder>
```