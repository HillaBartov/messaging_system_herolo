from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254, blank=True)

# Message model, parent model is Conversation
class Message(models.Model):
    # conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner')
    receiver= models.ForeignKey(User, on_delete=models.CASCADE,related_name='target')
    message = models.CharField(max_length=100)
    subject = models.CharField(max_length=100,blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    
    read = models.BooleanField(default=False,blank=True)

    