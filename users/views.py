from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView 
from django.contrib import messages #import messages
from django.contrib.messages.views import SuccessMessageMixin

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')
    success_message = f'Bem-vindo'
    
class LogoutView(View):
    # Responde apenas requisições GET
    def get(self, request, *args, **kwargs):
        messages.success(request, "Tchau, até!" )
        logout(request)
        return redirect('index')    