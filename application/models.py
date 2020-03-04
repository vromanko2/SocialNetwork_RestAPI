from django.db import models
# from django.contrib.auth.models import User
from users.models import User


# Create your models here.
TAG_STATUS = (
    (0, "Unlike"),
    (1, "Like")
)

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False)
    content = models.TextField()
    like = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
