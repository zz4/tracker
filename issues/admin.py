from django.contrib import admin
from django.contrib.auth.models import Group
from .models import State, Issue, Category


class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'responsible_person', 'description', 'state', 'category', 'created_at',
                    'finished_at',)
    exclude = ('duration',)

    # fill creator and responsible_person fields as a current user
    def get_changeform_initial_data(self, request):
        get_data = super(IssueAdmin, self).get_changeform_initial_data(request)
        get_data['creator'] = request.user.pk
        get_data['responsible_person'] = request.user.pk
        return get_data


admin.site.register(State)
admin.site.register(Category)
admin.site.register(Issue, IssueAdmin)
admin.site.unregister(Group)
admin.site.site_title = 'Simple Tracker'
admin.site.index_title = 'Tracker Administration'
admin.site.site_url = '/admin'
