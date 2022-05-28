def calc_checksum(data):
    result = 0
    for i in range(0, len(data), 2):
        result = (result + int.from_bytes(data[i:i + 2], 'big')) % 2 ** 16
    return 2 ** 16 - 1 - result


def validation_checksum(data, checksum):
    result = checksum
    for i in range(0, len(data), 2):
        result = (result + int.from_bytes(data[i:i + 2], 'big')) % 2 ** 16
    return result == 2 ** 16 - 1


def test_calc_checksum_default():
    checksum = calc_checksum(b'')
    assert checksum == 2 ** 16 - 1
    assert validation_checksum(b'', checksum)


def test_calc_checksum_correct():
    checksum = calc_checksum(b'Test')
    assert validation_checksum(b'Test', checksum)


def test_calc_checksum_incorrect():
    checksum = calc_checksum(b'Test')
    assert not validation_checksum(b'Test!', checksum)


if __name__ == '__main__':
    test_calc_checksum_default()
    test_calc_checksum_correct()
    test_calc_checksum_incorrect()
