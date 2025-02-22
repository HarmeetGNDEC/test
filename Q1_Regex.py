import zipfile
import yaml
import json
import os
from helper_utils import load_files
from better_profanity import profanity
import re
import pandas as pd

def load_profanity_list():
    with open('./profanity_list.txt', 'r') as f:
        profanity_list = [line.strip() for line in f.readlines()]
    return profanity_list

def profanity_regex(profanity_list):
    return re.compile(r'\b(' + '|'.join(profanity_list) + r')\b', re.IGNORECASE)


# def detect_profanity(text):
#     return profanity.contains_profanity(text)
def detect_profanity(text, profanity_pattern):
    if profanity_pattern.search(text):
        return True
    return False

def profanity_pattern_func():
    profanity_list = load_profanity_list()
    return profanity_regex(profanity_list)

def analyze_conversations(all_data, profanity_pattern):
    agent_profanity_calls = []
    borrower_profanity_calls = []
    data_with_labels = []

    for filename, conversations in all_data:
        overall = False
        for convo in conversations:
            speaker = convo.get('speaker')
            text = convo.get('text')
            stime = convo.get('stime')
            etime = convo.get('etime')
            di = {'speaker': speaker, 'text': text, 'stime': stime, 'etime': etime, 'callIds': filename}

            if not text:
                continue

            # if detect_profanity(text):
            if detect_profanity(text, profanity_pattern):
                overall = True
                di['label'] = 1
                if speaker == 'Agent':
                    agent_profanity_calls.append(filename)  # Record the call ID
                elif speaker == 'Customer':
                    borrower_profanity_calls.append(filename)  # Record the call ID
            else:
                di['label'] = 0
            data_with_labels.append(di)

    return agent_profanity_calls, borrower_profanity_calls, data_with_labels, overall

if __name__ == '__main__':
    extract_folder = './data/'

    # Load YAML files
    data = load_files(extract_folder)
    # profanity
    # profanity_list = load_profanity_list()
    # profanity_pattern = profanity_regex(profanity_list)

    agent_calls, borrower_calls, data_with_labels, overall = analyze_conversations(data, profanity_pattern_func())
    df = pd.DataFrame(data_with_labels)
    df.to_excel('profanity_calls.xlsx')
    print("Calls with profanity by agents:", agent_calls)
    print("Calls with profanity by borrowers:", borrower_calls)
