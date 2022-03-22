# Task 1:
*to get docker with rsacrack* - docker pull b4den/rsacrack
*to get Modulus from crt* - openssl x509 -in cacertificate.pem -noout -modulus
Modulus=E649D57F6FF9CFF655CB79EE38380C8F8278EB374A90059B0FF06534829D337C753D0E59AFED6FA489F015CF33

Attack:
1. openssl x509 -in cacertificate.pem -pubkey -noout > rsa_pub.pem
2. docker run -it b4den/rsacrack "$(cat rsa_pub.pem)"
[*] results are: [u'1385409854850246784644682622624349784560468558795524903', u'1524938362073628791222322453937223798227099080053904149', 65537L]

$ p = 1385409854850246784644682622624349784560468558795524903$

$ q = 1524938362073628791222322453937223798227099080053904149$

$ N = pq $

$ e = 2^{16} + 1 $

$ \phi(N) = (p-1)(q-1) $

$ d = e^{-1} \mod \phi(N) $

after python script 

`d = pow(e, -1, fi)`

$ d = 585377376205045827301220782663105468898592075285171211065018186416365699827074434761795565062334913589643145$ 

# Task 2:
It can not be done in the wat it is formulated.