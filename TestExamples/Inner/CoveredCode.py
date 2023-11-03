

def add_and_multiply(*args, add=12, multiply_by=2):
    return [(item + add) * multiply_by for item in args]


def divide(left, right):
    if right <= 0:
        raise ArithmeticError("Divide by 0")
    return left / right


def extract_items_lower_than(array, threshold):
    """Extract items from the array lower than the given threshold."""
    return  [item for item in array if item < threshold]

