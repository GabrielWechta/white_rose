# Task 1:
* to get docker with rsacrack* - docker pull b4den/rsacrack
* to get Modulus from crt - `openssl x509 -in cacertificate.pem -noout -modulus`

```
Modulus=E649D57F6FF9CFF655CB79EE38380C8F8278EB374A90059B0FF06534829D337C753D0E59AFED6FA489F015CF33
```

Attack:
1. `openssl x509 -in cacertificate.pem -pubkey -noout > rsa_pub.pem`
2. `docker run -it b4den/rsacrack "$(cat rsa_pub.pem)"`
results are: 

```
[u'1385409854850246784644682622624349784560468558795524903', u'1524938362073628791222322453937223798227099080053904149', 65537L]
```

$ p = 1385409854850246784644682622624349784560468558795524903$

$ q = 1524938362073628791222322453937223798227099080053904149$

$ N = pq $

$ e = 2^{16} + 1 $

$ \phi(N) = (p-1)(q-1) $

$ d = e^{-1} \mod \phi(N) $

after python script 

`d = pow(e, -1, fi)`

$ d = 585377376205045827301220782663105468898592075285171211065018186416365699827074434761795565062334913589643145$ 

Signing:

```
openssl dgst -md5 -sign rsa_priv.pem -out grade.my.sign grade.txt
```

Verifying:

```
openssl dgst -md5 -verify rsa_pub.pem -signature grade.my.sign grade.txt
Verified OK
openssl dgst -md5 -verify <(openssl x509 -in cacertificate.pem -pubkey -noout) -signature grade.my.sign grade.txt
Verified OK
```

# Task 2:
It can not be done in the wat it is formulated.

I ran [`hashclash`](https://github.com/cr-marcstevens/hashclash)  for chosen-prefix collisions.

`bash cpc.sh grade.txt grade_forged.txt`

I got 2 files:

- `grade.txt.coll`
- `grade_forged.txt.coll`

which have the same md5 hash value.
```
$ md5sum grade.txt.coll
97769b8ddab4138b3a71ab352ec9e36b  grade.txt.coll
$ md5sum grade_forged.txt.coll 
97769b8ddab4138b3a71ab352ec9e36b  grade_forged.txt.coll
```

I generated new certificate:
```
$ openssl genrsa -out cakeySec.pem 2048
$ openssl req -new -sha256 -key cakeySec.pem -out cacsrSec.csr
$ openssl req -x509 -sha256 -days 365 -key cakeySec.pem -in cacsrSec.csr -out cacertSec.pem
```
Then, signing `grade.txt.coll` with:

```
$ openssl dgst -md5 -sign cakeySec.pem -out grade.coll.2048.sign grade.txt.coll
```
And verifying signature `grade.coll.2048.sign` while providing forged file `grade_forged.txt.coll`:
```
$ openssl dgst -md5 -verify <(openssl x509 -in cacertSec.pem -pubkey -noout) -signature grade.coll.2048.sign grade_forged.txt.coll

