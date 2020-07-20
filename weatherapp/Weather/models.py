from django.db import models

class City(models.Model):
    is_private = models.BooleanField(default=False)
    city_name = models.CharField(max_length=100, default=" ")

    def __str__(self):
        return self.city_name

class Review(models.Model):
    rname = models.CharField(max_length=50)
    remail = models.CharField(max_length=100)
    rphone = models.IntegerField()
    rreview = models.CharField(max_length=1000)

    def __str__(self):
        return self.rname


class Contact(models.Model):
    cname = models.CharField(max_length=100)
    cemail = models.CharField(max_length=150)
    cphone = models.IntegerField()
    cquery = models.CharField(max_length=1500)

    def __str__(self):
        return self.cname


