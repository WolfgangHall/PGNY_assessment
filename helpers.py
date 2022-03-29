def calculate_percent_difference(val1: float, val2:float) -> float:
    return abs(val1 - val2) / ((val1 + val2) / 2) * 100

def write_to_log_file(write_string: str, filepath="storage/logs/transaction_history.txt"):
    with open(filepath, 'a') as file:
        file.write(f"{write_string}\n")