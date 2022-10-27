from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=70)
    parent = models.ForeignKey('self',related_name="category", blank=True, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True,null=True)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.FloatField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name