from django.contrib import admin
from .models import Message
# Register your models here.
class MessageInline(admin.StackedInline):
    model = Message
    can_delete = False
    verbose_name_plural = 'Messages'

admin.site.register(Message)