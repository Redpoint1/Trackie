from django.conf.urls import include, patterns, url

import domain_app.trackie.rest.v1.views as trackie_restV1_views

urlpatterns = patterns('',
     url(r'^test/$',
         view=trackie_restV1_views.TestEndpoint.as_view(),
         name=trackie_restV1_views.TestEndpoint.name     ,
     ),
)