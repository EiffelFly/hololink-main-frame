from django.urls import get_resolver
from django.conf import settings
import sys, os, django


sys.path.append(os.path.dirname(os.path.abspath('test.py')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hololink.settings")
django.setup()


for k, v in get_resolver(None).reverse_dict.items():
    print(k)