from django.urls import get_resolver
from django.conf import settings
import sys, os, django



sys.path.append(os.path.dirname(os.path.abspath('test.py')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hololink.settings")
django.setup()

from django.contrib.auth.tokens import default_token_generator

#for k, v in get_resolver(None).reverse_dict.items():




a = ([('@%(slug)s/', ['slug'])], '@(?P<slug>[-a-zA-Z0-9_]+)/$', {}, {'slug': 'django'})

print(a[0][0][1][0])
addr = str(a[0][0][0])
print(addr)
link = 'https://hololink.co/' + addr[0: addr.index('%')] + '1265554'
print(link)