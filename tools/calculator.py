import numexpr

def calculate(expression):
    try:
        result = numexpr.evaluate(expression)
        return str(result)

    except Exception:
        return "Invalid Expression"