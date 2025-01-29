from django.db import models
from config.utils import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"