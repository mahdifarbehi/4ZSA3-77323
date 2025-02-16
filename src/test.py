import random


random_odd = lambda: random.randrange(1, 5 + 1, 2)
random_even = lambda: random.randrange(2, 5 + 1, 2)

print(random_odd())
print(random_even())
