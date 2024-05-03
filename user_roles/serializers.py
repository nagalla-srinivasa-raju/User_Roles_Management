from rest_framework import serializers
from .models import User, Role, UserLog

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_active', 'roles']

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        password = validated_data.pop('password')  
        user = User.objects.create(**validated_data)
        user.set_password(password) 
        user.save()
        for role_id in roles_data:
            user.roles.add(role_id)
        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', [])
        password = validated_data.pop('password', None) 
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        
        if password is not None:
            instance.set_password(password) 
            
        instance.save()
        instance.roles.clear()
        for role_id in roles_data:
            instance.roles.add(role_id)
        return instance
    
class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = ['id', 'user', 'action', 'role', 'timestamp']
























# class UserSerializer(serializers.ModelSerializer):
#     roles = RoleSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'is_active', 'roles']
        
# class UserSerializer(serializers.ModelSerializer):
#     roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'is_active', 'roles']

#     def create(self, validated_data):
#         roles_data = validated_data.pop('roles', [])
#         user = User.objects.create(**validated_data)
#         for role_id in roles_data:
#             # role = Role.objects.get(pk=role_id)
#             user.roles.add(role_id)
#         return user

#     def update(self, instance, validated_data):
#         roles_data = validated_data.pop('roles', [])
#         instance.email = validated_data.get('email', instance.email)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         instance.roles.clear()
#         for role_id in roles_data:
#             # role = Role.objects.get(pk=role_id)
#             instance.roles.add(role_id)
#         return instance
