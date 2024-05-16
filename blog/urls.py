from django.urls import include, path
from blog.views import ArticleList, detail, about, contact, category, shoppingcard, signup, shopping_cart, checkout, order_history, add_to_cart

app_name = "blog"
urlpatterns = [
    path ("", ArticleList.as_view(), name = "home"),
    path ("page/<int:page>", ArticleList.as_view(), name = "home"),
    path ("article/<slug:slug>", detail, name = "detail"),
    path ("about", about, name = "about"),
    path ("contact", contact, name = "contact"),
    path ("shoppingcard", shoppingcard, name = "shoppingcard"),
    path ("category/<slug:slug>", category, name = "category"),
    path ("category/<slug:slug>/page/<int:page>", category, name = "category"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("signup/", signup, name="signup"),
    path('cart/', shopping_cart, name='shopping_cart'),
    path('cart/checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('product/<int:product_id>/add/', add_to_cart, name='add_to_cart'),
]
