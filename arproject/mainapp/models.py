from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Image(models.Model):
    title = models.CharField(max_length=100)
    height = models.IntegerField(validators=[MinValueValidator(1)])
    width = models.IntegerField(validators=[MinValueValidator(1)])
    thumbnail = models.ImageField(null=False, blank=False)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title