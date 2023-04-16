from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')