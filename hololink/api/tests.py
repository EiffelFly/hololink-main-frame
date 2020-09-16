from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from project.models import Project
from article.models import Article
from django.contrib.auth.models import User
import json
# Create your tests here.


class DRFWorkflowTest(APITestCase):
    def testMergeNewArticleIntoGalaxy(self):

        # init user object and token
        user = User.objects.create(username="eiffelfly", email="eric525282@gmail.com")
        user.save()
        token = Token.objects.create(user=user)
        token.save()

        # init Project.object ner_test
        project = Project.objects.create(name="merge_article_into_galaxy_test", created_by=user, project_visibility='private')
        project.save()

        # init a set of Article.object 
        article = Article.objects.create(
            name = "蘋果、Epic Games 與爭奪虛構宇宙入口",
            from_url = "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance",
            content = "美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季，將待美中貿易戰明朗化後再做定奪。",
        )
        article.owned_by.add(user)
        article.projects.add(project) # Article 在首次由使用者 post 上來時已經存入該使用者指定的 project 裡
        article.save()


        # With django native request object map additional headers in a specific way: converted every data in headers into META
        # we have to follow that
        # content_tpye -> HTTP_CONTENT_TYPE
        # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
        # the way setting up token auth: https://stackoverflow.com/questions/53107824/how-to-write-django-unit-test-for-authentication-protected-rest-apis

        headers = {
            "HTTP_CONTENT_TYPE": "application/json",
            "HTTP_X_REQUESTED_WITH": "XMLHttpRequest",
            "HTTP_AUTHORIZATION":f"Token {token.key}" #this token is for demo
        }

        # Test condition: new keywords

        new_article_new_keywords_data = {
            "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", 
            "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", 
            "projects": [1],
            "owned_by": [1],
            "ner_output": {
                "title": "蘋果、Epic Games 與爭奪虛構宇宙入口",
                "url": "https://udn.com/news/story/7240/4604445",
                "galaxy": "merge_article_into_galaxy_test",
                "content": "美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季，將待美中貿易戰明朗化後再做定奪。",
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

        response = self.client.post("http://127.0.0.1:8000/api/ner-result/",content_type="application/json" ,data=json.dumps(new_article_new_keywords_data), **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project_result = Project.objects.get(name="merge_article_into_galaxy_test")
        result_keywords_list = {
            "total":["美國", "華", "技術", "台積電"],
            "stellar":["技術"],
            "basestone":["美國", "華", "台積電"],
        }

        self.assertEqual(json.dumps(project_result.keyword_list), json.dumps(result_keywords_list))

        # Test condition: old keywords with some new keywords
        
        print(project_result.articles_project_owned.all())

        new_article_old_keywords_data = {
            "name": "蘋果、Epic Games 與爭奪虛構宇宙入口",
            "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance",
            "projects": [1],
            "owned_by": [1],
            "ner_output": {
                "title": "蘋果、Epic Games 與爭奪虛構宇宙入口",
                "url": "https://udn.com/news/story/7240/4604445",
                "galaxy": "merge_article_into_galaxy_test",
                "content": "美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季，將待美中貿易戰明朗化後再做定奪。",
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
                    },
                    "test": { 
                        "Title": "test",
                        "POS": "Na",
                        "Absolute_positions": [
                            [
                                450,
                                453
                            ]
                        ],
                        "Frequency": 4
                    }
                }
            }
        }

        second_response = self.client.post("http://127.0.0.1:8000/api/ner-result/",content_type="application/json" ,data=json.dumps(new_article_old_keywords_data), **headers)

        second_project_result = Project.objects.get(name="merge_article_into_galaxy_test")
        second_result_keywords_list = {
            "total":["美國", "華", "技術", "台積電", "test"],
            "stellar":["技術", "test"],    
            "basestone":["美國", "華", "台積電"],
        }

        self.assertEqual(json.dumps(second_project_result.keyword_list), json.dumps(second_result_keywords_list))
