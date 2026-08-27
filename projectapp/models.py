from django.db import models


# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Title: {self.name}, last edited: {self.last_edited.date()}'

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"