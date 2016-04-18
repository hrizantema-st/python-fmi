from itertools import chain, repeat
from itertools import permutations


def number_of_inversions(iterable):
    tmp = list(iterable)
    length = len(tmp)
    count = 0
    for i in range(0, length - 1):
        for j in range(i + 1, length):
            if tmp[j] < tmp[i]:
                count += 1
    return count


class ZipExhausted(Exception):
    pass


def izip_longest(*args, **kwds):
    fillvalue = kwds.get('fillvalue')
    counter = [len(args) - 1]

    def sentinel():
        if not counter[0]:
            raise ZipExhausted
        counter[0] -= 1
        yield fillvalue
    fillers = repeat(fillvalue)
    iterators = [chain(it, sentinel(), fillers) for it in args]
    try:
        while iterators:
            yield tuple(map(next, iterators))
    except ZipExhausted:
        pass


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def zero_position(grid, size):
    tmp = list(grid)
    for i in range(0, size):
        if 0 in set(tmp[i]):
            return i


def solvable_tiles(size=3):
    length = size ** 2
    tmp = permutations(range(0, length))

    for perm in tmp:
        num_inv = number_of_inversions(perm)
        grid = tuple(grouper(perm, size))
        zero_pos = zero_position(grid, size)

        if any([((size % 2 != 0) and (num_inv % 2 == 0)),
                (size % 2 == 0 and num_inv % 2 == 0 and zero_pos % 2 != 0),
                (size % 2 == 0 and num_inv % 2 != 0 and zero_pos % 2 == 0)]):
            yield grid
        else:
            pass

    raise StopIteration
