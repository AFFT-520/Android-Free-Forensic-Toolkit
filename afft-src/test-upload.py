#!/usr/bin/env python

import requests, base64

url = 'https://192.168.56.102/index.php'
toupload=open('./testupload.db', 'rb')
content=toupload.read()
contentb64=base64.b64encode(content)
contentb64=str(contentb64)
contentb64=contentb64.replace("+","-")
contentb64=contentb64.replace("/","_")
contentb64=contentb64.replace("=",".")
contentb64=contentb64[2:-1]
print(contentb64)
r = requests.post(url, data={'file': contentb64}, verify=False)
print(r.text)