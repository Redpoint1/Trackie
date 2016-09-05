import django.views.generic as views

from .forms import RegisterForm


class HomePageView(views.TemplateView):

    name = 'trackie.home'
    template_name = 'trackie/home.html'
    form = None

    def get(self, request, *args, **kwargs):
        self.form = RegisterForm()
        kwargs['form'] = self.form

        return super(HomePageView, self).get(request, *args, **kwargs)
