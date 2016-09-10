import django.views.generic as views
import django.template.loader as template_loader
import django.template.exceptions as template_exceptions
import django.http.response as http_response

from .forms import RegisterForm


class BasePageView(views.TemplateView):

    name = 'trackie.base'
    template_name = 'trackie/base.html'


class MainPageView(views.TemplateView):

    name = 'trackie.home'
    template_name = 'trackie/main/unregistered.html'
    form = None

    def get(self, request, *args, **kwargs):
        self.form = RegisterForm()
        kwargs['form'] = self.form
        if request.user.is_authenticated():
            self.template_name = 'trackie/main/registered.html'

        return super(MainPageView, self).get(request, *args, **kwargs)


class PartialView(views.TemplateView):
    http_method_names = ('get',)

    name = 'trackie.partial'

    def get_template_names(self):

        partial_tpl_name = 'partials/%s' % self.kwargs['partial']

        try:
            template_loader.get_template(partial_tpl_name)
        except template_exceptions.TemplateDoesNotExist as e:
            # Prevent template rendering errors to return 404
            if e.args[0] == partial_tpl_name:
                raise http_response.Http404('partial not found')
            else:
                raise

        return partial_tpl_name,
