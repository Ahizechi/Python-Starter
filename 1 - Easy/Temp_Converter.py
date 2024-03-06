def temp_converter(temp, unit):
    if unit == "C":
        return (temp * 9/5) + 32  # Convert to Fahrenheit
    elif unit == "F":
        return (temp - 32) * 5/9  # Convert to Celsius

# Test
print(temp_converter(100, "C"))
