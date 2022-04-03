from RSA import RSA
from reduction_attack import reduction_attack


def task_1():
    rsa = RSA(bit_length=128)
    reduction_attack(rsa=rsa, samples_num=10000, bits_num=6)


def task_2():
    # Alice part
    message = "Agatha"
    hashed_message = hash(message)
    rsa = RSA(bit_length=128)
    N, e = rsa.get_public_key()
    r = rsa.get_random_element()
    q = (hashed_message * pow(r, e, N)) % N
    # Bob part
    t = rsa.sign(q)
    # Alice part
    s = (t * pow(r, -1, N)) % N

    if rsa.verify(hashed_message, s):
        print("Blind signature confirmed.")
    else:
        print("Blind signature failed.")


def task_3():
    rsa = RSA(bit_length=128)
    m = rsa.get_random_element()

    r = rsa.get_random_element()
    c = rsa.enc(m * r)
    m_r, reductions = rsa.blind_dec(c)
    x = m_r * pow(r, -1, rsa.N) % rsa.N
    print(x == m)

    reduction_attack(rsa=rsa, samples_num=1000, bits_num=6, blind=True)



if __name__ == "__main__":
    task_3()


