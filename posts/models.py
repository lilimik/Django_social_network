from django.db.models import Manager, Count, F, OuterRef, Subquery

from media.models import Media
from users.models import CustomUser, Follows
from django.db import models


class CommonModel(models.Model):
    date_of_creation = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='дата создания')

    class Meta:
        abstract = True


class PostManager(Manager):
    def annotate_likes_comments(self):
        liked = Like.objects.filter(main_post__id=OuterRef('pk')).select_related('owner')
        commented = Comment.objects.filter(main_post__id=OuterRef('pk')).select_related('owner')
        return self.annotate(
            # liked=Subquery(liked),
            likes_count=Count('likes'),
            dislikes_count=Count('dislike'),
            # commented=Subquery(commented),
            comments_count=Count('comments'),
        )


class Post(CommonModel):
    objects = PostManager()
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='пользователь', related_name='posts',
                              null=False, blank=False)
    published = models.BooleanField(verbose_name='статус публикации поста', null=False, blank=False)
    text = models.TextField(max_length=1000, blank=True, verbose_name='текст')
    main_post = models.ForeignKey("self", on_delete=models.PROTECT, verbose_name='основной пост', related_name='twits',
                                  null=True, blank=True)

    def __str__(self):
        return f'[{self.date_of_creation.strftime("%d.%m.%y")}] - {self.text[:50]}...'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Comment(CommonModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Комментатор',
                              related_name="comments", null=False, blank=False)
    main_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост',
                                  related_name="comments", null=True, blank=True)
    main_media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name='медиа',
                                   related_name="comments", null=True, blank=True)
    main_comment = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name='коммент',
                                     related_name='comments', null=True, blank=True)
    text = models.CharField(max_length=300, blank=False, verbose_name='текст')

    def __str__(self):
        return f'[{self.date_of_creation.strftime("%d.%m.%y %H.%i")}] | {self.text[:10]} {self.owner.email}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Like(CommonModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Лайкнувший',
                              related_name="likes", null=False, blank=False)
    main_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост',
                                  related_name="likes", null=True, blank=True)
    main_media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name='медиа',
                                   related_name="likes", null=True, blank=True)
    main_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='комментарий', related_name='likes')

    def __str__(self):
        value = ''
        if self.main_post is not None:
            value = f'{self.main_post.text[:10]}'
        elif self.main_comment is not None:
            value = f'{self.main_comment.text[:10]}'
        elif self.main_media is not None:
            value = f'{self.main_media.short_link}'
        return f'[{self.date_of_creation.strftime("%d.%m.%y %H:%i")}] | {value}... - {self.owner.email}'

    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'


class Dislike(CommonModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Дизайкнувший',
                              related_name="dislikes", null=False, blank=False)
    posts = models.ManyToManyField(Post, verbose_name='пост')

    def __str__(self):
        return f'[{self.date_of_creation.strftime("%d.%m.%y %H:%i")}] | владелец {self.owner.email}'

    class Meta:
        verbose_name = 'дизлайк'
        verbose_name_plural = 'дизлайки'
