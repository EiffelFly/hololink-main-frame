import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from timeit import default_timer as timer
import json

data = {
	"D3_data_format": {
		"article_name": "台積電5奈米擴建及3奈米試產 延後2季 | 科技產業 | 產經 | 聯合新聞網",
		"from_url": "https://udn.com/news/story/7240/4604445",
		"recommended":"True",
		"projects": ["科技島讀"],
		"Final": {
			"美國": {
				"Title": "美國",
				"POS": "GPE",
				"Absolute_positions": [
					[
						0,
						2
					],
					[
						239,
						241
					],
					[
						286,
						288
					],
					[
						335,
						337
					]
				],
				"Frequency": 4
			},
			"華": {
				"Title": "華",
				"POS": "GPE",
				"Absolute_positions": [
					[
						5,
						6
					],
					[
						302,
						303
					],
					[
						314,
						315
					],
					[
						617,
						618
					]
				],
				"Frequency": 4
			},
			"技術": {
				"Title": "技術",
				"POS": "Na",
				"Absolute_positions": [
					[
						7,
						9
					],
					[
						225,
						227
					]
				],
				"Frequency": 2
			},
			"台積電": {
				"Title": "台積電",
				"POS": "ORG",
				"Absolute_positions": [
					[
						12,
						15
					],
					[
						72,
						75
					],
					[
						107,
						110
					],
					[
						145,
						148
					],
					[
						169,
						172
					],
					[
						228,
						231
					],
					[
						254,
						257
					],
					[
						264,
						267
					],
					[
						362,
						365
					],
					[
						390,
						393
					],
					[
						453,
						456
					],
					[
						501,
						504
					],
					[
						600,
						603
					],
					[
						634,
						637
					]
				],
				"Frequency": 14
			},
			"五奈米": {
				"Title": "五奈米",
				"POS": "ORG",
				"Absolute_positions": [
					[
						20,
						23
					],
					[
						213,
						216
					],
					[
						351,
						354
					],
					[
						404,
						407
					],
					[
						541,
						544
					]
				],
				"Frequency": 5
			},
			"時間": {
				"Title": "時間",
				"POS": "Na",
				"Absolute_positions": [
					[
						34,
						36
					],
					[
						659,
						661
					]
				],
				"Frequency": 2
			},
			"美": {
				"Title": "美",
				"POS": "GPE",
				"Absolute_positions": [
					[
						0,
						1
					],
					[
						52,
						53
					],
					[
						112,
						113
					],
					[
						187,
						188
					],
					[
						195,
						196
					],
					[
						233,
						234
					],
					[
						239,
						240
					],
					[
						270,
						271
					],
					[
						286,
						287
					],
					[
						335,
						336
					]
				],
				"Frequency": 10
			},
			"中": {
				"Title": "中",
				"POS": "GPE",
				"Absolute_positions": [
					[
						53,
						54
					],
					[
						199,
						200
					],
					[
						234,
						235
					],
					[
						632,
						633
					]
				],
				"Frequency": 4
			},
			"貿易戰": {
				"Title": "貿易戰",
				"POS": "Na",
				"Absolute_positions": [
					[
						54,
						57
					]
				],
				"Frequency": 1
			},
			"鏈": {
				"Title": "鏈",
				"POS": "Na",
				"Absolute_positions": [
					[
						68,
						69
					]
				],
				"Frequency": 1
			},
			"設備商": {
				"Title": "設備商",
				"POS": "Na",
				"Absolute_positions": [
					[
						81,
						84
					]
				],
				"Frequency": 1
			},
			"設備": {
				"Title": "設備",
				"POS": "Na",
				"Absolute_positions": [
					[
						81,
						83
					],
					[
						98,
						100
					]
				],
				"Frequency": 2
			},
			"美方": {
				"Title": "美方",
				"POS": "GPE",
				"Absolute_positions": [
					[
						112,
						114
					],
					[
						270,
						272
					]
				],
				"Frequency": 2
			},
			"禁令": {
				"Title": "禁令",
				"POS": "Na",
				"Absolute_positions": [
					[
						124,
						126
					],
					[
						249,
						251
					],
					[
						622,
						624
					]
				],
				"Frequency": 3
			},
			"申訴期": {
				"Title": "申訴期",
				"POS": "Na",
				"Absolute_positions": [
					[
						130,
						133
					]
				],
				"Frequency": 1
			},
			"變數": {
				"Title": "變數",
				"POS": "Na",
				"Absolute_positions": [
					[
						139,
						141
					]
				],
				"Frequency": 1
			},
			"資本": {
				"Title": "資本",
				"POS": "Na",
				"Absolute_positions": [
					[
						162,
						164
					],
					[
						178,
						180
					]
				],
				"Frequency": 2
			},
			"支出": {
				"Title": "支出",
				"POS": "Na",
				"Absolute_positions": [
					[
						164,
						166
					],
					[
						180,
						182
					]
				],
				"Frequency": 2
			},
			"三奈米": {
				"Title": "三奈米",
				"POS": "QUANTITY",
				"Absolute_positions": [
					[
						26,
						29
					],
					[
						209,
						212
					],
					[
						570,
						573
					],
					[
						654,
						657
					]
				],
				"Frequency": 4
			},
			"七奈米": {
				"Title": "七奈米",
				"POS": "ORG",
				"Absolute_positions": [
					[
						217,
						220
					]
				],
				"Frequency": 1
			},
			"製程": {
				"Title": "製程",
				"POS": "Na",
				"Absolute_positions": [
					[
						223,
						225
					]
				],
				"Frequency": 1
			},
			"科技戰": {
				"Title": "科技戰",
				"POS": "Na",
				"Absolute_positions": [
					[
						235,
						238
					]
				],
				"Frequency": 1
			},
			"商務部": {
				"Title": "商務部",
				"POS": "Nc",
				"Absolute_positions": [
					[
						241,
						244
					]
				],
				"Frequency": 1
			},
			"限制": {
				"Title": "限制",
				"POS": "Na",
				"Absolute_positions": [
					[
						261,
						263
					],
					[
						275,
						277
					]
				],
				"Frequency": 2
			},
			"傷害": {
				"Title": "傷害",
				"POS": "Na",
				"Absolute_positions": [
					[
						277,
						279
					]
				],
				"Frequency": 1
			},
			"政府": {
				"Title": "政府",
				"POS": "Na",
				"Absolute_positions": [
					[
						290,
						292
					]
				],
				"Frequency": 1
			},
			"關係": {
				"Title": "關係",
				"POS": "Na",
				"Absolute_positions": [
					[
						292,
						294
					]
				],
				"Frequency": 1
			},
			"部門": {
				"Title": "部門",
				"POS": "Na",
				"Absolute_positions": [
					[
						294,
						296
					]
				],
				"Frequency": 1
			},
			"編制": {
				"Title": "編制",
				"POS": "Na",
				"Absolute_positions": [
					[
						296,
						298
					]
				],
				"Frequency": 1
			},
			"華府": {
				"Title": "華府",
				"POS": "ORG",
				"Absolute_positions": [
					[
						302,
						304
					]
				],
				"Frequency": 1
			},
			"華為": {
				"Title": "華為",
				"POS": "ORG",
				"Absolute_positions": [
					[
						5,
						7
					],
					[
						314,
						316
					],
					[
						617,
						619
					]
				],
				"Frequency": 3
			},
			"旗下": {
				"Title": "旗下",
				"POS": "Nc",
				"Absolute_positions": [
					[
						316,
						318
					]
				],
				"Frequency": 1
			},
			"海思": {
				"Title": "海思",
				"POS": "ORG",
				"Absolute_positions": [
					[
						318,
						320
					],
					[
						341,
						343
					],
					[
						394,
						396
					],
					[
						479,
						481
					],
					[
						509,
						511
					]
				],
				"Frequency": 5
			},
			"新單": {
				"Title": "新單",
				"POS": "Na",
				"Absolute_positions": [
					[
						320,
						322
					],
					[
						511,
						513
					]
				],
				"Frequency": 2
			},
			"突破點": {
				"Title": "突破點",
				"POS": "Na",
				"Absolute_positions": [
					[
						329,
						332
					]
				],
				"Frequency": 1
			},
			"法規": {
				"Title": "法規",
				"POS": "Na",
				"Absolute_positions": [
					[
						337,
						339
					]
				],
				"Frequency": 1
			},
			"大單": {
				"Title": "大單",
				"POS": "Na",
				"Absolute_positions": [
					[
						359,
						361
					]
				],
				"Frequency": 1
			},
			"方式": {
				"Title": "方式",
				"POS": "Na",
				"Absolute_positions": [
					[
						370,
						372
					]
				],
				"Frequency": 1
			},
			"月": {
				"Title": "月",
				"POS": "Na",
				"Absolute_positions": [
					[
						89,
						90
					],
					[
						115,
						116
					],
					[
						345,
						346
					],
					[
						399,
						400
					],
					[
						411,
						412
					],
					[
						431,
						432
					],
					[
						465,
						466
					],
					[
						583,
						584
					]
				],
				"Frequency": 8
			},
			"產能": {
				"Title": "產能",
				"POS": "Na",
				"Absolute_positions": [
					[
						407,
						409
					],
					[
						432,
						434
					],
					[
						462,
						464
					],
					[
						647,
						649
					]
				],
				"Frequency": 4
			},
			"增幅": {
				"Title": "增幅",
				"POS": "Na",
				"Absolute_positions": [
					[
						422,
						424
					]
				],
				"Frequency": 1
			},
			"蘋果": {
				"Title": "蘋果",
				"POS": "Na",
				"Absolute_positions": [
					[
						444,
						446
					],
					[
						457,
						459
					]
				],
				"Frequency": 2
			},
			"限期": {
				"Title": "限期",
				"POS": "Na",
				"Absolute_positions": [
					[
						381,
						383
					],
					[
						495,
						497
					]
				],
				"Frequency": 2
			},
			"廠": {
				"Title": "廠",
				"POS": "Nc",
				"Absolute_positions": [
					[
						525,
						526
					]
				],
				"Frequency": 1
			},
			"P3": {
				"Title": "P3",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						530,
						532
					]
				],
				"Frequency": 1
			},
			"強化版": {
				"Title": "強化版",
				"POS": "Na",
				"Absolute_positions": [
					[
						544,
						547
					]
				],
				"Frequency": 1
			},
			"計畫": {
				"Title": "計畫",
				"POS": "Na",
				"Absolute_positions": [
					[
						547,
						549
					]
				],
				"Frequency": 1
			},
			"試產線": {
				"Title": "試產線",
				"POS": "Na",
				"Absolute_positions": [
					[
						573,
						576
					]
				],
				"Frequency": 1
			},
			"二奈米": {
				"Title": "二奈米",
				"POS": "PERSON",
				"Absolute_positions": [
					[
						356,
						359
					],
					[
						608,
						611
					]
				],
				"Frequency": 2
			},
			"客戶": {
				"Title": "客戶",
				"POS": "Na",
				"Absolute_positions": [
					[
						645,
						647
					]
				],
				"Frequency": 1
			},
			"法說會": {
				"Title": "法說會",
				"POS": "Na",
				"Absolute_positions": [
					[
						664,
						667
					]
				],
				"Frequency": 1
			},
			"明年第一季": {
				"Title": "明年第一季",
				"POS": "DATE",
				"Absolute_positions": [
					[
						44,
						49
					],
					[
						562,
						567
					],
					[
						593,
						598
					]
				],
				"Frequency": 3
			},
			"一百六十億美元": {
				"Title": "一百六十億美元",
				"POS": "MONEY",
				"Absolute_positions": [
					[
						190,
						197
					]
				],
				"Frequency": 1
			},
			"三萬": {
				"Title": "三萬",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						437,
						439
					],
					[
						473,
						475
					],
					[
						536,
						538
					]
				],
				"Frequency": 3
			},
			"第三": {
				"Title": "第三",
				"POS": "ORDINAL",
				"Absolute_positions": [
					[
						526,
						528
					]
				],
				"Frequency": 1
			},
			"七月": {
				"Title": "七月",
				"POS": "DATE",
				"Absolute_positions": [
					[
						88,
						90
					]
				],
				"Frequency": 1
			},
			"十八廠": {
				"Title": "十八廠",
				"POS": "ORG",
				"Absolute_positions": [
					[
						523,
						526
					]
				],
				"Frequency": 1
			},
			"五月十五日": {
				"Title": "五月十五日",
				"POS": "DATE",
				"Absolute_positions": [
					[
						114,
						119
					],
					[
						344,
						349
					]
				],
				"Frequency": 2
			},
			"二季": {
				"Title": "二季",
				"POS": "DATE",
				"Absolute_positions": [
					[
						38,
						40
					],
					[
						554,
						556
					]
				],
				"Frequency": 2
			},
			"美國商務部": {
				"Title": "美國商務部",
				"POS": "ORG",
				"Absolute_positions": [
					[
						239,
						244
					]
				],
				"Frequency": 1
			},
			"二周": {
				"Title": "二周",
				"POS": "DATE",
				"Absolute_positions": [
					[
						127,
						129
					]
				],
				"Frequency": 1
			},
			"五": {
				"Title": "五",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						20,
						21
					],
					[
						114,
						115
					],
					[
						117,
						118
					],
					[
						184,
						185
					],
					[
						213,
						214
					],
					[
						344,
						345
					],
					[
						347,
						348
					],
					[
						351,
						352
					],
					[
						404,
						405
					],
					[
						410,
						411
					],
					[
						541,
						542
					]
				],
				"Frequency": 11
			},
			"四成": {
				"Title": "四成",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						425,
						427
					]
				],
				"Frequency": 1
			},
			"一百二十天": {
				"Title": "一百二十天",
				"POS": "DATE",
				"Absolute_positions": [
					[
						375,
						380
					],
					[
						489,
						494
					]
				],
				"Frequency": 2
			},
			"今年六月": {
				"Title": "今年六月",
				"POS": "DATE",
				"Absolute_positions": [
					[
						580,
						584
					]
				],
				"Frequency": 1
			},
			"二萬多": {
				"Title": "二萬多",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						400,
						403
					]
				],
				"Frequency": 1
			},
			"一千": {
				"Title": "一千",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						418,
						420
					]
				],
				"Frequency": 1
			},
			"百分之八十": {
				"Title": "百分之八十",
				"POS": "PERCENT",
				"Absolute_positions": [
					[
						201,
						206
					]
				],
				"Frequency": 1
			},
			"一百五十億美元": {
				"Title": "一百五十億美元",
				"POS": "MONEY",
				"Absolute_positions": [
					[
						182,
						189
					]
				],
				"Frequency": 1
			},
			"今年": {
				"Title": "今年",
				"POS": "DATE",
				"Absolute_positions": [
					[
						92,
						94
					],
					[
						176,
						178
					],
					[
						580,
						582
					]
				],
				"Frequency": 3
			},
			"近三萬": {
				"Title": "近三萬",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						436,
						439
					],
					[
						535,
						538
					]
				],
				"Frequency": 2
			},
			"今年底": {
				"Title": "今年底",
				"POS": "DATE",
				"Absolute_positions": [
					[
						92,
						95
					]
				],
				"Frequency": 1
			},
			"五月": {
				"Title": "五月",
				"POS": "DATE",
				"Absolute_positions": [
					[
						114,
						116
					],
					[
						344,
						346
					],
					[
						410,
						412
					]
				],
				"Frequency": 3
			},
			"下月": {
				"Title": "下月",
				"POS": "DATE",
				"Absolute_positions": [
					[
						464,
						466
					]
				],
				"Frequency": 1
			},
			"全年": {
				"Title": "全年",
				"POS": "DATE",
				"Absolute_positions": [
					[
						160,
						162
					]
				],
				"Frequency": 1
			},
			"上周": {
				"Title": "上周",
				"POS": "DATE",
				"Absolute_positions": [
					[
						75,
						77
					]
				],
				"Frequency": 1
			},
			"十二奈米": {
				"Title": "十二奈米",
				"POS": "QUANTITY",
				"Absolute_positions": [
					[
						355,
						359
					]
				],
				"Frequency": 1
			},
			"二點七萬": {
				"Title": "二點七萬",
				"POS": "CARDINAL",
				"Absolute_positions": [
					[
						447,
						451
					]
				],
				"Frequency": 1
			}
		},
		"username": "hololink"
	}
}

with open('1028.json', 'r', encoding='utf-8') as file:
	target_file = json.load(file)

request_session = requests.Session()
# get_target_session = request_session.get('https://') #will change to https://hololink.co after deploying on GCP
# get_csrf_token = get_target_session.cookies['csrftoken']

headers = {
    # "X-CSRFToken": get_csrf_token,
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Authorization":"Token 78602c22bc09d0669bd14895264f083bcebc6e93" #this token is for demo
}

ner_endpoint = 'http://127.0.0.1:8000/api/ner-result/' #will change to https://hololink.co/api/ner-result after deploying on GCP

start = timer()  
post_target = request_session.post(url=ner_endpoint, json = target_file, headers=headers)
ml_end = timer()



print(post_target.status_code)
print(post_target.text)
print(start-ml_end)


'''
data = {
    "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", #put in the name Hololink_mainframe post to you
    "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", #put in the from_url Hololink_mainframe post to you
    "ner_output":{
        "data":"put NER output here"
    }
    "owned_by":[1],
    "projects":[19,]
}
'''
'''
data = [
    {
        "name": "螞蟻集團上市 — 無法複製的中國超級平台",
        "content": "今年新創上市熱絡，島讀最近就分析了 5 家。不過它們的估值全部加起來，都還比不上預計將於 9 月上市的中國螞蟻集團。螞蟻集團申請在香港與上海同步上市。一般推測其將募資 300 億美金，估值達 2,000 億美金（約 6 兆台幣）。",
        "from_url": "https://daodu.tech/09-03-2020-ant-group-file-ipo-the-uncopyable-super-app",
        "projects":[19],
        "owned_by":[1]
    }
]

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

url = "http://127.0.0.1:8000/api/ner-result/"
start = timer()  
ml_result = session.post(url, json=data)
ml_end = timer()
print(ml_result.status_code)
print(ml_result.text)

'''


'''
a = ['sks']

list = [{"a":'sks', "b":20},{"a":2, "b":34}]

list_a = [ (dict if dict['b'] > 30 ) if dict['a'] in a for dict in list]

print(list_a)

url = "http://35.201.255.213:8080/predict"

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