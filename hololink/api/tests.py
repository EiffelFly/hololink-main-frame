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
        except Project.DoesNotExist:
            user = User.objects.get(username="eiffelfy")
            project = Project.objects.create(name="merge_article_into_galaxy_test", created_by=user, project_visibility='private')

        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Authorization":f"Token {token.key}" #this token is for demo
        }

        data = {
            "name":"蘋果、Epic Games 與爭奪虛構宇宙入口", --
            "from_url": "https://daodu.tech/08-20-2020-apple-epic-games-and-the-fight-for-metaverse-entrance", 
            "ner_output": {
                "data":"put NER output here"
            }
        }

if if __name__ == "__main__":
    pass