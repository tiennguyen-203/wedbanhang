from django.shortcuts import render,redirect
from app.models import Order, OrderItem, Product,Categories,Filter_Price,Color,Brand,Tag,Contact_us
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.filter(status ='Publish')

    context = {
        'product':product,
    }
    return render(request, 'Main/index.html',context)

def PRODUCT(request):

    product = Product.objects.filter(status ='Publish')
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()


    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    print(PRICE_FILTER_ID)
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')
    
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    PRICE_LOWTOHIGHTID  = request.GET.get('PRICE_LOWTOHIGHT')
    PRICE_HIGHTTOLOWID = request.GET.get('PRICE_HIGHTTOLOW')

    PRODUCT_NEWID = request.GET.get('PRODUCT_NEW')
    PRODUCT_OLDID = request.GET.get('PRODUCT_OLD')

    if CATID:
        product = Product.objects.filter(categories = CATID,status = 'Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID,status = 'Publish')
    elif COLORID:
        product = Product.objects.filter(color = COLORID,status = 'Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID,status = 'Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHTID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif PRODUCT_NEWID:
        product = Product.objects.filter(status='Publish',condition = 'New').order_by('-id')
    elif PRODUCT_OLDID:
        product = Product.objects.filter(status='Publish',condition = 'Old').order_by('-id')
    
        
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')


    context = {
        'product':product,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand,
    }
    return render(request, 'Main/product.html',context)

def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product
    }
    return render(request, 'Main/search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()

    context = {
        'prod':prod
    }
    return render(request, 'Main/product_singer.html',context)

def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name = name,
            email = email,
            subject = subject,
            message = message,

        )
        contact.save()
        return redirect('home')
    

    return render(request, 'Main/contact.html')




def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('login')
 
    return render(request, 'Registartion/auth.html')

def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'Registartion/auth.html')

def HandleLogout(request):
    logout(request)

    return redirect('home')





@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    return render(request, 'Cart/checkout.html')

def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        
        
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount =amount,

        )
        order.save()
        for i in cart:

            a = (int(cart[i]['price']))
            b = cart[i]['quantity']

            total = a * b

            
            item = OrderItem(
                order = order,
                
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = a * b,
                product_id = cart[i]['product_id'],
                
            )
            item.save()

        
    return render(request, 'Cart/placeorder.html')


def success(request):
    return render(request, 'Cart/thank_you.html')

def about(request):
    return render(request, 'Main/about.html')

def blog(request):
    return render(request, 'Main/blog.html')
def blog_singer(request):
    return render(request, 'Main/blog_singer.html')
def blog_singer2(request):
    return render(request, 'Main/blog_singer2.html')