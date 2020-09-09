import requests

request_session = requests.Session()
get_target_session = request_session.get('https://127.0.0.1:8000') #will change to https://hololink.co after deploying on GCP
get_csrf_token = get_target_session.cookies['csrftoken']

data = {
    "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", #put in the name Hololink_mainframe post to you
    "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", #put in the from_url Hololink_mainframe post to you
    "ner_output":{
        "data":"put NER output here"
    }
}

headers = {
    "X-CSRFToken": get_csrf_token,
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Authorization":"Token dc7a52ed89a638ec3236685a1d2005b1b242b262"
}

ner_endpoint = 'https://127.0.0.1:8000/api/ner-result/' #will change to https://hololink.co/api/ner-result after deploying on GCP

post_target = request_session.post(url=ner_endpoint, json = data, headers=headers)

print(post_target.status_code)
print(post_target.text)
