from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
from .models import Item, StorageLoc, ShopDept, Meal
from .forms import ItemForm, MealForm, LocationForm, DepartmentForm, FindItemForm, SelectItemForm, SelectMealCheckboxForm, SelectItemCheckboxForm
import shoplist_app.helpers as helpers

meal_choices = []
# a global varaible to enable meal_choices to be passed between view methods
# list_meal_add and list_stock_add

initial_list = []
# a global variable to hold all shopping list items. Compiled from: 1) meal_choices
# and 2) the list of favourite items. This forms the basis of the final list creation functionality.

final_list = []
# a global variable to hold the final list of selected items

def list_new(request):
	''' Main menu page for creating a new shopping list. Simply two links:
	Add meals to a new list & Add stock items to your list. '''
	return render(request, 'shoplist_app/list_new.html')


def list_meal_add(request):
	''' A page where the user can choose which meals they will eat over coming 
	days so that the required shopping items can be added to the list as step 1 '''
	meals = Meal.objects.all().order_by('name')
	choices = []
	for meal in meals:
		choices.append((meal.id, meal.name.capitalize()))
	form = SelectMealCheckboxForm()
	form.fields["selection"].choices = choices
	if request.method != 'POST':
		return render(request, 'shoplist_app/list_meal_add.html', {'form': form})
	else:
		# print(request.POST) # request.POST is a QueryDict. The key we want is 'selection' which contains a list of meal ids
		selected_indexes = request.POST.getlist('selection')
		form = SelectMealCheckboxForm(data=request.POST)
		if form.is_valid:
			global meal_choices
			meal_choices = selected_indexes
			return redirect('stock_items_add')
		# meal_choices is a list of integers that represent the
		# meal_ids of chosen meals
			
			
def list_stock_add(request):
	''' A page that lists all of the shopping items marked as favourite, in storage
	location order TOGETHER WITH the meal shopping items added in the list_meal_add
	process (also in the appropriate storage area) '''
	items_for_meals = helpers.create_meals_shopping_list(meal_choices)
	# for item in items_for_meals:
		# print(item.id, item.name, item.storage_loc.id, item.need_for)
	locations = StorageLoc.objects.all().order_by('sort_order')
	# select all storage areas in sort order
	faves = Item.objects.filter(favourite=True).order_by('name')
	# select all items marked fave in storage_id order
	global initial_list
	initial_list = helpers.create_initial_list(items_for_meals, faves, locations)
	# initial_list_by_storage = helpers.sort_initial_list(initial_list, locations)
	# print(initial_list)
	form = SelectItemCheckboxForm()
	form.fields["selection"].choices = helpers.create_list_choices(initial_list)
	context = {
		'initial_list': initial_list,
		'locations': locations,
		'form': form
		}
	if request.method != 'POST':
		return render(request, 'shoplist_app/list_stock_add.html', context)
	else:
		form = SelectItemCheckboxForm(data=request.POST)
		if form.is_valid:
			selected_indexes = request.POST.getlist('selection')
			global final_list
			final_list = []
			for i in range(len(initial_list)):
				if str(i) in selected_indexes:
					final_list.append(initial_list[i])
			return redirect('show_final_list')


def show_final_list(request):
	all_depts = ShopDept.objects.all().order_by('sort_order')
	used_depts = helpers.get_used_depts(final_list)
	context = {
		'all_depts': all_depts,
		'used_depts': used_depts,
		'final_list': final_list
	}
	return render(request, 'shoplist_app/show_final_list.html', context)


def item_list(request):
	''' A simple view that lists all of the items held in the database. 
	Displayed fields are: 'item name', 'storage_loc', 'shop_dept', and 'favourite' (true or false) '''
	items = Item.objects.all().order_by('name')
	# for item in items:
		# item.name = item.name.title()
		# item.storage_loc = item.storage_loc.upper()
	return render(request, 'shoplist_app/item_list.html', {'items': items})


def add_item(request, meal_id=None):
	''' Add a new item to the master list '''
	if request.method != 'POST':
		# no data submitted so render a blank form
		form = ItemForm()
	else:
		# process the POST data
		form = ItemForm(data=request.POST)
		if form.is_valid:
			form.save()
			if meal_id:
				all_items = Item.objects.all().order_by("id")
				latest_item = all_items.reverse()[:1][0]
				meal = Meal.objects.get(id=meal_id)
				meal.items.add(latest_item)
				return redirect('find_item') 
			return redirect('item_list')

	# display blank or invalid form
	context = {'form': form, 'meal_id': meal_id}
	return render(request, 'shoplist_app/add_item.html', context)


def edit_item(request, item_id):
	''' Edit an item entry '''
	item = Item.objects.get(id=item_id)
	if request.method != 'POST':
		# no data amemded yet so render form with existing entries
		form = ItemForm(instance=item)
	else:
		# POST data submitted, containing edited data
		form = ItemForm(instance=item, data=request.POST)
		if form.is_valid:
			form.save()
			return redirect('item_list')

	# display blank or invalid form
	context = {'item': item, 'form': form}
	return render(request, 'shoplist_app/edit_item.html', context)


def find_item(request):
	''' Search through the Item db table for any Item whose name
	contains the string passed in via the form. Present a single-choice list of
	items to choose that match the search string. Or give the option to add
	a completely new item. '''
	meals = Meal.objects.all().order_by("id")
	meal = meals.reverse()[:1][0]
	# meal_id = meal.id
	meal.shoppinglist = meal.items.all()
	if request.method != 'POST':
		# no form data submitted - must be "first" visit. Render blsnk form
		form = FindItemForm()
	else:
		# search string must have been passed in so process it.
		form = FindItemForm(data=request.POST)
		if form.is_valid:
			# if the form processes...
			poss_matches = Item.objects.filter(name__contains=request.POST['search_text'])
			# pull items from the database whose name contains the search string
			if len(poss_matches) > 0:
				# if at least one possible match...
				select_form = SelectItemForm()
				# initialize a select form (which has single-choice radio buttons)
				CUSTOM_CHOICES = []
				# initialise custom choices array
				for m in poss_matches:
					# add poss matches to custom choice array
					choice = (m.id, m.name)
					CUSTOM_CHOICES.append(choice)
				select_form.fields["selection"].choices = CUSTOM_CHOICES
				return render(request, 'shoplist_app/display_matches.html', {"form": select_form, "meal": meal})
			else:
				select_form = ItemForm()
				return render(request, 'shoplist_app/no_matches.html', {"form": select_form, "meal": meal})
			
	return render(request, 'shoplist_app/find_item.html', {"form": form, "meal": meal})


def index(request):
	return render(request, 'shoplist_app/index.html')


def storage_list(request):
	locations = StorageLoc.objects.all().order_by('sort_order')
	return render(request, 'shoplist_app/storage_list.html', {'locations': locations})


def edit_location(request, location_id):
	''' Edit the details of a storage location '''
	location = StorageLoc.objects.get(id=location_id)
	all_locations = StorageLoc.objects.all().order_by('sort_order')
	items = Item.objects.filter(storage_loc=location_id).order_by('name')
	if request.method != 'POST':
		# no data amemded yet so render form with existing entries
		form = LocationForm(instance=location)
	else:
		# POST data submitted, containing edited data
		form = LocationForm(instance=location, data=request.POST)
		if form.is_valid:
			form.save()
			return redirect('storage_list')

	# display blank or invalid form
	context = {'location': location, 'all_locations': all_locations, 'items': items, 'form': form}
	return render(request, 'shoplist_app/edit_location.html', context)


def department_list(request):
	departments = ShopDept.objects.all().order_by('sort_order')
	return render(request, 'shoplist_app/department_list.html', {'departments': departments})


def edit_department(request, department_id):
	''' Edit the details of a shop department '''
	department = ShopDept.objects.get(id=department_id)
	all_departments = ShopDept.objects.all().order_by('sort_order')
	items = Item.objects.filter(shop_dept=department_id).order_by('name')
	if request.method != 'POST':
		# no data amemded yet so render form with existing entries
		form = DepartmentForm(instance=department)
	else:
		# POST data submitted, containing edited data
		form = DepartmentForm(instance=department, data=request.POST)
		if form.is_valid:
			form.save()
			return redirect('department_list')

	# display blank or invalid form
	context = {'department': department, 'all_departments': all_departments, 'items': items, 'form': form}
	return render(request, 'shoplist_app/edit_department.html', context)



def meal_list(request):
	meals = Meal.objects.all().order_by('name')
	for meal in meals:
		# meal.name = meal.name.title()
		meal.shoppinglist = meal.items.all()
	return render(request, 'shoplist_app/meal_list.html', {'meals': meals})


def add_meal(request):
	''' Add a new meal '''
	if request.method != 'POST':
		# no data submitted so render a blank form
		form = MealForm()
	else:
		# process the POST data
		form = MealForm(data=request.POST)
		if form.is_valid:
			form.save()
			return redirect('find_item') # possibly needs to change to redirect('find_item', meal_id="meal_id")

	# display blank or invalid form
	context = {'form': form}
	return render(request, 'shoplist_app/add_meal.html', context)


def add_meal_item(request, meal_id):
	''' add shopping items to a meal that is already in the db '''
	meal = Meal.objects.get(id=meal_id)
	item = Item.objects.get(id=request.POST["selection"])
	meal.items.add(item)
	return redirect('find_item')






