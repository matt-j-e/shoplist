from django.conf import settings
from django.db import models
from django.utils import timezone


class StorageLoc(models.Model):
	''' A location in your home where food items are stored '''
	name = models.CharField(max_length=200)
	sort_order = models.SmallIntegerField()

	def __str__(self):
		''' Return a string representation of the model '''
		return self.name	


class ShopDept(models.Model):
	''' A department in the shop where you would look for a specific item '''
	name = models.CharField(max_length=200)
	sort_order = models.SmallIntegerField()

	def __str__(self):
		''' Return a string representation of the model '''
		return self.name


class Item(models.Model):
	''' An item on a shopping list'''
	name = models.CharField(max_length=200)
	storage_loc = models.ForeignKey(StorageLoc, on_delete=models.CASCADE)
	shop_dept = models.ForeignKey(ShopDept, on_delete=models.CASCADE)
	favourite = models.BooleanField(default=True)

	def __str__(self):
		''' Return a string representation of the model '''
		return self.name


class Meal(models.Model):
	''' A meal, including preparation method and items that need to be 
	bought before it can be made '''
	name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=20)
	serves = models.SmallIntegerField()
	cook_time = models.SmallIntegerField("Cooking Time (mins)")
	total_time = models.SmallIntegerField("Total Time (mins)")
	ingredients = models.TextField()
	method = models.TextField()
	items = models.ManyToManyField(Item)

	def __str__(self):
		''' Return a string representation of the model '''
		return self.name	