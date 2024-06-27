from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_imgs/')
    email = models.EmailField('email address', unique=True) # changes email to unique and blank to false
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    def __str__(self) -> str:
        if super().first_name != "" and super().last_name != "":
            return super().first_name + " " + super().last_name
        else:
            return super().username

languages = [
    ('go', 'Go'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('c', 'C'),
    ('rust', 'Rust'),
    ('php', 'Php'),
    ('ruby', 'Ruby'),
    ('js', 'Javascript'),
    ('ts', 'Typescript'),
]

class Snippet(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=200)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(choices=languages, max_length=100, default="plaintext")

    def __str__(self):
        return self.title
    