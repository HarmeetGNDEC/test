import matplotlib.pyplot as plt


def calculate_overtalk_and_silence(conversation):
    total_call_duration = conversation[-1]['etime']
    overtalk_duration = 0
    silence_duration = 0

    # Calculate overtalk and silence durations
    for i in range(1, len(conversation)):
        # Extract speech start and end times
        prev_speaker = conversation[i - 1]
        curr_speaker = conversation[i]

        prev_start, prev_end = prev_speaker["stime"], prev_speaker["etime"]
        curr_start, curr_end = curr_speaker["stime"], curr_speaker["etime"]

        # Check for overtalk (simultaneous speaking)
        if prev_end > curr_start and curr_end > prev_start:
            overlap_duration = min(prev_end, curr_end) - max(prev_start, curr_start)
            overtalk_duration += overlap_duration

        # Check for silence between segments
        if prev_end < curr_start:
            silence_duration += curr_start - prev_end

    # Calculate percentages
    overtalk_percentage = (overtalk_duration / total_call_duration) * 100
    silence_percentage = (silence_duration / total_call_duration) * 100

    return overtalk_percentage, silence_percentage


# def plot_call_quality_metrics(overtalk, silence):
#     labels = ['Overtalk', 'Silence']
#     values = [overtalk, silence]
#
#     plt.bar(labels, values, color=['orange', 'blue'])
#     plt.xlabel('Metrics')
#     plt.ylabel('Percentage (%)')
#     plt.title('Call Quality Metrics: Overtalk vs Silence')
#     plt.ylim(0, 100)
#     plt.show()

