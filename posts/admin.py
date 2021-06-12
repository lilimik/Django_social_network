from django.contrib import admin, messages
from django.utils.datetime_safe import datetime

from posts.models import Post, Comment, Like, Dislike


class CommentsInline(admin.TabularInline):
    model = Comment
    # readonly_fields = ('',)
    extra = 1


class LikeInline(admin.TabularInline):
    model = Like

    def has_add_permission(self, request, obj):
        return False


class DislikeInline(admin.TabularInline):
    model = Dislike

    def has_add_permission(self, request, obj):
        return True


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_date_of_creation', 'get_owner_email', 'text')
    list_display_links = ('id', 'get_date_of_creation', 'text')
    ordering = ('-date_of_creation',)
    search_fields = ('id', 'text',)
    list_filter = ('owner', 'date_of_creation')
    readonly_fields = ('text', 'get_date_of_creation')
    inlines = [CommentsInline, LikeInline]
    actions = ['update_date_of_creation']
    change_form_template = 'users/admin/posts_change.html'

    def get_queryset(self, request):
        qs = super(PostModelAdmin, self).get_queryset(request)
        return qs.select_related('owner')

    def get_owner_email(self, instance: Post):
        return instance.owner.email

    get_owner_email.short_description = 'email пользователя'
    get_owner_email.admin_order_field = 'owner__email'

    def update_date_of_creation(self, request, queryset):
        models = []
        for model in queryset:
            model.date_of_creation = datetime.now()
            models.append(model)
        Post.objects.bulk_update(models, ['date_of_creation'])
        self.message_user(request, 'Даты обновлены', messages.SUCCESS)

    update_date_of_creation.short_description = 'Обновить дату'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        is_custom_button_pressed = request.POST.get('custom_button', False)
        print('is_custom_button_pressed', is_custom_button_pressed)
        return super(PostModelAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def get_date_of_creation(self, instance: Post):
        return instance.date_of_creation.strftime('%d.%m.%Y в %H:%M:%S')

    get_date_of_creation.short_description = 'Дата создания'


admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment)
admin.site.register(Like)
