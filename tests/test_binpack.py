import pytest

from bakpack import binpack
from typing import Union, Optional

#Rack = Optional(list[list[int]])

def test_binpack_callable():
    assert callable(binpack)


#def bad(size: int, answer: Rack) -> Union[False, str]:
def bad(size, answer):
    # Any bins are overstuffed
    if any(sum(v) > size for v in answer):
        return "overstuffed"
    # Any bin is empty
    if any(len(b) == 0 for b in answer):
        return "empty bin"
    return False

#def is_valid(size: int, answer: Rack) -> Union[False, str]:
def assert_valid(size, answer):
    b = bad(size, answer)
    assert not b, b

def test_bad():
    assert bad(2, [[1,2], [2]]) == "overstuffed"
    assert bad(3, [[1,2],[]]) == "empty bin"
    assert not bad(3, [[1,2]])

def test_assert_valid():
    with pytest.raises(AssertionError):
        assert_valid(2, [[1,2]])
    with pytest.raises(AssertionError):
        assert_valid(3, [[1,2],[]])


def test_binpack():
    assert_valid(3, binpack(3, [2, 2, 1, 1]))
    assert_valid(3, binpack(3, [3, 3, 1, 1]))

    for n in range(10):
        assert_valid(
            n, binpack(n, list(j for i in range(1, n + 1) for j in range(1, i)))
        )


def test_binpack_cannot():
    assert binpack(1, [2]) is None


big_sizes = [
    2221110026240,
    799619635200,
    144425922560,
    166,
    21572382894080,
    255874805760,
    75088793600,
    1445412874248,
    979842,
    6064791,
    222354,
    0,
    86090934,
    123182,
    961057444,
    33263675,
    29327,
    306298792,
    31770,
    5313205,
    7819308,
    31696593,
    2760552,
    750707,
    9073694,
    41985634,
    1595396,
    86720663,
    276896,
    709075,
    1262,
    14802042921,
    189283,
    20000147,
    2514,
    8250688,
    3389419,
    0,
    37200721920,
    19357030400,
    39894507520,
    275675125760,
    9282311720960,
    1704581120,
    187874394112,
    1646755840,
    1843138560,
    8099840,
    497397760,
    176845322240,
    524943360,
    1445382010880,
    17502068049920,
    748697600,
    100003840,
    35505428480,
    2260513003520,
    92577689600,
    1445412976640,
    88555520,
    376760320,
    35133440,
    180362086400,
    122347528,
    1373255680,
    72981657600,
    557844090880,
    344755787776,
    790923939840,
    337873233920,
    1759291504640,
    41200575161,
    733525678080,
    1274515015680,
    840382269440,
    983489761280,
    619422433280,
    936974295040,
]
big_bin_size = 12 << 40
fittable_big_sizes = [v for v in big_sizes if v <= big_bin_size]


def test_binpack_bigsizes():
    assert_valid(big_bin_size, binpack(big_bin_size, fittable_big_sizes))


def test_binpack_reduced_bigsizes():
    rsh = 30
    reduced_bin_size = big_bin_size >> rsh
    reduced_big_sizes = [max(v >> rsh, 1) for v in fittable_big_sizes]
    assert_valid(reduced_bin_size, binpack(reduced_bin_size, reduced_big_sizes))
