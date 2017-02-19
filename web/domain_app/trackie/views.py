from importlib import import_module
import django.views.generic as views
import django.template.loader as template_loader
import django.template.exceptions as template_exceptions
import django.http.response as http_response

from django.utils.translation import ugettext_lazy as _

import domain_app.trackie.forms as forms



class BasePageView(views.TemplateView):

    name = 'trackie.base'
    template_name = 'trackie/base.html'


class MainPageView(views.TemplateView):

    name = 'trackie.home'
    template_name = 'trackie/main/unregistered.html'
    form = None

    def get(self, request, *args, **kwargs):
        self.form = forms.RegisterForm()
        kwargs['form'] = self.form
        if request.user.is_authenticated():
            self.form = None
            self.template_name = 'trackie/main/registered.html'

        return super(MainPageView, self).get(request, *args, **kwargs)


class ProfilePageView(views.TemplateView):

    name = 'trackie.profile'
    template_name = 'partials/profile/profile.html'
    form = None

    def get(self, request, *args, **kwargs):
        self.form = forms.UserForm()
        kwargs['form'] = self.form

        return super(ProfilePageView, self).get(request, *args, **kwargs)


class PartialView(views.TemplateView):
    http_method_names = ('get',)

    name = 'trackie.partial'

    def get_context_data(self, **kwargs):
        module = import_module(".forms", "domain_app.trackie")
        partial = kwargs["partial"].split(".")[0].title().replace("/", "")
        class_name = "{}Form".format(partial)
        form = getattr(module, class_name, None)
        if form:
            kwargs["form"] = form()
        kwargs["default_fields"] = ["text", "file"]
        return super(PartialView, self).get_context_data(**kwargs)

    def get_template_names(self):

        partial_tpl_name = 'partials/%s' % self.kwargs['partial']

        try:
            template_loader.get_template(partial_tpl_name)
        except template_exceptions.TemplateDoesNotExist as e:
            # Prevent template rendering errors to return 404
            if e.args[0] == partial_tpl_name:
                raise http_response.Http404(_('partial not found'))
            else:
                raise

        return partial_tpl_name,
