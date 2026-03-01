from django.db import models

# Create your models here.

class Category(models.Model):

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Brand(models.Model):
    
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null= True)
    price = models.DecimalField(decimal_places=2, max_digits= 6)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['name','brand'], name = 'unique_name_brand')
        ]

