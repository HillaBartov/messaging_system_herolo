from django.http import HttpResponse
from django.contrib.auth.models import User
from .serializers import UserSerializer, MessageSerializer
from .models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, authentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class TokenAuthentication(authentication.TokenAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'

def home(request):
    return HttpResponse("Hello abra!")

def creat_messages_list(queryset):
    messagesSerializerList = []
    for message in queryset:
        messagesSerializerList.append(MessageSerializer(message).data)

    # messagesSerializerList.reverse() 
    content = {
        'status': 1, 
        'responseCode' : status.HTTP_200_OK, 
        'data': messagesSerializerList,
    }
    return content

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, authentication.BasicAuthentication) 
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [IsAdminUser]}

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class MessageViewSet(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication, authentication.BasicAuthentication) 
    #create new message
    def post(self, request):
        if request.user.is_authenticated:
            message_dict = {'sender': request.user.id, 'receiver': request.data['receiver'], 'message': request.data['message'],'subject':request.data['subject']}
            serializer = MessageSerializer(data=message_dict)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get specific message by id
    def get(self, request, id=None):
        if request.user.is_authenticated:
            
            if id:
                # Find the requested message for current user, or 404 if current user did not receive this message
                queryset = Message.objects.filter(receiver = request.user.id)
                message = get_object_or_404(queryset, id=id)
                message.read = True
                message.save()
                serializer = MessageSerializer(message)
                return Response({"status": "read successfully", "massage": serializer.data}, status=status.HTTP_200_OK)

    
    # Delete specific message by id
    def delete(self, request, id=None):
        if request.user.is_authenticated:
            # Find the requested message for current user, or 404 if current user did not receive this message
            queryset = Message.objects.filter(receiver = request.user.id)
            message = get_object_or_404(queryset, id=id)
            message.delete()
            return Response({"status": "deleted successfully", "data": "message deleted"})


class GetUserMessagesViewSet(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication, authentication.BasicAuthentication) 
    
    def get(self, request, unread="read"):
        
        if request.user.is_authenticated:
            # Find the inbox for current user
            queryset = Message.objects.filter(receiver = request.user.id)
            # When unread messages requsted filter inbox
            if unread == "unread":
                queryset = queryset.filter(read = False)
                if queryset is None:
                    return Response({"Queryset is empty": "No unread massages"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(creat_messages_list(queryset))
            
            if queryset is None:
                return Response({"Queryset is empty": "No massages"}, status=status.HTTP_400_BAD_REQUEST) 
            # Get all inbox
            return Response(creat_messages_list(queryset))