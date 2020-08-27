from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('list/new', views.list_new, name='list_new'),
	path('list/meals/add', views.list_meal_add, name='meal_items_add'),
	path('list/stock/add', views.list_stock_add, name='stock_items_add'),
    path('manage/items', views.item_list, name='item_list'),
    path('manage/items/add/<meal_id>', views.add_item, name='add_item'),
    path('manage/items/edit/<int:item_id>', views.edit_item, name='edit_item'),
    path('manage/items/find', views.find_item, name='find_item'),
    path('manage/locations', views.storage_list, name='storage_list'),
    path('manage/locations/edit/<int:location_id>', views.edit_location, name='edit_location'),
    path('manage/departments', views.department_list, name='department_list'),
    path('manage/departments/edit/<int:department_id>', views.edit_department, name='edit_department'),
    path('manage/meals', views.meal_list, name='meal_list'),
    path('manage/meals/add', views.add_meal, name='add_meal'),
    path('manage/meals/add_meal_item/<meal_id>', views.add_meal_item, name='add_meal_item'),
]