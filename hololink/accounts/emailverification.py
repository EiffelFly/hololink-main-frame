from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from base64 import urlsafe_b64decode, urlsafe_b64encode
from threading import Thread
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .views import verify
from django.urls import get_resolver

'''
    This python file is especially for verify user signup.
    Code Reference as below:
    1. https://github.com/LeoneBacciu/django-email-verification
    2. https://stackoverflow.com/questions/24935271/django-custom-user-email-account-verification

'''

def sendVerification(user, **kwargs):
    try:
        setattr(user, 'is_active', False) #將 user status 改為 in_active
        user.save()

        token = default_token_generator.make_token(user)

        email = urlsafe_b64encode(str(kwargs['email']).encode('utf-8'))
        print(urlsafe_b64encode('eric525282@gmail.com'.encode('utf-8')))

        t = Thread(target=sendVerification_thread, args=(user.email, f'{email.decode("utf-8")}/{token}'))
        t.start()
    except AttributeError:
        raise InvalidUserModel('The user model you provided is invalid')


def sendVerification_thread(email, token):

    user = get_user_model().objects.filter(email=urlsafe_b64decode(email).decode("utf-8"))

    subject = 'Welcome to Hololink, please verify your E-mail address'
    signup_verification_email_text = GetFieldAndValidate('SIGNUP_VERIFICATION_EMAIL_TEXT', raise_error=False)
    signup_verification_email_html = GetFieldAndValidate('SIGNUP_VERIFICATION_EMAIL_HTML', raise_error=False)
    domain = GetFieldAndValidate('EMAIL_VERIFICATION_PAGE_DOMAIN')
    from_email = settings.DEFAULT_FROM_EMAIL

    if not (signup_verification_email_html and signup_verification_email_text): 
        raise NotAllFieldCompiled(f"Both SIGNUP_VERIFICATION_EMAIL_HTML and SIGNUP_VERIFICATION_EMAIL_TEXT missing from settings.py, two of them is necessary")

    domain += '/' if not domain.endswith('/') else '' #make sure domain is endwith /

    try:
        if '_' in user.username:
            username_readable = ' '.join([word[0].upper() + word[1:] for word in user.username.split('_')])
        else:
            username_readable = user.username
    except Exception:
        username_readable = user.username

    '''
        Generate verification link
        get_resolver(None) 會將 settings.ROOT_URLCONF 下 url 叫出來，而由於
        此專案的 settings.ROOT_URLCONF 設定為 hololink.urls get_resolver(None) 會叫出所有 url

        k : <function user_public_profile at 0x000000000413F168>
        v : ([('@%(slug)s/', ['slug'])], '@(?P<slug>[-a-zA-Z0-9_]+)/$', {}, {'slug': <django.urls.converters.SlugConverter object at 0x000000000393D688>})

        v[0][0][1][0] 為判斷該 url 有沒有 pass 任何 args 
        所以 if k is verify and v[0][0][1][0]: 這一行在做的事情就是判斷 k 是不是我們特別定義出來給 verify email 使用的 view 同時判斷它是否有正確丟出 args

        addr = str(v[0][0][0]) 則會取出 '@%(slug)s/'
        addr[0: addr.index('%')] 則會拿第零個到%之間的字串

    '''
    
    link = ''
    for k, v in get_resolver(None).reverse_dict.items():
        if k is verify and v[0][0][1][0]:
            addr = str(v[0][0][0])
            link = domain + addr[0: addr.index('%')] + token

    '''
        render data into email template and form multi-type email
    '''

    msg = EmailMultiAlternatives(subject, from_email, [user.email])

    if signup_verification_email_text:
        try:
            text = render_to_string(signup_verification_email_text, {'link': link})
            msg.attach_alternative(text, "text/plain")
        except AttributeError:
            pass
    
    if signup_verification_email_html:
        try:
            html = render_to_string(signup_verification_email_html, {'link': link})
            msg.attach_alternative(html, "text/html")
        except AttributeError:
            pass 

    msg.send()
    
    


def GetFieldAndValidate(field, raise_error=True, default_type=str):
    try:
        d = getattr(settings, field)
        if d == "" or d is None or not isinstance(d, default_type):
            raise AttributeError
        return d
    except AttributeError:
        if raise_error:
            raise NotAllFieldCompiled(f"Field {field} missing or invalid")
        return None







class NotAllFieldCompiled(Exception):
    """Compile all the fields in the settings"""
    pass