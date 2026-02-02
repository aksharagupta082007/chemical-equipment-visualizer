from django.db import models

class Dataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)

    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    equipment_type_distribution = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"
