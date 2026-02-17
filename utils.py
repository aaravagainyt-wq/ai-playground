# utils.py
import datetime

def log_message(log_list, speaker, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_list.append({
        "time": timestamp,
        "speaker": speaker,
        "message": message
    })
    return log_list

def format_history(log_list):
    return "\n".join([f"{item['speaker']}: {item['message']}" for item in log_list])
