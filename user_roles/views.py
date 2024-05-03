from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
# from django.db.models import Q
from rest_framework.decorators import action
from django.core.mail import send_mail
# from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active_param = self.request.query_params.get('is_active', None)

        if is_active_param is not None:
            is_active_value = is_active_param.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_value)

        return queryset 
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print(f"Deleting user: {instance.email}")
    #     instance.soft_delete()  # Soft delete user
    #     print(f"User {instance.email} deleted successfully")
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'])
    def delete_inactive_users(self, request):
        inactive_users = User.objects.filter(is_active=False)
        if inactive_users.exists():
            inactive_users.delete()  # Delete all inactive users
            return Response({"detail": "All inactive users deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "No inactive users found"}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            subject = 'Account Registration'
            message = f'Hello {user.email},\n\nYour account has been created successfully.\nEmail: {user.email}\nPassword: {request.data.get("password")}\n\nThank you!'
            from_email = "mailtrap@demomailtrap.com"
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            role = serializer.save()
            return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            role = serializer.save()
            return Response(RoleSerializer(role).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
