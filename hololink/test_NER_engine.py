
import requests

c = {
    "content":'aaaaa',
    "test":'sddde'
}

a = "test"

print(c[f'{a}'])

'''
data = [
    {
        "name":"台積電5奈米擴建及3奈米試產 延後2季 | 科技產業 | 產經 | 聯合新聞網", #put in the name Hololink_mainframe post to you
        "from_url": "https://udn.com/news/story/7240/4604445", #put in the from_url Hololink_mainframe post to you
        "content":"美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季",
        "galaxy":"台積電三奈米",
    },
]

url="http://35.221.178.255:8080/predict"

post_target = requests.post(url=url, json = data)

print(post_target.status_code)
print(post_target.text)

data = {'name': contents[0]['name'],
                'from_url': contents[0]['from_url'],
                'ner_output': contents[0],
                }
print('data process Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print(data)


headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Authorization":"Token 7040fe57d322fdf29585595e39deea0c0badb4c1"
        }
ner_endpoint = 'https://hololink.co/api/ner-result/'
post_target = requests.post(url=ner_endpoint, json=data, headers=headers)

contents[0]['post_status']=post_target.status_code
contents[0]['post_result']=post_target.reason

print(post_target.status_code)
print(post_target.text)
'''