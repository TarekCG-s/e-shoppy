from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):

    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f"{self.code} - {self.discount}"
