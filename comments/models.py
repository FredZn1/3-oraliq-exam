from django.db import models
from config.utils import BaseModel
from posts.models import Post


class Comment(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=False)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)

    def __str__(self):
        return f"{self.name}"