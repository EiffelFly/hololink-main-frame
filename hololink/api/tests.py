from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from project.models import Project
from django.contrib.auth.models import User

# Create your tests here.


class DRFWorkflowTest(APITestCase):
    def testMergeArticleIntoGalaxy(self):

        token = Token.objects.get(User='eiffelfly')

        # init Project.object ner_test
        try:
            project = Project.objects.get(name="merge_article_into_galaxy_test")
            project.project_d3_json = {"nodes":[],"links":[]}
            keyword_list = {"total":[],"basestone":[],"stellar":[]}
            project.articles_project_owned.clear()
        except Project.DoesNotExist:
            user = User.objects.get(username="eiffelfy")
            project = Project.objects.create(name="merge_article_into_galaxy_test", created_by=user, project_visibility='private')

        # With django native request object map additional headers in a specific way: converted every data in headers into META
        # we have to follow that
        # content_tpye -> HTTP_CONTENT_TYPE
        # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META

        headers = {
            "HTTP_CONTENT_TYPE": "application/json",
            "HTTP_X_REQUESTED_WITH": "XMLHttpRequest",
            "HTTP_AUTHORIZATON":f"Token {token.key}" #this token is for demo
        }

        new_article_old_keywords_data = {
            "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", 
            "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", 
            "ner_output": {
                "title": "台積電5奈米擴建及3奈米試產 延後2季 | 科技產業 | 產經 | 聯合新聞網",
                "url": "https://udn.com/news/story/7240/4604445",
                "galaxy": "台積電三奈米",
                "content": "美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季，將待美中貿易戰明朗化後再做定奪。供應鏈透露，台積電上周緊急通知設備商，原訂自七月起到今年底交貨的設備，全暫停交貨。台積電坦承美方五月十五日頒布新出口禁令，二周的申訴期極為關鍵，若變數未釐清，台積電就會被迫調整，但尚無下修全年資本支出打算。台積電稍早公布今年資本支出一百五十億美元至一百六十億美元，其中約百分之八十將用於三奈米、五奈米與七奈米等先進製程技術。台積電捲入美中科技戰，美國商務部頒布新出口禁令後，對台積電帶來極大限制。台積電為突破美方新出口限制傷害，近期也擴大在美國負責政府關係部門編制，極力與華府溝通。另一方面也停接華為旗下海思新單，避免在未找到突破點前觸犯美國法規，但海思在五月十五日下的五奈米及十二奈米大單，台積電已透過增產方式，趕在一百二十天寬限期交貨。據了解，台積電為海思提供每月二萬多片五奈米產能，五月起拉升至每天一千片，增幅逾四成，換算每月產能推升近三萬片，已超過蘋果的二點七萬片，台積電為蘋果備買的產能下月仍預定將拉升至三萬片，將與海思相近。不過，由於一百二十天寬限期截止後，台積電即不再承接海思新單，因此原本預定打算在十八廠第三期（P3）擴增近三萬片的的五奈米強化版計畫，決定延後二季，預定順延至明年第一季。至於三奈米試產線，原預定今年六月裝設，也同步順延至明年第一季。但台積電內部透露，二奈米研發仍不會受華為新出口禁令影響，仍加速進行中。台積電表示不會透露個別客戶產能配置，至於三奈米試產時間，將於法說會對外說明。",
                "POS": {
                    "二奈米": {
                        "Title": "二奈米",
                        "POS": "Na",
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
                    }
                },
                "NER": {
                    "二奈米": {
                        "Title": "二奈米",
                        "POS": "Na",
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
                    }
                },
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
                    }
                }
            }
        }

        response = self.client.post('https://hololink.co/api/ner-result',content_type='application/json' ,data=new_article_old_keywords_data, **headers)



if __name__ == "__main__":
    pass