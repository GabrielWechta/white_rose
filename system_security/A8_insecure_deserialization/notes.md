# Insecure Deserialization
### 5
VulnerableTaskHolder.java - holds code for insecure TaskHolder. It has to has .plusHours(-2) cause docker has two hours delay
BuildExploit.java - serializes this TaskHolder.

in A_8_insecure_deserialization/:
$ javac org/dummy/insecure/framework/VulnerableTaskHolder.java
$ javac BuildExlpoit.java
$ java BuildExploit