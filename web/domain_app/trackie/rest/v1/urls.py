from django.conf.urls import url

import domain_app.trackie.rest.v1.views as trackie_restV1_views

urlpatterns = [
     url(r'^test/$',
         view=trackie_restV1_views.TestEndpoint.as_view(),
         name=trackie_restV1_views.TestEndpoint.name     ,
     ),
]