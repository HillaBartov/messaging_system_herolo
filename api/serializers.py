from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'first_name', 'last_name']

    # Overide create method - in order to create Token
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #create token
        Token.objects.create(user=user)
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id','sender', 'receiver', 'message','subject','creation_date','read')
