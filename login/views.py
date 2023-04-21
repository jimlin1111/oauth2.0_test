from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from login.models import (
    SystemUserLoginInfo,
    LoginRequired,
    SystemNotify,
    SystemCity,
    SystemCityRefer,
    SystemSendDetail,
)
from django.contrib import auth
from login.controller import LineLoginClass, NotifySubScribe
import arrow

# Create your views here.
class RedirectView(View):
    def get(self, request):
        return redirect('auth:login')
class LoginView(View):
    def get(self, request):
        auth.logout(request)
        return render(request, 'auth/login.html')
    def post(self, request):
        action = request.POST.get('action')
        response = LineLoginClass(action, request).return_login_info()
        return JsonResponse(response)
        
class LineLoginCallbackView(View):
    def get(self, request):
        # 取得access_token相關資訊
        action = 'get_at'
        token_data, client_id = LineLoginClass(action, request).return_access_token()
        now = arrow.utcnow().to('Asia/Taipei').shift(seconds=token_data['expires_in']).format('YYYY-MM-DD HH:mm:ss')

        # 用id_token取得身份
        action_next = 'get_profile'
        user_profile = LineLoginClass(action_next, request, **token_data, **{'client_id':client_id}).return_profile()

        # 找是否曾經授權登入過
        try:
            SystemUserLoginInfo.objects.get(line_user_id=user_profile['sub'])
            action = 'login'
            # 若有則登入
        except:
            action='register'
            # 沒有是註冊
        # 不一定每個人都會授權email
        try:
            email = user_profile['email']
        except:
            email = ''
        
        user_data = {
            'username': user_profile['name'],
            'password': '',
            'email': email,
            'is_superuser': 0,
            'is_staff': 0,
            'is_active':1
        }
        if action == 'register':
            user = User.objects.create(**user_data)
            extend_info = {
                'user_id': user.id,
                'access_token': token_data['access_token'],
                'token_type': token_data['token_type'],
                'refresh_token': token_data['refresh_token'],
                'at_expired': now,
                'scope': token_data['scope'],
                'id_token': token_data['id_token'],
                'user_pic': user_profile['picture'],
                'id_token_expired': arrow.get(user_profile['exp']).to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss'),
                'line_user_id': user_profile['sub'],
                'status': 1,
                'create_datetime': arrow.get(user_profile['iat']).to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss')
            }
            SystemUserLoginInfo.objects.create(**extend_info)
            auth.login(request, user)
        elif action == 'login':
            extend_info_obj = SystemUserLoginInfo.objects.filter(line_user_id=user_profile['sub'])
            user = User.objects.get(id=extend_info_obj[0].user_id)
            user.username = user_profile['name']
            user.email = email
            user.save()
            extend_info = {
                'user_id': user.id,
                'access_token': token_data['access_token'],
                'token_type': token_data['token_type'],
                'refresh_token': token_data['refresh_token'],
                'at_expired': now,
                'scope': token_data['scope'],
                'id_token': token_data['id_token'],
                'user_pic': user_profile['picture'],
                'id_token_expired': arrow.get(user_profile['exp']).to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss'),
                'line_user_id': user_profile['sub'],
                'status': 1,
                'create_datetime': arrow.get(user_profile['iat']).to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss')
            }
            extend_info_obj.update(**extend_info)
            auth.login(request, user)
        return render(request, 'auth/callback.html',{'success':True,'msg':'您已成功登入'})
    
class IndexView(LoginRequired, View):
    def get(self, request):
        user_id = request.user.id
        # 找是否有訂閱notify
        try:
            notify_obj = SystemNotify.objects.get(user_id=user_id,status=1)
            if notify_obj.status == 1:
                subscribe = True
            else:
                subscribe = False
        except:
            subscribe = False

        citys = [{'sn':i.sn, 'name':i.name} for i in SystemCity.objects.all()]
        citys_refer = [i.city_sn for i in SystemCityRefer.objects.filter(user_id=user_id)]

        return render(request, 'index/index.html',{'subscribe':subscribe, 'citys':citys, 'citys_refer':citys_refer})
    
    def post(self, request):
        action = request.POST.get('action')
        if action == 'subscribe':
            response = NotifySubScribe(action, request).return_notify_info()

            return JsonResponse(response)
        elif action == 'cancel':
            response = NotifySubScribe(action, request).return_notify_cancel()
            return JsonResponse(response)
    
class NotifyOauthView(LoginRequired, View):
    def get(self, request):
        ret = NotifySubScribe('auth', request).return_notify_auth()

        user_id = request.user.id
        try:
            notify_obj = SystemNotify.objects.get(user_id=user_id)
            notify_obj.access_token = ret['access_token']
            notify_obj.status = 1
            notify_obj.save()
        except:
            create_data = {
                'user_id':user_id,
                'access_token':ret['access_token'],
                'status':1,
                'create_datetime': arrow.utcnow().to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss')
            }
            SystemNotify.objects.create(**create_data)
        
        NotifySubScribe('hello', request, **ret).send_welcome()
        return render(request, 'auth/callback.html',{'success':True,'msg':'您已成功訂閱notify'})
    
class CitySubScribe(View):
    def post(self, request):
        user_id = request.user.id
        now = arrow.utcnow().to('Asia/Taipei').format('YYYY-MM-DD HH:mm:ss')
        response = {'success':True, 'msg':'訂閱成功'}

        citys = [int(i) for i in request.POST.getlist('city_list[]', [])]
        if len(citys) == 0:
            response['success'] = False
            response['msg'] = '沒有選擇的城市'
        else:
            for city in citys:
                create_dict = {
                    'city_sn':city,
                    'user_id':user_id,
                    'create_datetime':now
                }
                SystemCityRefer.objects.create(**create_dict)
        return JsonResponse(response)
    
    def delete(self, request):
        user_id = request.user.id
        SystemCityRefer.objects.filter(user_id=user_id).delete()
        return JsonResponse({'success':True, 'msg':'取消訂閱成功'})
