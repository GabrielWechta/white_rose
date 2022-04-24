# Merkel Puzzle cryptosystem using AES-GCM

## Responder
$R$ generates: $(\tilde{k_i}, k_i, id_i)$ then $c_i = Enc_{\tilde{k_i}}(k_i \mathbin\Vert id_i)$

where $\tilde{k_i}$ - is a weak key that can be guessed in time $q$.

$n = 30$

$q = 2^n$
        
Then:

- PubKeys: ${(c_1, t_1), (c_2, t_2), \ldots , (c_q, t_q)}$
  - $c_i$ stands both for ciphertext.
  - $(c_i, t_i)$ is challenge.

- PrivKeys: ${(id_1, k_1), (id_2, k_2), \ldots, (id_q, k_q)}$	
  - $id_i$ is $i$-th key identifier.
  - $k_i$ is $i$-th key.

---
## Initiator
$I(\{(c_1, t_1), (c_2, t_2), \ldots , (c_q, t_q)\},m$):

1. selects $j \leftarrow {1, \ldots, q}$
2. computes $\tilde{k_j}$ in loop, as follows:
   1. $\tilde{k_j} \coloneqq \tilde{k_j} + 1$
   2. $(\dot{k_j} \mathbin\Vert \dot{id_j}), \dot{t_j} \leftarrow Dec_{\tilde{k_j}}(c_j)$
   3. if $\dot t_j == t_j$:
      1. $id_j \coloneqq \dot{id_j}$
      2. $k_j \coloneqq \dot{k_j}$
      3. break loop
3. sends $id_j, Enc_{k_j}(m)$ to Responder.

---
## Time complexity
$R(\text{PrivKeys}, \text{PubKeys}))$:
- Time - $O(q) = O(2^n)$
- Memory - $O(q) = O(2^n)$

$I(\text{PubKeys})$:
- Time - $O(q) = O(2^n)$
- Memory - $O(q) = O(2^n)$

$Eve(\text{PubKeys})$:
- Time -  $O(q \cdot q) = O(2^{2n})$
- Memory - $O(q) = O(2^n)$
---
## Implementation
for $i \in \{0,1, \ldots, 2^n -1 \}$
- $id_i$ is 32-bytes number. $id_i \leftarrow_{\$} [0, 2^{256}]$, without repetitions 
- $k_i$ is 32-bytes number. $k_i \leftarrow_{\$} [0, 2^{256}]$ 
- $\tilde{k_i}$ is 32-bytes number. $\tilde{k_i} \leftarrow_{\$} [0, 2^{n} - 1]$

--- 
public challenge looks like this:
```
	key_id_bytes = plaintext[:32]
	key_bytes = plaintext[32:]
```
so after decrypting, both values always take exactly 32 bytes.