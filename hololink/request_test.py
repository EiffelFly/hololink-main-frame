import requests



url = "http://35.221.178.255:8080/predict"

data = [
    {
        "name": "螞蟻集團上市 — 無法複製的中國超級平台",
        "content": "今年新創上市熱絡，島讀最近就分析了 5 家。不過它們的估值全部加起來，都還比不上預計將於 9 月上市的中國螞蟻集團。螞蟻集團申請在香港與上海同步上市。一般推測其將募資 300 億美金，估值達 2,000 億美金（約 6 兆台幣）。",
        "from_url": "https://daodu.tech/09-03-2020-ant-group-file-ipo-the-uncopyable-super-app",
        "projects":[19],
        "owned_by":[1]
    }
]

r = requests.post(url, json=data)

print(r.status_code)
print(r.text)
'''
request_session = requests.Session()
get_target_session = request_session.get('https://127.0.0.1:8000') #will change to https://hololink.co after deploying on GCP
get_csrf_token = get_target_session.cookies['csrftoken']

data = {
    "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", #put in the name Hololink_mainframe post to you
    "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", #put in the from_url Hololink_mainframe post to you
    "ner_output":{
        "data":"put NER output here"
    }
    "owned_by":[1],
    "projects":[19,]
}

headers = {
    "X-CSRFToken": get_csrf_token,
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Authorization":"Token " #this token is for demo
}

ner_endpoint = 'https://127.0.0.1:8000/api/ner-result/' #will change to https://hololink.co/api/ner-result after deploying on GCP

post_target = request_session.post(url=ner_endpoint, json = data, headers=headers)

print(post_target.status_code)
print(post_target.text)
'''