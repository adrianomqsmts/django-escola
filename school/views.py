from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    