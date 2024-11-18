from django.contrib import admin

from .models import Image, Reply, User, Question, Answer

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)
admin.site.register(Image)
