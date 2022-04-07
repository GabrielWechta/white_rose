Notes for labs:

THis is usually how asym-crypto system look like

K - public key
k - private key

A(K):
- Time - poly
- Memory - poly

B(K, k):
- Time - poly
- Memory - poly

E(K):
- Time - **subexp**
- Memory - 

$c=Enc(K,m)$
A -$c$-> B

---
A generates: $(k_i', k_i, id_i)$ then $c_i = Enc_{k_i'}(k_i || id_i)$

where $k_i'$ - is a weak key that can be guessed in time $q$. $q = 2^n, n = 30$

Then:
PubKey: ${c_1, c_2, ... , c_q}$
PrivKey: ${(id_1, k_1), (id_2, k_2), ..., (id_q, k_q)}$

A(${c_1, ..., c_q},m$):
1. selects $j \leftarrow {1, ..., q}$
2. computes $k_j'$
3. finds $id_j, k_j$
4. sends $id_j, Enc_{k_j}(m)$

A(K):
- Time - $O(q) = O(2^n)$
- Memory - $O(q) = O(2^n)$

B(K, k):
- Time - $O(q) = O(2^n)$
- Memory - $O(q) = O(2^n)$

E(K):
- Time -  $O(q \cdot q) = O(2^{2n})$
- Memory - $O(q) = O(2^n)$

A -$id_j, Enc_j(K,m)$-> B

**SO** when $n=30$, then A spends $2^{30}$, but E spends $2^{60}$

$n=40$, then A spends $2^{40}$, but E spends $2^{80}$, which is to much