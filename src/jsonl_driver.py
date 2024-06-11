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
        record_path=['messages'],
        meta=['model'],
        errors='ignore'
    )
    return df