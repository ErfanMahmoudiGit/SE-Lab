from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Article, category as categ, Order, OrderItem
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic.list import ListView

class ArticleList(ListView):
    template_name = "blog/home.html"
    queryset = Article.objects.filter(status="p").order_by('-publish')
    paginate_by = 4

def detail(request, slug):
    context = {
        "article" : get_object_or_404 (Article, slug=slug, status = "p"),
    }
    return render (request, "blog/detail.html", context)

def about (request):
    context = {
        # - means decending
        "articles" : Article.objects.filter(status="p").order_by('-publish'),
    }
    return render (request, "blog/about.html", context)

def contact (request):
    context = {
        # - means decending
        "articles" : Article.objects.filter(status="p").order_by('-publish'),
    }
    return render (request, "blog/contact.html", context)

def category(request, slug, page=1):
    category = get_object_or_404 (categ, slug=slug, status = True)
    articles_list = category.articles.published()
    paginator = Paginator(articles_list, 4)  # Show 25 contacts per page.
    articles = paginator.get_page(page)


    context = {
        # - means decending
        "category" : category,
        "articles" : articles,
    }
    return render (request, "blog/category.html", context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/') # Redirect to a view named 'home' after signup
    else:
        form = UserCreationForm()
    return render(request, "blog/signup.html", {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Article, Order, OrderItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Article, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, order_date=None)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    print(f"Product {product_id} added to cart. Redirecting to shopping cart. Order ID: {order.id}, Order Created: {created}, Order Items: {order.items.all()}")
    return redirect('blog:shopping_cart')

@login_required
def shopping_cart(request):
    order = Order.objects.filter(user=request.user, order_date=None).first()
    if order:
        print(f"Shopping cart for user {request.user.username}: {order.items.all()}")
    else:
        print(f"No active order found for user {request.user.username}.")
    return render(request, 'blog/shopping-cart.html', {'order': order})


@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, order_date__isnull=True).first()
    if order:
        order.order_date = timezone.now()
        order.save()
    return redirect('blog/order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, order_date__isnull=False)
    return render(request, 'blog/order_history.html', {'orders': orders})
