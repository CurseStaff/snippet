from django.db import models
from django.contrib.auth.models import User


class Snippet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=100, default="plaintext")

    def __str__(self):
        return self.title
