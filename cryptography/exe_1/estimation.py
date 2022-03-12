from math import log2

cc_100 = 4*10 ** 9
seconds = 3155760000

right = log2(cc_100*seconds)

for n in range(1, 4000):
    time = n ** (1/3)*log2(n) ** (2/3)
    if time > right:
        print(f"{n=} - {time=} - {right=}")
        break
