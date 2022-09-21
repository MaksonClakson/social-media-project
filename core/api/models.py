from django.db import models

class Customer(models.Model):
    name = models.CharField("Name2", max_length=240)
    email = models.EmailField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

