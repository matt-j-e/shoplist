from .models import Item, StorageLoc, ShopDept, Meal


def extract_meal_choices(data):
	''' takes in a request.POST object from a form submission, extracts the relevant data
	and returns it as a simple list '''
	collected_data = [
		int(data['form-0-selection']),
		int(data['form-1-selection']),
		int(data['form-2-selection']),
		int(data['form-3-selection']),
		int(data['form-4-selection']),
		int(data['form-5-selection']),
		int(data['form-6-selection'])
	]
	return collected_data


def create_meals_shopping_list(meal_choices):
	''' takes in the meal_choices array which contains 7 integers representing the meals
	that have been chosen for the coming days. Then constructs a shopping list of all of
	the items needed to cook those meals. The returned variable 'meals_shoppimh_list'
	is a list of query set results relating to every item needed. The same item may be 
	repeated where needed in more than 1 meal. The variable also includes the short meal
	name for which each item is required '''
	meals_shopping_list = []
	for meal_id in meal_choices:
		if meal_id == 0:
			continue
		meal = Meal.objects.get(id=meal_id)
		items = meal.items.all()
		for item in items:
			item.need_for = meal.short_name
			meals_shopping_list.append(item)
	return meals_shopping_list


def create_initial_list(meal_items, fave_items, locations):
	''' takes in the meals shopping list and the favourites list and constructs a list of 
	dictionaries in storage location order. Each dictionary contains: 
	item.id
	item.name
	item.storage_loc.id
	item.shop_dept.id and 
	item.need_for '''
	initial_l = []
	for location in locations:
		for meal_item in meal_items:
			if meal_item.storage_loc != location:
				continue
			item_dict = {
				'id': meal_item.id,
				'name': meal_item.name,
				'storage_loc_id': meal_item.storage_loc.id,
				'shop_dept_id': meal_item.shop_dept.id,
				'need_for': meal_item.need_for
			}
			initial_l.append(item_dict)

		for fave_item in fave_items:
			if fave_item.storage_loc != location:
				continue
			item_dict = {
				'id': fave_item.id,
				'name': fave_item.name,
				'storage_loc_id': fave_item.storage_loc.id,
				'shop_dept_id': fave_item.shop_dept.id,
				'need_for': ""
			}
			initial_l.append(item_dict)
	return initial_l


def create_list_choices(init_list):
	''' takes in the initial list of dictionaries (in storage location order), extracts list 
	index and name and constructs a 'choices' variable to pass to a multiple choice field form '''
	choices = []
	for i in range(len(init_list)):
		description = init_list[i]['name']
		if init_list[i]['need_for'] != "":
			description += f" [{init_list[i]['need_for']}]"
		choice = (i, description)
		choices.append(choice)
	return choices
