from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Avg
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Products, Cart, HistoryImage, Order, Artisan, ArtisanRating

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Sum
from .models import Artisan, ArtisanRating


@login_required
def rate_artisan(request):
    if request.method == 'POST':
        artisan_id = request.POST.get('artisan_id')
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        try:
            artisan = Artisan.objects.get(id=artisan_id)
            rating, created = ArtisanRating.objects.update_or_create(
                user=request.user,
                artisan=artisan,
                defaults={
                    'rating': rating_value,
                    'comment': comment
                }
            )
            return JsonResponse({'success': True})
        except Artisan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Artisan not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def artisan_detail(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)

    # Calculate average rating
    ratings = ArtisanRating.objects.filter(artisan=artisan)
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0

    # Get user's rating if exists
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ArtisanRating.objects.filter(
            user=request.user,
            artisan=artisan
        ).first()

    # Handle rating submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if rating_value:
            rating, created = ArtisanRating.objects.update_or_create(
                user=request.user,
                artisan=artisan,
                defaults={
                    'rating': rating_value,
                    'comment': comment
                }
            )
            return redirect('artisan_detail', artisan_id=artisan.id)

    # Get other artisans with their average ratings
    other_artisans = Artisan.objects.exclude(id=artisan.id).annotate(
        avg_rating=Avg('artisanrating__rating')
    ).order_by('-avg_rating')[:4]  # Get top 4 artisans

    context = {
        'artisan': artisan,
        'avg_rating': avg_rating,
        'all_ratings': ratings,
        'user_rating': user_rating,
        'other_artisans': other_artisans,
    }
    return render(request, 'shop/artisan_detail.html', context)


# ... keep your other views ...


# ... keep all your other existing views ...
# ===================== Authentication Views =====================
def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if not uname or not email or not pass1 or not pass2:
            return render(request, 'shop/signup.html', {'error': 'All fields are required.'})

        if pass1 != pass2:
            return render(request, 'shop/signup.html', {'password_error': 'Passwords do not match.'})

        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('LoginPage')

    return render(request, 'shop/signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username and Password is Incorrect!")
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('SignUpPage')


# ===================== Product Views =====================
def index(request):
    product_objects = Products.objects.all()
    item_name = request.GET.get('item_name')

    if item_name:
        product_objects = product_objects.filter(title__icontains=item_name)

    return render(request, 'shop/index.html', {'product_objects': product_objects})


def productdetail(request, id):
    product_object = get_object_or_404(Products, id=id)
    return render(request, 'shop/product detail.html',
                  {'product_object': product_object,
                   })


# ===================== History Views =====================
def historyofhandicrafts(request):
    return render(request, 'shop/history.html')


def history(request):
    images = HistoryImage.objects.all()
    context = {'images': images}
    return render(request, 'shop/history.html', context)


# ===================== Cart Views =====================
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'success': True, 'quantity': cart_item.quantity})
    return JsonResponse({'success': False})


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        cart_item = get_object_or_404(Cart, user=request.user, product=product)

        if cart_item.quantity > 0:
            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                cart_item.delete()
            else:
                cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity if cart_item.quantity > 0 else 0})
        return JsonResponse({'success': False, 'message': 'Item not in cart'})
    return JsonResponse({'success': False})


@login_required
def cart_count(request):
    try:
        count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'count': count})
    except Exception as e:
        print(f"Error in cart_count view: {e}")
        return JsonResponse({'count': 0})


@login_required
def cart(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = cart_items.aggregate(total=Sum('product__price'))['total'] or 0
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'shop/cart.html', context)
    except Exception as e:
        print(f"Error in cart view: {e}")
        return render(request, 'shop/cart.html', {'cart_items': [], 'total_price': 0})


@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            payment_method=request.POST.get('payment_method')
        )
        cart_items.delete()
        return redirect('order_confirmation')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/payment.html', context)


@login_required
def order_confirmation(request):
    return render(request, 'shop/order_confirmation.html')


def index(request):
    product_objects = Products.objects.all()
    item_name = request.GET.get('item_name')

    if item_name:
        product_objects = product_objects.filter(title__icontains=item_name)

    # Add pagination - 8 items per page
    paginator = Paginator(product_objects, 8)
    page_number = request.GET.get('page')
    product_objects = paginator.get_page(page_number)

    return render(request, 'shop/index.html', {'product_objects': product_objects})


def aboutus(request):
    return render(request, 'shop/aboutus.html')
