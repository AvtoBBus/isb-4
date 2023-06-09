import hashlib
import json

def check_hash(x: int) -> int:
    """Функция для проверки соответствия хеша числа с данным нам хешем

    Args:
        x (int): номер карты

    Returns:
        int: номер карты
    """
    with open('options.json') as json_file:
            options = json.load(json_file)

    return x if hashlib.sha256(f'{options["bin"]}{x}{options["last_digit"]}'.encode()).hexdigest() == f'{options["hash"]}' else False


def luna_algorithm(number: int) -> bool:
    """функция для проверки номера алгоритмом Луна

    Args:
        number (int): номер

    Returns:
        bool: соответствует/не соответствует
    """
    with open('options.json') as json_file:
            options = json.load(json_file)
    number = str(number)
    if len(number) != 6:
        return False
    check = 8
    bin = [int(i) for i in options['bin']]
    code = [int(i) for i in number]
    end = [int(i) for i in options['last_digit']]
    all_number = bin+code+end
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            mul = num*2
            if mul > 9:
                mul -= 9
            all_number[i] = mul
    total_sum = sum(all_number)
    rem = total_sum % 10
    check_sum = 10 - rem if rem != 0 else 0
    return number if check_sum == check else False