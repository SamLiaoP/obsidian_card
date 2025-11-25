
httpbin:
```
import requests 
response = requests.get('https://httpbin.org/ip') 
ip = response.json()['origin'] 
print('My public IP address is:', ip) 
```

ipify:
```
import requests 
response = requests.get('https://api.ipify.org?format=json') 
ip = response.json()['ip'] 
print('My public IP address is ipify:', ip)
```