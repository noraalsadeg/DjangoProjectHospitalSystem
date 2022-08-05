from django.db import models

# Create your models here.

class lists(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField()
    rating = models.FloatField()
    pub_date = models.DateField()

    def __str__(self) -> str:
        return self.title\

class store(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField()
    rating = models.FloatField()
    pub_date = models.DateField()

    def __str__(self) -> str:
        return self.title

class TD_Market(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField()
    rating = models.FloatField()
    pub_date = models.DateField()

    def __str__(self) -> str:
        return self.title
