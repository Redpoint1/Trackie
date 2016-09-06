from django.conf.urls import include, url

from . import views as trackie_views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$',
        view=trackie_views.HomePageView.as_view(),
        name=trackie_views.HomePageView.name
        ),
    url(r'^partials/(?P<partial>[\w/.]+)',
        view=trackie_views.PartialView.as_view(),
        name=trackie_views.PartialView.name,
        )
]
