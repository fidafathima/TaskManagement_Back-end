from rest_framework import serializers

from TaskApp.models import Tasks, UserDetails


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tasks
        fields="__all__"


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model=UserDetails
        fields=('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        user = UserDetails.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user