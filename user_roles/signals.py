from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserRole, UserLog,Role

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='login')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='logout')
    
@receiver(post_save, sender=UserRole)
def log_role_change(sender, instance, created, **kwargs):
    if not created:  # Check if it's an update (not a new creation)
        user = instance.user

        #previous role as inactive
        previous_role = instance.role
        UserRole.objects.filter(user=user, role=previous_role).update(active=False)

        # Create a new UserRole instance with the updated role
        new_role = instance.role
        UserRole.objects.create(user=user, role=new_role, active=True)

        # Log the role change
        UserLog.objects.create(user=user, action='role_updated', role=f'{previous_role.name} to {new_role.name}')





