from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()

    class MPTTMeta:
        order_insertion_by = ['parent']

    def __str__(self):
        return f'Комментарий {self.name} на {self.post}'

    def save(self, *args, **kwargs):
        if self.parent is None:
            pass
        elif self.post.id not in [i for i in Comment.objects.filter(pk=self.parent.id).values_list('post')][0]:
            raise ValidationError("invalid post")
        super().save(*args, **kwargs)


