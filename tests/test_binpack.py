from bakpack import binpack


def test_binpack_callable():
    assert callable(binpack)


def test_binpack():
    def is_valid(size, answer):
        return all(sum(v) <= size for v in answer)

    assert is_valid(3, binpack(3, [2, 2, 1, 1]))
    assert is_valid(3, binpack(3, [3, 3, 1, 1]))

    for n in range(10):
        assert is_valid(
            n, binpack(n, list(j for i in range(1, n + 1) for j in range(1, i)))
        )


def test_binpack_cannot():
    assert binpack(1, [2]) is None
