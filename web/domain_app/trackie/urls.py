from django.conf.urls import include, url

from . import views as trackie_views

urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^main.html$',
        view=trackie_views.MainPageView.as_view(),
        name=trackie_views.MainPageView.name
    ),
    url(
        r'^partials/(?P<partial>[\w/.]+)',
        view=trackie_views.PartialView.as_view(),
        name=trackie_views.PartialView.name,
    ),
    url(
        r'^.*$',
        view=trackie_views.BasePageView.as_view(),
        name=trackie_views.BasePageView.name
    ),
]
