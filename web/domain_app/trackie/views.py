import django.views.generic as views

from .forms import RegisterForm


class HomePageView(views.TemplateView):

    name = 'trackie.home'
    template_name = 'trackie/unregistered/home.html'
    form = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.template_name = 'trackie/registered/home.html'
        else:
            self.form = RegisterForm()
            kwargs['form'] = self.form

        return super(HomePageView, self).get(request, *args, **kwargs)
