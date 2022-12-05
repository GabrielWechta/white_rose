# SIGMA (sign-and-MAC)

An example of an authenticated key exchange protocol is **SIGMA** (SIGn-and-MAc). This protocol assumes that there exist: a secure signature scheme $\mathrm{SS}$, secure **message authentication code** scheme $\mathrm{MAC}$ and a pseudorandom function $\mathrm{PRF}$. We can model $\mathrm{MAC}$ and $\mathrm{PRF}$ using a hash (a random oracle model).

In the protocol we have two parties: Alice $\hat{A}(a, A)$ and Bob $\hat{B}(a, B)$. Alice chooses $x \in_R \mathbb{Z}_q^*$ and sends $X = g^x$ over to Bob along with a session identifier $s$ and her certificate (certified public key):

$$ \hat{A} \xrightarrow{s, X, A} \hat{B} $$

Bob chooses $y \in_R \mathbb{Z}_q^*$ and computes an **intermediate key** $K = X^y$ as well as the ephemeral value $Y = g^x$. Then Bob computes $K_0, K_1$ using the pseudorandom function over the intermediate key and the numbers $0, 1$, respectively:

$$ K_0 = \mathrm{PRF}(K, 0) $$

$$ K_1 = \mathrm{PRF}(K, 1) $$

Bob produces a signature over the ephemeral values $X,Y$ and Bob's role:

$$ \sigma_B = \mathrm{Sign}((X, Y, 1), b)$$

where $1$ denotes that Bob is the *responder*, as well as the message authentication code with the key $K_0$ for his own identity:

$$ M_B = \mathrm{MAC}(K_0, B) $$

("I am the party who uses $K_0$ computed using $X^y$ who proves the identity $B$").
Bob sends all the computed values along with the session identifier and his certificate/public key $B$ back to Alice:

$$ \hat{A} \xleftarrow{s, Y, \sigma_B, M_B, B} \hat{B} $$

Alice verifies the signature (note that Alice expects the message $(X, Y, 1)$ as she expects Bob to identify as the responder):

$$ \mathrm{Ver}(\sigma_B, (X, Y, 1), B) \rightarrow 1 $$

If the signature verification passes, Alice verifies the message authentication code by computing:

$$ K = Y^x = g^{xy} $$

$$ K_0 = \mathrm{PRF}(K, 0) $$

$$ K_1 = \mathrm{PRF}(K, 1) $$

and checking that:

$$ M_B' = \mathrm{MAC}(K_0, B) $$

matches the MAC sent by Bob - $M_B$. If the verification passes Alice sends to Bob the session identifier, her signature and her MAC:

$$ \hat{A} \xrightarrow{s, \sigma_A, M_A} \hat{B} $$

where:

$$ \sigma_A = \mathrm{Sign}((X, Y, 0), a) $$

and:

$$ M_A = \mathrm{MAC}(K_0, A) $$

Bob then verifies Alice's signature and MAC:

$$ \mathrm{Ver}(\sigma_A, (X, Y, 0), A) $$

$$ M_A' = \mathrm{MAC}(K_0, A) $$

If the verification succeeds Bob concludes he is indeed talking to Alice. As the session key the value $K_1$ is being used.

Note that the scheme provides perfect forward secrecy since the session key is computed as a pseudorandom function over ephemeral values, e.g. for $i$-th session we have:

$$ K_1^{(i)} = \mathrm{PRF}(g^{x_iy_i}, 1) $$

where $x_i, y_i$ were chosen at random for this session only.
