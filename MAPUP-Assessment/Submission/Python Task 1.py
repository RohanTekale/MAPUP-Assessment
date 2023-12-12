#!/usr/bin/env python
# coding: utf-8

# # Question 1: Car Matrix Generation

# In[1]:


import pandas as pd

# Assuming you have a DataFrame named df
# You can replace the following line with how you get your DataFrame
df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv")

def generate_car_matrix(df):
    # Pivot the DataFrame using id_1 as index, id_2 as columns, and car as values
    matrix_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
    matrix_df = matrix_df.fillna(0)

    # Replace diagonal values with 0
    for col in matrix_df.columns:
        matrix_df.at[col, col] = 0

    return matrix_df


result_df = generate_car_matrix(df)

# Print the resulting DataFrame
print(result_df)


# #  Question 2: Car Type Count Calculation

# In[5]:


import pandas as pd

def get_type_count(df):
    """
    Adds a new categorical column 'car_type' based on values of the column 'car' and
    calculates the count of occurrences for each 'car_type' category.

    Args:
        df (pandas.DataFrame): Input DataFrame with a 'car' column.

    Returns:
        dict: A dictionary with 'car_type' categories as keys and their counts as values,
              sorted alphabetically based on keys.
    """
    # Check if 'car' column exists in the DataFrame
    if 'car' not in df.columns:
        raise ValueError("The 'car' column does not exist in the DataFrame.")

    # Add a new column 'car_type' based on conditions
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Count occurrences of each 'car_type'
    car_type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    car_type_counts = dict(sorted(car_type_counts.items()))

    return car_type_counts


df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv")

result_dict = get_type_count(df)

# Print the resulting dictionary
print(result_dict)


# # Question 3: Bus Count Index Retrieval

# In[6]:


import pandas as pd

def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Check if 'bus' column exists in the DataFrame
    if 'bus' not in df.columns:
        raise ValueError("The 'bus' column does not exist in the DataFrame.")

    # Calculate the mean value of the 'bus' column
    mean_bus_value = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean value
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()

    return bus_indexes


df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv")

result_list = get_bus_indexes(df)

# Print the resulting list of indices
print(result_list)


# # Question 4: Route Filtering

# In[7]:


import pandas as pd

def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame with 'route' and 'truck' columns.

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Check if 'truck' and 'route' columns exist in the DataFrame
    if 'truck' not in df.columns or 'route' not in df.columns:
        raise ValueError("The 'truck' or 'route' column does not exist in the DataFrame.")

    # Calculate the average value of the 'truck' column
    avg_truck_value = df['truck'].mean()

    # Filter rows where the average of 'truck' values is greater than 7
    filtered_df = df[df['truck'] > 7]

    # Get the unique values of the 'route' column and sort them
    routes_list = filtered_df['route'].unique().tolist()
    routes_list.sort()

    return routes_list


df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv")

result_list = filter_routes(df)

# Print the resulting list of route names
print(result_list)


# # Question 5: Matrix Value Modification

# In[8]:


import pandas as pd

def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Check if the input matrix is empty or not a DataFrame
    if not isinstance(matrix, pd.DataFrame) or matrix.empty:
        raise ValueError("Input should be a non-empty DataFrame.")

    # Apply the specified logic to each element in the matrix
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


matrix = pd.DataFrame({'A': [15, 25, 30], 'B': [10, 20, 25], 'C': [5, 15, 20]})

modified_matrix = multiply_matrix(matrix)

# Print the modified DataFrame
print(modified_matrix)


# # Question 6: Time Check

# In[11]:


import pandas as pd

def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns id, id_2, and timestamp.

    Returns:
        pd.Series: Boolean series indicating if each (id, id_2) pair has correct timestamps.
    """
    # Check if the required columns exist in the DataFrame
    if not all(col in df.columns for col in ['id', 'id_2', 'timestamp']):
        raise ValueError("The DataFrame should contain columns 'id', 'id_2', and 'timestamp'.")

    # Convert 'timestamp' to datetime format
    df['Timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Extract day of the week and time from the timestamp
    df['day_of_week'] = df['Timestamp'].dt.day_name().astype('object')
    df['time_of_day'] = df['Timestamp'].dt.time

    # Group by unique (id, id_2) pairs
    grouped = df.groupby(['id', 'id_2'])

    # Check if timestamps cover a full 24-hour period and span all 7 days of the week
    completeness_check = grouped.apply(lambda group: (
        group['time_of_day'].min() == pd.Timestamp('00:00:00').time() and
        group['time_of_day'].max() == pd.Timestamp('23:59:59').time() and
        set(group['day_of_week'].unique()) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ))

    return completeness_check


df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-2.csv")

result_series = time_check(df)

# Print the resulting boolean series
print(result_series)


# In[ ]:




