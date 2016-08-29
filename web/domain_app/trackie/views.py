import django.views.generic as views


class HomePageView(views.TemplateView):

    name = 'trackie.home'
    template_name = 'home.html'