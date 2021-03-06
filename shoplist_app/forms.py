# import form class from django 
from django import forms 

# import required models from models.py 
from .models import Item, Meal, StorageLoc, ShopDept

# create a ModelForm 
class ItemForm(forms.ModelForm): 
	# specify the name of model to use 
	class Meta: 
		model = Item 
		fields = "__all__"


class LocationForm(forms.ModelForm): 
	# specify the name of model to use 
	class Meta: 
		model = StorageLoc 
		fields = "__all__"


class DepartmentForm(forms.ModelForm):
	class Meta: 
		model = ShopDept 
		fields = "__all__"


class MealForm(forms.ModelForm):
	class Meta:
		model = Meal
		fields = ['name', 'short_name', 'serves', 'cook_time', 'total_time', 'ingredients', 'method']
		# temporarily removed ingredients & method from the form to simplify meal creation
		# fields = ['name', 'short_name', 'serves', 'cook_time', 'total_time']
		widgets = {
            'ingredients': forms.Textarea(attrs={'cols': 20, 'rows': 10}),
            'method': forms.Textarea(attrs={'cols': 20, 'rows': 10}),
        }


class FindItemForm(forms.Form):
	search_text = forms.CharField(label='Item to search for:', max_length=100)


class SelectItemForm(forms.Form):
	selection = forms.ChoiceField(widget=forms.RadioSelect, choices=())

'''
class MealSelectForm(forms.Form):
	meals = Meal.objects.all().order_by('name')
	print(meals)
	for meal in meals:
		print(meal)
	choices = []
	choices.append((0, "No meal selected"))
	for meal in meals:
		choices.append((meal.id, meal.name))
	selection = forms.ChoiceField(choices=choices, label='')
'''


class SelectMealCheckboxForm(forms.Form):
	selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=(), label='')



class SelectItemCheckboxForm(forms.Form):
	selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=(), label='')
	



