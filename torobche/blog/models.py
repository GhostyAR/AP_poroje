from django.db import models

class product(models.Model):
    name = models.CharField(max_length=200)
    ulp = models.JSONField(blank=True,null=True)
    attr = models.JSONField(blank=True,null=True)
    

    def __str__(self):
        return self.name

