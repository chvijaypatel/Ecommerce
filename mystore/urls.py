from django.urls import path,include
from . import views

urlpatterns = [  
     
     path('404/', views.error404, name='404'),
     path('', views.home, name='home'),
     path('base/', views.base, name='base'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('faq/', views.Faq, name='faq'),
     path('blog/', views.Blog, name='blog'),
     path('blog_details/', views.Blog_Details, name='blog_details'),
     path('product/filter-data',views.filter_data,name="filter-data"),
     path('product/<slug:slug>',views.PRODUCT_DETAILS,name='product_deatil'),
     path('shop/', views.Shop, name='shop'),
     path('accounts/register', views.register, name='handleregister'),
     path('accounts/login', views.user_login, name='handlelogin'),
     path('accounts/logout', views.logout_view, name='logout'),
     path('accounts/profile', views.Profile, name='profile'),
     path('accounts/profile_update', views.Profile_Update, name='profile_update'),
     path('accounts/', include('django.contrib.auth.urls')),
     path('cart/', views.cart, name='cart'), 
     path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
     path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
     path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
     path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
     path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
     path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
     path('cart/checkout/',views.Checkout,name='checkout'),
     path('cart/wishlist/',views.Wishlist,name='wishlist'),


    

] 