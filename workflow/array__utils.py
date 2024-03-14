from typing import List


def all_present(arr1: List[str], arr2: List[str]) -> bool:
    set1 = set(arr1)
    set2 = set(arr2)

    return all(elem in set2 for elem in set1)


def none_present(arr1: List[str], arr2: List[str]) -> bool:
    set1 = set(arr1)
    set2 = set(arr2)

    return not any(elem in set2 for elem in set1)
