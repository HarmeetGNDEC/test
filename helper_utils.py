import json
import os


def load_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    all_data.append((filename, data))
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    return all_data


def convert_conversation_to_string(conversations):
    conversation_string = ""

    for entry in conversations:
        speaker = entry["speaker"]
        text = entry["text"]
        conversation_string += f"{speaker}: {text}\n"

    return conversation_string.strip()