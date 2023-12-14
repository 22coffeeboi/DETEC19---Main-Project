from django.contrib import admin
from.models import Users,Predict

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username','pass1')


admin.site.register(Users, UsersAdmin)

class PredictAdmin(admin.ModelAdmin):
    list_display = ('result', 'img', 'accuracy')

admin.site.register(Predict,PredictAdmin)