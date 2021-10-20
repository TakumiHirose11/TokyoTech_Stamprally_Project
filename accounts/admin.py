from django.contrib import admin

from .models import User,Profile,Answer,Unit,Question


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Unit)
admin.site.register(Answer)
admin.site.register(Question)

