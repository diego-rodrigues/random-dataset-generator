
import random
import string
from datetime import datetime, timedelta

def generate_random_string(min: int, max: int) -> str:
    return generate_random_string_with_lenght(random.randint(min, max))


def generate_random_string_with_lenght(length: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))


def generate_random_premium_string() -> str:
    return "[" + generate_random_string_with_lenght(generate_random_int(3,5)) + "]-" + \
            "[" + generate_random_string_with_lenght(generate_random_int(5,9)) + "]-" + \
            "[" + generate_random_string_with_lenght(generate_random_int(3,5)) + "]"


def generate_random_int(min: int, max: int) -> int:
    return random.randint(min, max)


def _truncate_float(float_number: float,  decimal_points: int) -> float:
    multiplier = 10 **  decimal_points
    return int(float_number * multiplier) / multiplier


def generate_random_float_with_decimals(min: float, max: float, decimal_points: int) -> float:
    return _truncate_float(random.uniform(min, max), decimal_points)


def generate_random_float(min: float, max: float) -> float:
    return generate_random_float_with_decimals(min, max, random.randint(1,5))


def generate_random_datetime(start_date: datetime, end_date: datetime) -> datetime:
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date


def generate_random_boolean(true_chance: float) -> bool:
    return random.random() < true_chance


def generate_random_from_pool(choices: list) -> object:
    return random.choice(choices)

