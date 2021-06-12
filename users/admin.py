from django.contrib import admin

from users.models import CustomUser, Follows


class CustomUserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'birthday'
    # fields = ('id', 'password', 'email', 'birthday', 'patronymic')
    pass


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follows)
