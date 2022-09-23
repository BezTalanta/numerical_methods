from django.views.generic.base import TemplateView


class StartView(TemplateView):
    template_name = 'base.html'
