def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

# Test the function
number_to_check = 17
print(f"Is {number_to_check} a prime number? {is_prime(number_to_check)}")
