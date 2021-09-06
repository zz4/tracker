from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/issues/(?P<pk>[0-9]+)/$',
        views.get_delete_update_issue,
        name='get_delete_update_issue'
    ),
    url(
        r'^api/v1/issues/$',
        views.get_post_issues,
        name='get_post_issues'
    ),
    url(
        r'^api/v1/users/$',
        views.get_all_users,
        name='get_all_users'
    ),
    url(
        r'^api/v1/states/$',
        views.get_all_states,
        name='get_all_states'
    ),
    url(
        r'^api/v1/categories/$',
        views.get_all_categories,
        name='get_all_categories'
    )
]
