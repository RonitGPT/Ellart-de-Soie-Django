from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import string
import random
from Ellart_de_soie.models import PasswordResetOTP
import math

# Home View
def Home(request):
    return render(request, '1Home_Page.html')

# Product List View with Filtering, Sorting, and Searching
def product_list(request):
    products = Product.objects.filter(is_active=True)  # Fetch only active products

    # Get query parameters
    brand = request.GET.get('brand')
    sort_by = request.GET.get('sort')
    search_query = request.GET.get('search')

    # Filter by brand
    if brand:
        products = products.filter(brand__icontains=brand)

    # Search functionality
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(p_details__icontains=search_query)
        )

    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'availability':
        products = products.order_by('-is_active')

    return render(request, 'product_list.html', {'products': products})

# # Register Page
# def Register_Page(request):
#     if request.method == 'POST':
#         Username = request.POST.get('Username')
#         Email = request.POST.get('Email')
#         Password = request.POST.get('Password')
#         Confirm_Password = request.POST.get('Confirm_Password')

#         Message = {}
#         if Username == '' or Email == '' or Password == '' or Confirm_Password == '':
#             Message["invalid"] = "Fields must not be empty"
#             return render(request, 'Register_Page.html', Message)
#         elif Password != Confirm_Password:
#             Message["invalid"] = "Oops! Password does not match."
#             return render(request, 'Register_Page.html', Message)
#         else:
#             if User.objects.filter(username=Username).exists():
#                 Message["invalid"] = "Username already exists"
#                 return render(request, 'Register_Page.html', Message)
#             elif User.objects.filter(email=Email).exists():
#                 Message["invalid"] = "Email already exists"
#                 return render(request, 'Register_Page.html', Message)
#             else:
#                 # Create a new user
#                 user = User.objects.create_user(username=Username, email=Email, password=Password)
#                 user.save()

#                 # Optionally save additional profile details
#                 Profile.objects.create(user=user)

#                 Message["success"] = "User created successfully!"
#                 return render(request, 'Register_Page.html', Message)
#     else:
#         return render(request, 'Register_Page.html')

# Register Page
# def Register_Page(request):
#     if request.method == 'POST':
#         Username = request.POST.get('Username')
#         Email = request.POST.get('Email')
#         Phone = request.POST.get('Phone')
#         Password = request.POST.get('Password')
#         Confirm_Password = request.POST.get('Confirm_Password')

#         Message = {}
#         if Username == '' or Email == '' or Password == '' or Confirm_Password == '':
#             Message["invalid"] = "Fields must not be empty"
#             return render(request, 'Register_Page.html', Message)
#         elif Password != Confirm_Password:
#             Message["invalid"] = "Oops! Password does not match."
#             return render(request, 'Register_Page.html', Message)
#         else:
#             try:
#                 user = Profile.objects.create(
#                     Username=Username, Email=Email, Phone=Phone,
#                     Password=Password, Confirm_Password=Confirm_Password
#                 )
#                 user.set_password(Confirm_Password)
#                 user.save()
#                 Message["success"] = "User created successfully!"
#                 return render(request, 'Register_Page.html', Message)
#             except:
#                 Message["invalid"] = "Username already exists"
#                 return render(request, 'Register_Page.html', Message)
#     else:
#         return render(request, 'Register_Page.html')

# Login Page
# from django.contrib.auth import login, authenticate

# def Login_page(request):
#     if request.method == 'POST':
#         Username = request.POST.get("Username")
#         Password = request.POST.get("Password")
#         context = {}
#         if Username == "" or Password == "":
#             context['error_msg'] = "Fields cannot be empty."
#         else:
#             user = authenticate(username=Username, password=Password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 context["error_msg"] = "Invalid username or password."
#         return render(request, 'Login_page.html', context)
#     else:
#         return render(request, 'Login_page.html')

# # Login Page
# def Login_page(request):
#     if request.method == 'POST':
#         Username = request.POST.get("Username")
#         Password = request.POST.get("Password")
#         context = {}
#         if Username == "" or Password == "":
#             context['error_msg'] = "Fields cannot be empty."
#         else:
#             user = authenticate(username=Username, password=Password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 context["error_msg"] = "Invalid username or password."
#                 return render(request, 'Login_page.html', context)
#     else:
#         return render(request, 'Login_page.html')

# Logout User
def user_logout(request):
    logout(request)
    return redirect('home')

# Product Details
def Product_Details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})

# Cart Page
@login_required
def Cart_Page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'ViewCart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to Cart
@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')

# Other Views
def Aboutus(request):
    return render(request, 'About_us.html')

def Baby_Store(request):
    products = Product.objects.filter(category=1, is_active=True)  # Filter by Baby category
    return render(request, 'Baby_Store.html', {'products': products})

def Hair_Shop(request):
    products = Product.objects.filter(category=2, is_active=True)  # Filter by Hair category
    return render(request, 'Hair_Shop.html', {'products': products})

def Perfumes(request):
    products = Product.objects.filter(category=3, is_active=True)  # Filter by Perfumes category
    return render(request, 'Perfumes.html', {'products': products})

def Men_Store(request):
    products = Product.objects.filter(category=4, is_active=True)  # Filter by Men's category
    return render(request, 'Men_Store.html', {'products': products})

def Skin(request):
    products = Product.objects.filter(category=5, is_active=True)  # Filter by Skin Care category
    return render(request, 'Skin_Care.html', {'products': products})

def Women_Store(request):
    products = Product.objects.filter(category=6, is_active=True)  # Filter by Women's category
    return render(request, 'Women_Store.html', {'products': products})

def sort(request, sv):
    if sv == '0':
        col = 'price'  # Sort by price ascending
    else:
        col = '-price'  # Sort by price descending
    products = Product.objects.filter(category=3).order_by(col)
    return render(request, 'Perfumes.html', {'products': products})

from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()  # Remove the item from the cart
    messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
    return redirect('cart')  # Redirect back to the cart page

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Quantity of {cart_item.product.name} has been increased.")
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if cart_item.quantity > 1:  # Prevent going below 1
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.name} has been decreased.")
    else:
        messages.warning(request, "Quantity cannot be less than 1.")
    
    return redirect('cart')


@login_required
def Cart_Page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        discount = 0

        # Example: Simple promo code logic
        if promo_code == "SAVE10":
            discount = total_price * 0.10
        elif promo_code == "Ronit20":
            discount = total_price * 0.20

        total_price = total_price - discount

        return render(request, 'ViewCart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'discount': discount,
            'promo_code': promo_code,
        })

    return render(request, 'ViewCart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount': 0,
        'promo_code': '',
    })


import razorpay
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, Product

@login_required
def checkout(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch cart items for the user
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    # Razorpay client initialization
    client = razorpay.Client(auth=("rzp_test_0T4v1YEHRFiayq", "0sAyviL23bSRqG5xdd5Av63y"))

    # Create order on Razorpay
    order_data = {
        "amount": total_amount * 100,  # Amount in paise
        "currency": "INR",
        "payment_capture": 1  # 1 means payment is captured automatically
    }

    payment_order = client.order.create(data=order_data)

    context = {
        'order_id': payment_order['id'],
        'order_amount': payment_order['amount'],
        'razorpay_key': 'rzp_test_0T4v1YEHRFiayq',  # Your Razorpay API Key
    }

    return render(request, 'checkout.html', context)

# import razorpay
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Order, Cart
# import json

# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.body.decode('utf-8')
#         payment_data = json.loads(data)

#         razorpay_order_id = payment_data['order_id']
#         razorpay_payment_id = payment_data['payment_id']
#         razorpay_signature = payment_data['signature']

#         client = razorpay.Client(auth=("rzp_test_0T4v1YEHRFiayq", "0sAyviL23bSRqG5xdd5Av63y"))

#         # Verify payment signature
#         data = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         }
#         try:
#             client.payment.fetch_payment(razorpay_payment_id)
#             client.utility.verify_payment_signature(data)  # This will throw an error if signature is invalid
#             # Create Order in your database and mark it as successful
#             order = Order.objects.get(order_id=razorpay_order_id)
#             order.status = 'paid'
#             order.payment_id = razorpay_payment_id
#             order.save()
#             return JsonResponse({'success': True})
#         except razorpay.errors.SignatureVerificationError:
#             return JsonResponse({'success': False, 'message': 'Payment verification failed.'})


import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Razorpay Client Initialization
client = razorpay.Client(auth=("rzp_test_0T4v1YEHRFiayq", "0sAyviL23bSRqG5xdd5Av63y"))

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            # Get the amount from the frontend (optional customization)
            data = json.loads(request.body)
            amount = data.get("amount", 50000)  # Default ₹500 in paisa

            # Create an order on Razorpay
            order = client.order.create({
                "amount": amount,  # Amount in paisa (₹1 = 100 paisa)
                "currency": "INR",
                "payment_capture": 1  # Auto capture
            })

            # Return the order details to the frontend
            return JsonResponse(order)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


import razorpay
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

from django.shortcuts import render

@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_signature = data.get("razorpay_signature")

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            result = client.utility.verify_payment_signature(params_dict)

            if result:
                # Render the order success page
                return render(request, 'order_success.html', {
                    "payment_id": razorpay_payment_id,
                    "order_id": razorpay_order_id,
                })
            else:
                return JsonResponse({"success": False, "message": "Invalid payment signature"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=400)


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order

def place_order(request):
    if request.method == 'POST':
        # Assume that the order has been successfully created
        order = Order.objects.create(
            user=request.user,
            product_id=request.POST.get('product_id'),
            quantity=request.POST.get('quantity'),
            total_amount=5000  # Example total amount
        )

        # Send email after placing the order
        subject = f"Order Confirmation: {order.order_id}"
        message = f"Dear {request.user.username},\n\nThank you for placing an order with us. Your order ID is {order.order_id}.\n\nTotal Amount: ₹{order.total_amount / 100}.\n\nThank you for shopping with us!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]

        # Send email
        send_mail(subject, message, from_email, recipient_list)

        # Redirect to success page with order ID
        return redirect('order_success', order_id=order.order_id)

    return render(request, 'place_order.html')  # Return to the order page if there's an error

def order_success(request, order_id):
    # Render the success page with the order_id
    return render(request, 'order_success.html', {'order_id': order_id})


def register(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        ucpass=request.POST["ucpass"]
        context={}
        if uname=="" or upass=="" or ucpass=="":
             context['errmsg']="Field can not be empty" 
             return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="password and confirm password not match"
            return render(request,'register.html',context)   
        else:
          try:
            u=User.objects.create(password=upass,username=uname,email=uname)
            u.set_password(upass)
            u.save()
            context['sucess']="User created sucessfully...."
            return render(request,'register.html',context)
          except Exception:
            context['errmsg']="User name already exists"
            return render(request,'register.html',context)    
    else:

        return render(request,'register.html')
    

def user_login(request):
     if request.method=='POST':
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        context={}
        if uname=="" or upass=="" :
             context['errmsg']="Field can not be empty" 
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)     
                return redirect('/')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)    
     else :
        return render(request,'login.html')    
     
def user_logout(request):
    logout(request)             
    return redirect('/login')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No account found with that email.")
            return render(request, "forgot_password.html")

        for user in users:
            # Generate an OTP
            otp = ''.join(random.choices(string.digits, k=6))
            PasswordResetOTP.objects.update_or_create(user=user, defaults={"otp": otp}) 

    # Send the OTP via email
            send_mail(
                "Password Reset OTP",
                f"Hello {user.username},\n\nYour OTP for resetting the password is: {otp}.\n\nUse this to reset your password.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        messages.success(request, "An OTP has been sent to your email.")
        return redirect('enter_otp')  # Redirect to the OTP entry page
    return render(request,"forgot_password.html") 

def enter_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        try:
            reset_entry = PasswordResetOTP.objects.get(otp=otp)
            # Save the user ID in session to use it in the reset password view
            request.session['reset_user_id'] = reset_entry.user.id
            return redirect('reset_password')
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return render(request, "enter_otp.html")

    return render(request, "enter_otp.html")


def reset_password(request):
        user_id = request.session.get('reset_user_id')

        if not user_id:
            messages.error(request, "Unauthorized access. Please restart the process.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(id=user_id)

            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                else:
                    user.set_password(password)
                    user.save()
                    del request.session['reset_user_id']  # Clear session after password reset
                    messages.success(request, "Your password has been reset successfully. You can now log in.")
                    return redirect('/login')
        except User.DoesNotExist:
            messages.error(request, "Invalid user.")
            return redirect('forgot_password')

        return render(request, 'reset_password.html')

import random
def CashOnDelivery(request):
    OrderID = random.randint(3000000000 , 90000000000)
    context = {}
    context['order_id'] = OrderID
    return render (request , "order_success.html" , context)




