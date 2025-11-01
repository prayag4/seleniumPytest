import random
from datetime import datetime, timedelta
from calendar import month_name
from faker import Faker

faker = Faker()

class RandomUtility:
    months = list(month_name[1:])  # ['January', ..., 'December']

    @staticmethod
    def generate_random_string(length=5) -> str:
        return faker.text(max_nb_chars=length).replace('\n', '')[:length]

    @staticmethod
    def generate_random_numberss(digits=7) -> str:
        return ''.join(random.choices('0123456789', k=digits))

    @staticmethod
    def generate_random_number(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def generate_random_time() -> str:
        hour = random.randint(0, 12)
        minute = random.randint(0, 59)
        ampm = random.choice(["AM", "PM"])
        return f"{hour:02d}:{minute:02d} {ampm}"

    @staticmethod
    def generate_random_time_range() -> tuple:
        start_hour = random.randint(0, 12)
        start_minute = random.randint(0, 59)
        start_ampm = random.choice(["AM", "PM"])
        start_time = f"{start_hour:02d}:{start_minute:02d} {start_ampm}"

        duration = random.randint(15, 180)
        start_total_minutes = (start_hour % 12) * 60 + start_minute + (720 if start_ampm == "PM" else 0)
        end_total_minutes = start_total_minutes + duration

        end_hour = (end_total_minutes % 720) // 60
        end_minute = end_total_minutes % 60
        end_ampm = "PM" if end_total_minutes >= 720 else "AM"
        end_time = f"{end_hour:02d}:{end_minute:02d} {end_ampm}"
        return start_time, end_time

    @staticmethod
    def generate_multiple_line_content(word_count=5) -> str:
        return faker.sentence(nb_words=word_count)

    @staticmethod
    def generate_random_email() -> str:
        return f"user{random.randint(1000, 9999)}@example.com"

    @staticmethod
    def get_random_selected_values_from_array(array: list) -> list:
        count = min(5, random.randint(1, len(array))) if len(array) > 1 else 1
        random.shuffle(array)
        selected = [array.pop(0) for _ in range(count)]
        return selected

    @staticmethod
    def get_random_selected_one_value_from_array(array: list):
        return random.choice(array)

    @staticmethod
    def generate_fake_phone_number() -> str:
        first_digits = ["9", "8", "7", "6"]
        number = "+91" + random.choice(first_digits)
        number += ''.join(random.choices('0123456789', k=9))
        return number

    @staticmethod
    def format_date_to_ddmmyyyy(date_obj: datetime) -> str:
        return date_obj.strftime("%d/%m/%Y")

    @staticmethod
    def generate_random_date() -> list:
        now = datetime.now()
        delta_days = random.randint(-730, 730)  # ± 2 years
        random_date = now + timedelta(days=delta_days)
        day = str(random_date.day)
        month = RandomUtility.months[random_date.month - 1]
        year = str(random_date.year)
        formatted = RandomUtility.format_date_to_ddmmyyyy(random_date)
        return [[day, month, year], formatted]

    @staticmethod
    def generate_random_date_range() -> list:
        now = datetime.now()
        start_delta_days = random.randint(-730, 730)
        start_date = now + timedelta(days=start_delta_days)
        end_delta_days = random.randint(0, 730)
        end_date = start_date + timedelta(days=end_delta_days)

        start_array = [str(start_date.day), RandomUtility.months[start_date.month - 1], str(start_date.year)]
        end_array = [str(end_date.day), RandomUtility.months[end_date.month - 1], str(end_date.year)]

        start_formatted = RandomUtility.format_date_to_ddmmyyyy(start_date)
        end_formatted = RandomUtility.format_date_to_ddmmyyyy(end_date)
        return [start_array, start_formatted, end_array, end_formatted]

    @staticmethod
    def generate_random_lat_long() -> str:
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        return f"{latitude:.6f},{longitude:.6f}"

    @staticmethod
    def generate_random_text(length: int) -> str:
        special_chars = "!@#$%^&*()_+[]{}|;:,.<>?"
        numbers = "0123456789"
        lower = "abcdefghijklmnopqrstuvwxyz"
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        all_chars = special_chars + numbers + lower + upper

        # Ensure at least one of each type
        password = [
            random.choice(special_chars),
            random.choice(numbers),
            random.choice(lower),
            random.choice(upper)
        ]
        password += random.choices(all_chars, k=length - 4)
        random.shuffle(password)
        return ''.join(password)