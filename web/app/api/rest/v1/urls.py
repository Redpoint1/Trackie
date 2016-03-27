""" Rest api urls v1 """

from django.conf.urls import include, url

from . import views as rest_v1_views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$',
        view=rest_v1_views.ApiRoot.as_view(),
        name=rest_v1_views.ApiRoot.name)
]

urlpatterns += (
    url(r'^trackie/', include('domain_app.trackie.rest.v1.urls')),
)

# partials_view = restV1_views.PartialView.as_view()
# if not settings.DEBUG:
# partials_view = cache_page(60*60)(partials_view)

# urlpatterns.append(
#     url(r'^partials/(?P<partial>[\w/.]+)'   ,
#            view = partials_view                ,
#         name = restV1_views.PartialView.name,
#     )
# )
