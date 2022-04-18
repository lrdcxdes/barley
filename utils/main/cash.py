

def to_str(money: int):
    return f"<code>${money:,}</code>"


def get_cash(money: str):
    res = money.replace('.', '').replace(',', '').replace(' ', '').replace('к', '000').replace(
        'k', '000').replace('е', 'e').replace('$', '')
    return int(float(res))
