from django.views.generic import TemplateView

class RootRouteView(TemplateView):
    template_name = 'index.html'
