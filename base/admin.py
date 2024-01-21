from django.contrib import admin


from .models import User, Article, Message, Topic

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Message)
