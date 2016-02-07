from django.conf.urls import include, url

urlpatterns = [
    url(r'^v1/', include('app.api.rest.v1.urls')),
]