from django.contrib.auth.models import Permission
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


# Add or Remove 'Can view Issue' permission for user with/without staff role (if needed)
@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    permission = Permission.objects.get(codename='view_issue')
    if user.is_staff and (not user.has_perm(permission)):
        user.user_permissions.add(permission)
    if (not user.is_staff) and (not user.is_superuser) and (user.has_perm(permission)):
        user.user_permissions.remove(permission)
