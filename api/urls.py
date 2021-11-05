from django.contrib import admin
from django.urls import path
from rest_framework import routers
from api import views
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('users', views.UserViewSet) 
# router.register('messages', views.MessageViewSet)
# router.register('get-all-messages', views.GetMessageViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-tokn-auth'),
    path('new-message/', views.MessageViewSet.as_view()),
    path('message/<int:id>', views.MessageViewSet.as_view()),
    path('inbox/', views.GetUserMessagesViewSet.as_view()),
    path('inbox/<str:unread>', views.GetUserMessagesViewSet.as_view()),
    # path('accounts/', include('django.contrib.auth.urls')),  
    
]