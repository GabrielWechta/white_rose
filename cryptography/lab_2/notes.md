- problem set 5 from last year
- P1: what are eqs that will allow to distinguish bits

---
Regular RSA Signature:

$Gen:<pubK, privK> = <(N,e), d>$

$Sign(privK, m) = h(m)^d modN$

$Vrfy(pubK,m,s) = h(m) == s^e mod N)$

Normal flow:

`A-Alice, S-Signer, V-Verifier`

A(pubK), S(privK), V(pubK)

1. A -m-> S
2. A <-s- S
3. A -m,s-> V

*in this scenario S learns the message.*

---
Blind RSA Signature (D. Charm):

Normal flow:

`A-Alice, S-Signer, V-Verifier`

A(pubK), S(privK), V(pubK)
1. A generates $r$
2. A calculates $q = h(m) \cdot r^e mod N$ 
3. A -q-> S
4. S calculates $t=q^d mod N$
5. A <-t- S
6. A calculates $s = t \cdot r^{-1} mod N$

it holds:

$s = t \cdot r^{-1} mod N =$

$q^d \cdot r^{-1} mod N =$

$(h(m)\cdot r^e)^d \cdot r^{-1} mod N =$

$h(m)^d \cdot r^{ed} \cdot r^{-1} mod N = h(m)^d mod N$

7. A -m,s-> V

*In this scenario S learns nothing about m.*

It's like Bank(S) is signing that i have money but it can not track it after it signs it. 

---
Protection against Timing Attacks.

normally we do: $Dec(privK,c) = c^d mod N$

Now we will do:
1. $r \leftarrow randomElemnt(Z_N^*)$
2. $t = Dec(privK, c \cdot r^e mod N)$
3. return: $t \cdot r^{-1} mod N$

Run Timing Attack after fixing it with Blind Signature, to see that there are.