from django.db import models

class GliderMeasurement(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    salinity = models.FloatField(null=True, blank=True)
    oxygen = models.FloatField(null=True, blank=True)
    cdom = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} | Depth: {self.depth}m"