# Bypass front-end restrictions
# 2
1. open Burp
2. intercept request and change it's content:

select=option3&radio=option3&checkbox=maybe&shortInput=1234567890&readOnlyInput=change2

# 3
1. open Burp
2. intercept request and change it's content:

field1=abcd&field2=123d&field3=abc+1.23+ABC&field4=eleven&field5=0A1101&field6=90210-1111231&field7=301-604-4882d&error=0


# Client side filtering
# 2
1. open Burp
2. intercept request after clicking on dropdown menu, send it to repeater:
3. find Neville Bartholomew salary


# 3
1. open Burp
2. after typing something into coupon field intercept request /WebGoat/clientSideFiltering/challenge-store/coupons/{input} and change it to /WebGoat/clientSideFiltering/challenge-store/coupons:
3. receive all coupons in response

# HTML tampering

# 2a
1. open Burp
2. change values in intercepted request




