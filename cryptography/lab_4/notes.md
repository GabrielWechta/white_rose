We weill use - $\text{AES-CBC}^*$

Also we will see something about $\text{ECB}$. it is **deterministic**.

in AES:
$AES: \{0,1\}^l X \{0,1\}^n \rightarrow \{0,1\}^n$ 

where:	
- $l - 128, 256, ...$ - key length
- $n$ - plaintext length

**modes of encryption** allow to make:

$AES: \{0,1\}^l X \{0,1\}^* \rightarrow \{0,1\}^*$ 

We will show that AES-CBC is not CCA-secure

The problem:

$-(IV, ...)->$

$-(IV + 1, ...)->$

Think about key stores.

Solution:
1. Implement $O_{CBC}$.
2. Design the Adversary that wins the CCA game. It may requiere only the 2-part and 3-part.