import streamlit as st
from load_models import load_privacy, load_profanity
from helper_utils import *
from Q2_Regex import label_conversation
from Q1_Regex import profanity_pattern_func, analyze_conversations
from Q3 import calculate_overtalk_and_silence
import matplotlib.pyplot as plt

def plot_call_quality_metrics(overtalk, silence):
    # Create bar plot using Matplotlib
    labels = ['Overtalk', 'Silence']
    values = [overtalk, silence]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['orange', 'blue'])
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Call Quality Metrics: Overtalk vs Silence')
    ax.set_ylim(0, 100)

    # Display plot in Streamlit
    st.pyplot(fig)

st.title("Entity Detection Tool")

# Upload file
uploaded_file = st.file_uploader("Choose a Json file", type=["json"])
if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    try:
        data = json.loads(file_content)
        st.write(data)  # Display the content of the JSON file
    except json.JSONDecodeError:
        st.error("Error decoding JSON file.")


    # Select Approach (Pattern Matching, Machine Learning, or LLM)
    approach = st.selectbox("Select Detection Approach", ["Pattern Matching", "Machine Learning"])

    # Select Entity (Profanity Detection or Privacy and Compliance Violation)
    entity = st.selectbox("Select Entity to Analyze", ["Profanity Detection", "Privacy and Compliance Violation"])

    if st.button("Detect Entity"):
            result = ""
            conv = convert_conversation_to_string(data)
            if approach == 'Pattern Matching':
                if entity == 'Privacy and Compliance Violation':
                    label = label_conversation(conv)
                    if label == 1:
                        st.write('Privacy and Compliance Violation Found')
                    else:
                        st.write('Privacy and Compliance Violation not Found')
                if entity == 'Profanity Detection':
                    agent_profanity_calls, borrower_profanity_calls, label, overall = analyze_conversations([('uploaded_file',data)], profanity_pattern_func())
                    if overall:
                        if agent_profanity_calls != []:
                            st.write('Profanity Detection Found by Agent')
                        else:
                            st.write('Profanity Detection Found by Customer')
                    else:
                        st.write('Profanity Detection not Found')
            if approach == 'Machine Learning':
                if entity == 'Privacy and Compliance Violation':
                    if load_privacy(conv):
                        st.write('Privacy and Compliance Violation Found')
                    else:
                        st.write('Privacy and Compliance Violation not Found')
                if entity == 'Profanity Detection':
                    check_profanity = load_profanity(data)
                    if check_profanity == 'Agent':
                        st.write('Profanity Detection Found by Agent')
                    elif check_profanity == 'Customer':
                        st.write('Profanity Detection Found by Customer')
                    else:
                        st.write('Profanity Detection not Found')
            # start plot
            st.title("Call Quality Metrics Analysis")
            overtalk_percentage, silence_percentage = calculate_overtalk_and_silence(data)
            st.write(f"Overtalk Percentage: {overtalk_percentage:.2f}%")
            st.write(f"Silence Percentage: {silence_percentage:.2f}%")
            plot_call_quality_metrics(overtalk_percentage, silence_percentage)


