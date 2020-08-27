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

