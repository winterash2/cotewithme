from django.contrib import admin
from .models import *
# Register your models here.
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'count_text']
#     list_display_links = ['title']

#     def count_text(self, obj):
#         return '{} 글자'.format(len(obj.text))
#     count_text.short_description = 'text 글자 수' #column 이름을 바꿔줌


# Register your models here.
# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment)

admin.site.register(Post)
admin.site.register(Team)
admin.site.register(JoinedTeam)
admin.site.register(Code)