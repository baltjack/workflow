from typing import List


def all_present(arr1: List[str], arr2: List[str]) -> bool:
    set1 = set(arr1)
    set2 = set(arr2)

    return all(elem in set2 for elem in set1)


def none_present(arr1: List[str], arr2: List[str]) -> bool:
    set1 = set(arr1)
    set2 = set(arr2)

    return not any(elem in set2 for elem in set1)


def update_original_with_updates(original: dict[str, str], updates: dict[str, str]):
    """
    Update the original dictionary with values from the updates dictionary.

    Args:
        original (dict): The original dictionary containing cached values.
        updates (dict): The dictionary containing updated values.

    Returns:
        dict: The updated original dictionary.

    Raises:
        KeyError: If a key in the updates dictionary is not found in the original dictionary.
    """
    updated_original = original.copy()  # Create a copy to avoid modifying the original

    for key, value in updates.items():
        if key in updated_original:
            updated_original[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in the original dictionary.")

    return updated_original
