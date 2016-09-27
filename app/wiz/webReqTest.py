import requests
import datetime
req = requests.post("http://localhost:8001/homepage/api/user/n/",data={'username':'user1','datetime':str(datetime.datetime.now())})
print(req.text[:300] + '...')


