from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/issues/(?P<pk>[0-9]+)$',
        views.get_delete_update_issue,
        name='get_delete_update_issue'
    ),
    url(
        r'^api/v1/issues/$',
        views.get_post_issues,
        name='get_post_issues'
    )
]
