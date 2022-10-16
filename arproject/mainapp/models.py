from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()
    thumbnail = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title