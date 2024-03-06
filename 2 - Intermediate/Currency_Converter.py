import requests

def currency_converter(amount, from_currency, to_currency):
    try:
        url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or to_currency not in data['rates']:
            raise ValueError('Invalid currency or API request failed.')

        rate = data['rates'][to_currency]
        converted_amount = amount * rate
        return converted_amount
    except Exception as e:
        return f'Error: {e}'

# Example usage
print(currency_converter(100, 'USD', 'EUR'))
