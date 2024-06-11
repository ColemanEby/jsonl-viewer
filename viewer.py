import json
import os
import streamlit as st
import pandas as pd

# Function to read JSONL file
def read_jsonl_file(file_name):
    json_objects = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            json_objects.append(json.loads(line))
    return json_objects

# Function to get JSONL files in a directory
def get_jsonl_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.jsonl')]

# Function to convert list of JSON objects to a Pandas DataFrame, handling nested JSON
def json_objects_to_dataframe(json_objects):
    # Normalize the nested JSON
    df = pd.json_normalize(
        json_objects, 
        sep='_'
    )
    return df

# Create a container for the sidebar to show the list of JSONL files in the directory named 'data'
file_list_container = st.sidebar.empty()

# Get the list of JSONL files in the directory named 'data'
file_list = get_jsonl_files('data')

# Show the list of JSONL files in the sidebar
file_list_container.markdown('### List of JSONL Files')
selected_file = file_list_container.selectbox('Select a file', file_list)

# Create a container to show the content of the selected JSONL file
file_content_container = st.empty()

# Read the content of the selected JSONL file
json_objects = read_jsonl_file(f'data/{selected_file}')

# Convert JSON objects to a DataFrame
df = json_objects_to_dataframe(json_objects)

# Sidebar for sorting options
sort_by = st.sidebar.selectbox('Sort by', df.columns)
sort_asc = st.sidebar.checkbox('Ascending', value=True)

# Sidebar for filtering options
filter_column = st.sidebar.selectbox('Filter by', df.columns)
filter_value = st.sidebar.text_input('Filter value')

# Apply sorting
df_sorted = df.sort_values(by=sort_by, ascending=sort_asc)

# Apply filtering if filter value is provided
if filter_value:
    df_sorted = df_sorted[df_sorted[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]

# Show the content of the selected JSONL file
file_content_container.markdown('### Content of the Selected File')
file_content_container.write(df_sorted)
