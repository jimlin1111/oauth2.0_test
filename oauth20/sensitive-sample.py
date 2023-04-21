DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # enter your database name
        'USER':'', # enter your user name
        'PASSWORD':'', # enter your user password
        'HOST':'', # enter your database host
        'PORT':'3306',
        'OPTIONS':{
            'charset':'utf8mb4',
        }
    }
}

CHANNEL_ABOUT = {
    'channel_id': '', # enter your line login channel id
    'channel_secret': '', # enter your line login channel secret
    'notify_id': '', # enter your line notify channel id
    'notify_secret': '' # enter your line notify channel secret
}

BASE_URL = '' # enter your domain like https://example.com.tw