import math

input = 34000000


def present_number(house, primes):
    divisors = get_divisors2(house, primes)
    # print(house, divisors)
    return sum([d * 10 for d in divisors])


# Naive implementation
def get_divisors(n):
    i = 1
    d = [n]
    while i <= n / 2:
        if n % i == 0:
            d.append(i)
        i = i + 1
    return d


def get_divisors2(n, primes):
    return divisors(factorize(n, primes))


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/


def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def get_primes(upto):
    g = gen_primes()
    s = []
    n = next(g)
    while n <= upto:
        s.append(n)
        n = next(g)
    return s


# From here https://stackoverflow.com/a/12422030/119071
def factorize(n, primes):
    factors = []
    for p in primes:
        if p * p > n:
            break
        i = 0
        while n % p == 0:
            n //= p
            i += 1
        if i > 0:
            factors.append((p, i))
    if n > 1:
        factors.append((n, 1))

    return factors


def divisors(factors):
    div = [1]
    for (p, r) in factors:
        div = [d * p ** e for d in div for e in range(r + 1)]
    return div


primes = get_primes(int(math.sqrt(input)))

if __name__ == "__main__":
    print("Starting")
    part = "b"
    if part == "a":
        for i in range(1, input):
            pn = present_number(i, primes)
            if pn > input:
                print(i, pn)
                break
    else:
        # Part b
        excluded = set()
        factor_counter = dict()
        for i in range(1, input):
            ds = get_divisors2(i, primes)
            for d in ds:
                if d not in excluded:
                    v = factor_counter.get(d, 0)
                    factor_counter[d] = v + 1
                    if v == 50:
                        excluded.add(d)
            pn = sum([d * 11 for d in ds if d not in excluded])
            if i % 1000 == 0:
                print(i, pn)
            if pn > input:
                print(i, pn)
                break

