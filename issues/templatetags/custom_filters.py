from django import template
from issues.models import Issue

from datetime import timedelta


register = template.Library()


def calculate_avg_max_min_duration(durations_list):
    max_duration_timedelta, min_duration_timedelta = max(durations_list), min(durations_list)
    sum_timedelta = sum(durations_list, timedelta())
    avg_duration_timedelta = sum_timedelta / len(durations_list)
    # clear microseconds
    max_duration = timedelta(days=max_duration_timedelta.days, seconds=max_duration_timedelta.seconds)
    min_duration = timedelta(days=min_duration_timedelta.days, seconds=min_duration_timedelta.seconds)
    avg_duration = timedelta(days=avg_duration_timedelta.days, seconds=avg_duration_timedelta.seconds)
    return (str(avg_duration).replace('days,', 'dnů a '), str(max_duration).replace('days,', 'dnů a '),
            str(min_duration).replace('days,', 'dnů a '))


# Show issues statistics in header if user is logged in and is superuser or staff
@register.filter
def issues_statistics(request):
    issues = Issue.objects.exclude(finished_at__isnull=True)
    durations_timedelta = [x.finished_at - x.created_at for x in issues]
    _avg, _max, _min = calculate_avg_max_min_duration(durations_timedelta)
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return f'Délka issues: průměrná {_avg} | max. {_max} | min. {_min}'
    else:
        return 'Django Admin'
