from django.conf.urls import url

from . import views as trackie_rest_v1_views

urlpatterns = [
    url(r'^test/$',
        view=trackie_rest_v1_views.TestEndpoint.as_view(),
        name=trackie_rest_v1_views.TestEndpoint.name,
        ),
]
