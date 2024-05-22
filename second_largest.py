def find_second_largest(nums: list[int]) -> int:
    arr = list(set(nums))
    arr.sort()

    if len(arr) > 2:
        return arr[-2]
    else:
        return arr[0]

def test_find_second_largest():
    assert find_second_largest([4, 2, 5, 1]) == 4
    assert find_second_largest([12, 35, 1, 10, 34, 1]) == 34
    assert find_second_largest([-2, -8, -10, -1, -100]) == -2
    assert find_second_largest([10, 10, 10]) == 10


if __name__ == "__main__":
    test_find_second_largest()