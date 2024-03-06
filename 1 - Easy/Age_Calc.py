import datetime

def calculate_age(birth_date):
    today = datetime.date.today()
    print(today)
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

birth_date = datetime.date(1990, 5, 24)
age = calculate_age(birth_date)
print("Your age is:", age)