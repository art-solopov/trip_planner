from django.http import HttpRequest
from django.shortcuts import render


def home(request: HttpRequest):
    return render(request, 'home.html')


class WithMainClassMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_class'] = getattr(self, 'main_class', '')
        return context
