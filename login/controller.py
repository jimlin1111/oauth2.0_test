from django.conf import settings as st
import requests
import urllib.parse
from login.models import SystemNotify,SystemSendDetail
import arrow

class LineLoginClass:
    def __init__(self, action, request, *args, **kwargs):
        if action == 'auth':
            self.base_url = st.LINE_BASEURL_DICT['get_authorize']
            self.client_id = st.CHANNEL_ABOUT['channel_id']
            self.scope = urllib.parse.quote('openid email profile', safe='')
            self.redirect_uri = urllib.parse.quote(f'{st.BASE_URL}/auth/callback', safe='')
            self.state = kwargs['state']
        elif action == 'get_at':
            self.code = request.GET.get('code')
            self.client_id = st.CHANNEL_ABOUT['channel_id']
            self.secret = st.CHANNEL_ABOUT['channel_secret']
            self.base_url = st.LINE_BASEURL_DICT['get_access_token']

            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.payload = {
                'grant_type': 'authorization_code',
                'code': self.code,
                'redirect_uri': f'{st.BASE_URL}/auth/callback',
                'client_id': self.client_id,
                'client_secret': self.secret,
            }
        elif action == 'get_profile':
            print(kwargs)
            self.verify_url = st.LINE_BASEURL_DICT['profile_verify']
            self.verify_payload = {
                'id_token': kwargs['id_token'],
                'client_id': kwargs['client_id']
            }
    
    def return_login_info(self):
        ret = {'success':True, 'msg':''}
        ret['result'] = f'{self.base_url}?response_type=code&client_id={self.client_id}&state={self.state}&scope={self.scope}&redirect_uri={self.redirect_uri}'

        return ret
    
    def return_access_token(self):
        r = requests.post(self.base_url, headers=self.headers, data=self.payload)
        token_data = r.json()
        self.token_data = token_data
        return token_data, self.client_id
    
    def return_profile(self):
        verify_r = requests.post(self.verify_url, data=self.verify_payload)
        user_profile = verify_r.json()
        self.user_profile = user_profile
        return user_profile

class NotifySubScribe:
    def __init__(self, action, request, *argv, **kwargs):
        if action == 'subscribe':
            self.base_url = st.LINE_BASEURL_DICT['notify_authorize']
            self.redirect_uri = urllib.parse.quote(f'{st.BASE_URL}/auth/notify/callback', safe='')
            self.client_id = st.CHANNEL_ABOUT['notify_id']
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        elif action == 'cancel':
            user_id = request.user.id
            self.notify_obj = SystemNotify.objects.get(user_id=user_id)
        
            self.base_url = st.LINE_BASEURL_DICT['notify_cancel']
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {self.notify_obj.access_token}'
            }
        elif action == 'auth':
            self.code = request.GET.get('code')
            self.state = request.GET.get('state')
            self.base_url = st.LINE_BASEURL_DICT['notify_get_token']
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.payload = {
                'grant_type': 'authorization_code',
                'code': self.code,
                'redirect_uri': f'{st.BASE_URL}/auth/notify/callback',
                'client_id': st.CHANNEL_ABOUT['notify_id'],
                'client_secret': st.CHANNEL_ABOUT['notify_secret'],
            }
        elif action == 'hello':
            self.access_token = kwargs['access_token']
            self.send_url = st.LINE_BASEURL_DICT['notify_send_message']
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {kwargs["access_token"]}'
            }
            self.send_payload = {
                'message': '哈囉，歡迎使用我的網站訂閱Line Notify \U0001F604'
            }
    
    def return_notify_info(self):
        ret = {'success':True, 'msg':''}
        print(self.redirect_uri)
        ret['result'] = f"{self.base_url}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=notify&state=123123"
        return ret
    
    def return_notify_auth(self):
        r = requests.post(self.base_url, headers=self.headers, data=self.payload)
        ret = r.json()
        self.ret = ret
        return ret
    
    def return_notify_cancel(self):
        r = requests.post(self.base_url, headers=self.headers)
        if r.status_code == 200:
            success = True
            msg = '取消訂閱成功'
        else:
            success = False
            msg = '取消失敗，請聯絡作者'
        self.notify_obj.status = 0
        self.notify_obj.save()
        return {'success':success, 'msg':msg}
    
    def send_welcome(self):
        r = requests.post(self.send_url, headers=self.headers, data=self.send_payload)
        user_id = SystemNotify.objects.get(access_token=self.access_token).user_id
        write_dict = {
            'user_id':user_id,
            'who_send':'system',
            'message': '哈囉，歡迎使用我的網站訂閱Line Notify \U0001F604',
            'send_time': arrow.utcnow().to('Asia/Taipei').shift(hours=8).format('YYYY-MM-DDTHH:mm:ss')
        }
        ret = r.json()
        if ret['status'] == 200:
            write_dict['success'] = 1
        else:
            write_dict['success'] = 0
            write_dict['error_msg'] = ret["message"]
        SystemSendDetail.objects.create(**write_dict)