from django.db import models
from datetime import date

# Create your models here.
class Task(models.Model):
    """Model class for saving Tasks."""
    title = models.CharField(max_length=500, blank=False, null=False)
    date = models.DateField(default=date.today)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} due on {self.date}."
