# HTTP Basics
2. simply put my name
3. I opened Wireshark, started listening on docker interface. Checked the body of the HTTP POST request.

# HTTP Proxies
6. Intercepted request using ZAP and:
    - changed method to GET
    - added a header 'x-request-intercepted:true'
    - added field changeMe = Requests are tampered easily

# Developer tools
4. get output from json webgoat.customjs.phoneHome() in the JS console.
6. open Dev tools -> click "Go!" button and check payload of the latest 'network' packet.

# CIA Triad
5. choose proper answers from the checkboxes.

# Crypto
2. 
$ echo -n Z2FicmllbDpzZWNyZXQ= | base64 -d 
	returns "gabriel:secret"

3. 
{xor}Oz4rPj0+LDovPiwsKDAtOw== decoded returned databasepassword
The hash is than base64 decoded and each character is XORred against an underscore (ASCII 95).
good read: https://strelitzia.net/wp/blog/2011/05/17/decoding-websphere-passwords/

4. 
I guessed it is MD5 :
MD5("admin") = 21232f297a57a5a743894a0e4a801fc3

For the second part I used https://hashtoolkit.com/ and found matching hash for sha256:
sha_256("123456") = 8D969EEF6ECAD3C29A3A629280E686CF0C3F5D5A86AFF3CA12020C923ADC6C92 

6.
$ openssl rsa -in privkey.key -noout -modulus
returns: 
Modulus=B6762FBB3AB1FABC2D4F85BE8822D7D7A4BFB3128029392765A34B954BB656C9FD3172E9A8843A8FAB6E1B8EF1C728A83189DD8CC5D087842262338C5DD4C2EA484E37C36B064FAC2812719C6713F35A5D2DA253C69CA0090843E42642F026B0C9F2A4716C02C1400A58E116A9863FBB27E1096E212650A0F131B613E83DF8F33B9C7BB4B43FDFE4591CFD5405039BCA9BCA2362F06D4F190A67BAE87C6D7D7EACB195995A9EBA2BE28A4A73DA8898DEB5412DF3723B904EE2A5BC435A58F6E35557C78617E02F054F7E6CC0DB59DE5B9299634EA6459E29F05AF8E8363492ADB43DA0797728D415F43C65BF121FD83BB92DE6FFA30E76418FDB312631899F9D

$ echo -n "B6762FBB3AB1FABC2D4F85BE8822D7D7A4BFB3128029392765A34B954BB656C9FD3172E9A8843A8FAB6E1B8EF1C728A83189DD8CC5D087842262338C5DD4C2EA484E37C36B064FAC2812719C6713F35A5D2DA253C69CA0090843E42642F026B0C9F2A4716C02C1400A58E116A9863FBB27E1096E212650A0F131B613E83DF8F33B9C7BB4B43FDFE4591CFD5405039BCA9BCA2362F06D4F190A67BAE87C6D7D7EACB195995A9EBA2BE28A4A73DA8898DEB5412DF3723B904EE2A5BC435A58F6E35557C78617E02F054F7E6CC0DB59DE5B9299634EA6459E29F05AF8E8363492ADB43DA0797728D415F43C65BF121FD83BB92DE6FFA30E76418FDB312631899F9D" | openssl dgst -sha256 -sign privkey.key |base64 > tmp

returns:
chzwndVe5BPdJ96HG2XMHBgHcNGCz2yel1ANtAbAj5ksZaC+XNU4ifPj88zFA3/keuLZXq2wGSH0
kmGuAX5bHz8FrSkk83x8kSlUIOVyEKIO2s0niAROSfCTDd27pS4ktHS5a0OP+Q+oKTa343X8/og6
zyWoUwtD7MdMd+WfjpQFwKmmbtzK4WjMGlezxrdDnC8YQDOi+cu5ITzc12Cooa7NAhhf9VVmDVLC
SO/10+99WSRJwhHGM0rUOMbqLSbYw5t3ZRQabDMzfpBDHe9E0B8xYIYnON9LvKEM7EUQaKbC04/z
WRvs6STzEvbC5xQsWE2dMa6MQ4Vv5LCpIJ79yw==

8.
$ docker run -d webgoat/assignments:findthesecret

$ docker cp {docker_name}:/etc/passwd default.passwd

/# changing webgoat UID and GID to 0.

$ docker cp default.passwd {docker_name}:/etc/passwd

$ docker exec -it {docker_name} /bin/bash

$ cd root

$ echo "U2FsdGVkX199jgh5oANElFdtCxIEvdEvciLi+v+5loE+VCuy6Ii0b+5byb5DXp32RPmT02Ek1pf55ctQN+DHbwCPiVRfFQamDmbHBUpD7as=" | openssl enc -aes-256-cbc -d -a -kfile default_secret  

# Writing lesson 
6. param1 must equal "secr37Value"
