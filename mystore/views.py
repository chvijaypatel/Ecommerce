from importlib import invalidate_caches
from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render
from mystore.models import Banner1, Banner2, Categories, Coupon_Code, Main_Categories, Product,  Slider, Sub_Categories, Timer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.db.models import Max,Min,Sum
from django.contrib.auth.decorators import login_required
from cart.cart import Cart



# Create your views here.
def base(request):
    return render(request,'base.html')
     
def home(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners1 = Banner1.objects.all().order_by('-id')[0:3]
    banners2 = Banner2.objects.all().order_by('-id')[0:2]
    timers=Timer.objects.all()
    main_categories=Main_Categories.objects.all()
    categories=Categories.objects.all()
    sub_categories=Sub_Categories.objects.all()
    products=Product.objects.filter(section__name ='Top Deals Of The Day')
    
    context={
        'sliders':sliders,
        'banners1':banners1,
        'banners2':banners2,
        'timers':timers,
        'main_categories':main_categories,
        'categories':categories,
        'sub_categories':sub_categories,
        'products':products,

    }
    return render(request,'main/home.html',context)


def PRODUCT_DETAILS(request,slug):
    product = Product.objects.filter(slug = slug)   

    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')

    context = {
        'product':product,
    }
    return render(request,'product/product_deatil.html',context)

def Shop(request): 
    categories = Categories.objects.all()
    products=Product.objects.all()
    context={

        'products':products,
        'categories' : categories,
    }

    return render(request,'product/shop.html',context)

def error404(request):    
    return render(request,'errors/404.html')

def about(request):    
    return render(request,'pages/about.html')

def contact(request):    
    return render(request,'pages/contact.html')

def Blog(request):    
    return render(request,'pages/blog.html')

def Blog_Details(request):    
    return render(request,'pages/blog_details.html')

def Faq(request):    
    return render(request,'pages/faq.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is alredy Exit ! ")
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email is alredy Exit ! ")
            return redirect('login')

        user = User(
            username = username,
            email = email
        )
        user.set_password(password)
        user.save() 
        messages.success(request,'Successfully Registered ')
        return redirect('login')
        


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
             login(request, user)
            messages.success(request,'Successfully Login ')
            return redirect('home')
        else:
            messages.error(request,"Username and Password is invalid ! ")
            return redirect('login')
       
    return redirect('login')

@login_required(login_url='/accounts/login/')
def Profile(request):
    return render(request,'registration/profile.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/accounts/login/')
def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()


    t = render('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


@login_required(login_url='/accounts/login/')
def cart(request):    
      return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_charge = sum(i['packing_charge'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    
    coupon=None
    valid_coupon=None
    invalid_coupon=None
    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
           try:
               coupon = Coupon_Code.objects.get(code=coupon_code)
               valid_coupon =" It is applicable on current Oder"
           except:
               invalid_coupon ="Invalid Coupon!"
    context = {
        'packing_charge':packing_charge,
        'tax': tax,
        'coupon':coupon,
        'valid_coupon':valid_coupon,
        'invalid_coupon':invalid_coupon,
    }
    return render(request,'cart/cart.html',context)

def Checkout(request):    
    return render(request,'cart/checkout.html')

def Wishlist(request):    
    return render(request,'cart/wishlist.html')