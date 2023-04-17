from django.contrib import auth

def return_username(request):
    try:
        username = auth.get_user(request).username
    except:
        return {'username':''}
    else:
        return {'username':username}
