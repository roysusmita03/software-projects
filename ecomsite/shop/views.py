from .models import Product, Order
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Validate that fields are not empty
        if not uname or not email or not pass1 or not pass2:
            return render(request, 'shop/signup.html', {'error': 'All fields are required.'})

        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'shop/signup.html', {'password_error': 'Passwords do not match.'})

        # Create the user
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('LoginPage')

    return render(request, 'shop/signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print(username, pass1)
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username and Password is Incorrect!")
    return render(request, 'shop/login.html')


def LogoutPage(request):
    logout(request)
    return redirect('LoginPage')


def index(request):
    product_objects = Product.objects.all()

    # search code
    # code file
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(category__icontains=item_name)

    # paginator code
    paginator = Paginator(product_objects, 8)
    page = request.GET.get("page")
    product_objects = paginator.get_page(page)

    return render(request, 'shop/index.html', {'product_objects': product_objects})


def detail(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


def about(request):
    return render(request, 'shop/about.html')


def training(request):
    return render(request, 'shop/training.html')


def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items', '')
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")
        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode,
                      total=total)
        order.save()

    return render(request, 'shop/checkout.html')


from django.shortcuts import redirect, get_object_or_404
from decimal import Decimal
from django.urls import reverse


def rate_product(request, id):
    product_object = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        # Get the rating from the form input
        rating_input = request.POST.get('rating')

        # Check if the rating input is not empty
        if rating_input:
            try:
                # Convert the input to a float
                rating = float(rating_input)

                # Convert the rating to Decimal
                decimal_rating = Decimal(rating)

                # Update product rating (average it with the existing rating)
                product_object.rating = (product_object.rating + decimal_rating) / Decimal('2')

                # Save the product object
                product_object.save()
            except ValueError:
                # In case of invalid input, just ignore and do nothing
                pass

        # Redirect back to the detail page
        return redirect(reverse('detail', args=[id]))

    # If the request is not POST, redirect to the detail page
    return redirect(reverse('detail', args=[id]))


