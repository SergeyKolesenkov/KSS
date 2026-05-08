from django.contrib import admin


from .models import Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    fields = ('user', 'avatar')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ('avatar',)

