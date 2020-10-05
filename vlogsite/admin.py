from django.contrib import admin
from .models import *
# Register your models here.
class VlogTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']
    search_fields = ('type_name__type_name',)

class VlogTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog_type', 'author', 'create_time', 'last_updated_time']
    search_fields = ('title', 'blog_type', 'author', 'create_time', 'last_updated_time')

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comt', "belond", "user", "date", "parent"]
    search_fields = ('comt', "belond", "user", "date", "parent")

class SignAdmin(admin.ModelAdmin):
    list_display = ["user", "time", "Is_sign"]
    search_fields = ("user", "time", "Is_sign")

admin.site.register(VlogType, VlogTypeAdmin)
admin.site.register(vlogText, VlogTextAdmin)
admin.site.register(comment, CommentAdmin)
admin.site.register(geton, SignAdmin)