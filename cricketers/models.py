from django.db import models
import uuid

class Cricketer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname=models.CharField(max_length=100)
    fname = models.CharField(max_length=100,blank=True,null=True)
    image=models.URLField()
    lname = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=50)
    position=models.CharField(max_length=100)
    odi_matches=models.IntegerField(blank=True,null=True)
    odi_runs = models.IntegerField(blank=True,null=True)
    odi_average=models.FloatField(blank=True,null=True)
    odi_strike_rate=models.FloatField(blank=True,null=True)
    odi_catches = models.IntegerField(blank=True,null=True)
    story=models.TextField(blank=True,null=True)
    url_source=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.fullname
