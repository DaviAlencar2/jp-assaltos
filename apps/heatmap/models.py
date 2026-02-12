from django.db import models
from django.contrib.auth.models import User


def defautl_user():
    user = User.objects.filter(username='davil').first()
    if user:
        return user.pk
    return None


class Neighborhood(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Robbery(models.Model):
    TYPES = [("a","assalto"),
             ("f","furto")
    ]

    neighborhood = models.ForeignKey(
        Neighborhood, on_delete=models.CASCADE, related_name="robberies",default="")
    
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=False)
    number = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=False)
    longitude = models.CharField(max_length=255, blank=True, null=False)
    type = models.CharField(max_length=1,blank=False, null=False, choices=TYPES, default="a")
    is_valid = models.BooleanField(default=False)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="robberies", default=defautl_user)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Assalto em: {self.neighborhood.name}, as: {self.date} - {self.time}"