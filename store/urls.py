from django.urls import path

from . import views

urlpatterns = [
	
	path('', views.store, name="store"),
	path('search',views.search,name="search"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('product/<int:id>',views.product_detail,name="product_detail"),
	path('register/',views.register,name="register"),

]