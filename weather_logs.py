

def weather_logs(message, date):
    with open(f"logs/{date}.log", "a") as log_file:
        log_file.write(message)