#!/usr/bin/env python
# coding: utf-8

# # Question 1: Distance Matrix Calculation

# In[2]:


import pandas as pd

def calculate_distance_matrix(df):
    distance_matrix = pd.DataFrame(index=df['id_start'].unique(), columns=df['id_end'].unique(), dtype=float)

    for row in df.itertuples():
        distance_matrix.at[row.id_start, row.id_end] = row.distance

    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)

    return distance_matrix

# Assuming that the CSV file contains columns 'id_start', 'id_end', and 'distance'
df = pd.read_csv("C:\\Users\\tekal\\OneDrive\\Desktop\\MapUp-Data-Assessment-F-main\\MapUp-Data-Assessment-F-main\\datasets\\dataset-3.csv")

result_matrix = calculate_distance_matrix(df)

# Print the resulting distance matrix
print(result_matrix)


# # Question 2: Unroll Distance Matrix

# In[3]:


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', and 'distance'.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_data = []

    for id_start in df.index:
        for id_end in df.columns:
            # Exclude same id_start to id_end
            if id_start != id_end:
                distance = df.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    return pd.DataFrame(unrolled_data)

# Assuming 'result_matrix' is the distance matrix obtained from the previous question
result_matrix = calculate_distance_matrix(df)

# Use the unroll_distance_matrix function
unrolled_df = unroll_distance_matrix(result_matrix)

# Print the resulting unrolled DataFrame
print(unrolled_df)


# # Question 3: Finding IDs within Percentage Threshold

# In[4]:


import pandas as pd

def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', and 'distance'.
        reference_id (int): Reference ID for which to find similar IDs.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    avg_distance_reference = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_range = [0.9 * avg_distance_reference, 1.1 * avg_distance_reference]

    avg_distances = df.groupby('id_start')['distance'].mean()
    within_threshold_ids = avg_distances[(avg_distances >= threshold_range[0]) & (avg_distances <= threshold_range[1])].index

    result_df = df[df['id_start'].isin(within_threshold_ids)]

    return result_df

# Example usage:
# Assuming 'unrolled_df' is the DataFrame obtained from the previous steps
reference_id = 123  # Replace with the desired reference ID
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)

# Print the resulting DataFrame
print(result_within_threshold)


# # Question 4: Calculate Toll Rate

# In[5]:


def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame): Unrolled DataFrame with columns 'id_start', 'id_end', 'distance'.

    Returns:
        pandas.DataFrame: DataFrame with added columns for toll rates for each vehicle type.
    """
    toll_rates = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate in toll_rates.items():
        df[vehicle_type] = df['distance'] * rate

    return df

# Example usage:
# Assuming 'unrolled_df' is the DataFrame obtained from the previous steps
result_with_toll_rates = calculate_toll_rate(unrolled_df)

# Print the resulting DataFrame
print(result_with_toll_rates)


# # Question 5: Calculate Time-Based Toll Rates

# In[11]:


import pandas as pd

def calculate_time_based_toll_rates(df):
    time_ranges = {
        '00:00:00-10:00:00': 0.8,
        '10:00:00-18:00:00': 1.2,
        '18:00:00-23:59:59': 0.8
    }

    df['start_day'] = df['id_start'].astype(str)  # Assuming 'id_start' represents day information
    df['end_day'] = df['id_end'].astype(str)  # Assuming 'id_end' represents day information

    for index, row in df.iterrows():
        for time_range, discount_factor in time_ranges.items():
            if time_range.startswith('00:00:00'):
                # Assuming 'id_start' and 'id_end' are integers representing hours
                if 0 <= row['id_start'] <= 10 and 0 <= row['id_end'] <= 10:
                    df.at[index, 'distance'] *= discount_factor
                    break
            elif time_range.startswith('10:00:00'):
                if 10 <= row['id_start'] <= 18 and 10 <= row['id_end'] <= 18:
                    df.at[index, 'distance'] *= discount_factor
                    break
            elif time_range.startswith('18:00:00'):
                if 18 <= row['id_start'] and 18 <= row['id_end']:
                    df.at[index, 'distance'] *= discount_factor
                    break

    return df

# Example usage:
# Assuming 'df' is the DataFrame with columns 'id_start', 'id_end', and 'distance'
result_with_time_based_toll_rates = calculate_time_based_toll_rates(df)

# Print the resulting DataFrame
print(result_with_time_based_toll_rates)


# In[10]:





# In[ ]:




