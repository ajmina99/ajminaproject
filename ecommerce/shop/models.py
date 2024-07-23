from django.db import models


class Category(models.Model):
    objects = None
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    desc = models.TextField()

    def __str__(self):
        return self.title

class Product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='media/products', blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True) #one time
    updated=models.DateTimeField(auto_now=True)  #change every time we update record
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name