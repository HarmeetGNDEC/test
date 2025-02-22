import pandas as pd

from helper_utils import load_files, convert_conversation_to_string
import re

sensitive_info_patterns = [
    r"\b(balance|account\s*number|account\s*balance|total\s*balance|available\s*credit)\b",
    r"\b(account\s*\d{4,})\b",  # Detect account number (simplified to 4+ digits)
]
identity_verification_patterns = [
    r"\b(date\s*of\s*birth|dob|birthday)\b",  # Date of birth
    r"\b(address)\b",  # Address
    r"\b(ssn|social\s*security\s*number)\b",  # Social Security Number
]
sensitive_info_regex = re.compile('|'.join(sensitive_info_patterns), re.IGNORECASE)
identity_verification_regex = re.compile('|'.join(identity_verification_patterns), re.IGNORECASE)


def detect_sensitive_information(text):
    return sensitive_info_regex.search(text) is not None

def detect_identity_verification(text):
    return identity_verification_regex.search(text) is not None

def analyze_conversations_for_compliance(all_data):
    privacy_violation_calls = []

    for filename, conversations in all_data:
        agent_shared_sensitive_info = False
        identity_verified = False

        for convo in conversations:
            speaker = convo.get('speaker')
            text = convo.get('text')

            if not text:
                continue  # Skip if there's no text

            # Check if the agent shared sensitive information
            if detect_sensitive_information(text) and speaker == 'Agent':
                agent_shared_sensitive_info = True

            # Check if there is identity verification before sensitive information
            if detect_identity_verification(text) and speaker == 'agent':
                identity_verified = True

            # If the agent shares sensitive info without prior identity verification, flag it
            if agent_shared_sensitive_info and not identity_verified:
                privacy_violation_calls.append(filename)
                break  # Stop further checking for this call ID, as we have already flagged it

    return privacy_violation_calls


def label_conversation(conversation):
    # Keywords to look for in the conversation
    sensitive_keywords = ['balance', 'account number', 'ssn', 'social security number', 'account details']
    verification_keywords = ['date of birth', 'dob', 'address', 'ssn']

    # Initialize label as 0 (no violation)
    label = 0

    # Check for sensitive information
    sensitive_found = any(re.search(r'\b' + keyword + r'\b', conversation.lower()) for keyword in sensitive_keywords)

    # Check for identity verification request
    verification_found = any(
        re.search(r'\b' + keyword + r'\b', conversation.lower()) for keyword in verification_keywords)

    # Label as violation if sensitive information is shared without verification
    if sensitive_found and not verification_found:
        label = 1  # Privacy and compliance violation

    return label


if __name__ == '__main__':
    extract_folder = './data/'

    # Load YAML files
    data = load_files(extract_folder)  #[(id,data)]
    data_for_labels = []
    violation_calls = []
    for each in data:
        di={}
        conv = each[1]
        id = each[0]
        conv = convert_conversation_to_string(conv)
        di['conversation'] = conv
        di['id'] = id
        label = label_conversation(conv)
        if label == 1:
            violation_calls.append(id)
        di['label'] = label
        data_for_labels.append(di)
    # violation_calls = analyze_conversations_for_compliance(data)
    df = pd.DataFrame(data_for_labels)
    df.to_excel('violation_calls.xlsx')
    print("Calls with privacy and compliance violations:", violation_calls)