from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Order, MeasurementData, Payment
from .serializers import ProductSerializer, OrderSerializer, MeasurementDataSerializer, PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def get_flask_data(request):
    flask_api_url = 'http://127.0.0.1:5000/api'  # Flask API URL
    response = requests.get(flask_api_url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch data from Flask API."}, status=500)

def get_jwt_token(request):
    """
    Retrieve the JWT token from the request headers or session.
    This assumes you are using JWT for authentication.
    """
    token = request.headers.get('Authorization')  # Assuming token is sent in Authorization header
    if token and token.startswith('Bearer '):
        return token.split(' ')[1]
    return None


def login_view(request):
    """ Login page to authenticate using Flask API """
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # Prepare the data to send to Flask API for authentication
        login_data = {
            'username': username,
            'password': password
        }

        # Send the login request to Flask API
        response = requests.post('http://127.0.0.1:5000/api/login', json=login_data)
        print(response.status_code)
        # Check if the response is successful
        if response.status_code == 200:
            # Successful login, store the JWT token in session or cookies
            access_token = response.json().get('access_token')
            request.session['access_token'] = access_token  # Save token in session for later use
            messages.success(request, 'Login successful!')  # Show success message
            return redirect('product-list')  # Redirect to homepage or dashboard after login
        else:
            # Show an error message if login fails
            messages.error(request, 'Invalid credentials')  # Show error message

    return render(request, 'login.html')

def home(request):
    """ Home page that will display products from Flask API """
    token = request.session.get('access_token')  # Retrieve the JWT token
    headers = {'Authorization': f'Bearer {token}'}
    print("Token: ",token)
    response = requests.get('http://127.0.0.1:5000/api/products', headers=headers)
    # Fetch products data from Flask API
    # response = requests.get('http://127.0.0.1:5000/flask-data/api/products')
    
    if response.status_code == 200:
        products = response.json()  # Parse the JSON response from Flask API
    else:
        products = []
    
    return render(request, 'home.html', {'products': products})


def order_list(request):
    """ Page to display orders from Flask API """
    # Fetch orders data from Flask API
    response = requests.get('http://127.0.0.1:5000/flask-data/api/orders')
    
    if response.status_code == 200:
        orders = response.json()  # Parse the JSON response from Flask API
    else:
        orders = []
    
    return render(request, 'orders.html', {'orders': orders})

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

def add_product(request):
    """Handle adding a product via the Flask API."""
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        # Prepare data for API
        product_data = {
            'name': name,
            'description': description,
            'price': float(price),
        }

        print(product_data)

        # Send the data to the Flask API
        try:
            response = requests.post(
                'http://127.0.0.1:5000/api/products',
                json=product_data,
                headers={
                    'Authorization': f'Bearer {request.session.get("access_token")}',  # Use JWT token from session
                    'Content-Type': 'application/json'
                }
            )

            print(response)

            # Handle API response
            if response.status_code == 201:
                messages.success(request, 'Product added successfully!')
                return redirect('product-list')  # Redirect to product list after success
            else:
                error = response.json()
                messages.error(request, f"Error: {error.get('message', 'Failed to add product.')}")
        except requests.RequestException as e:
            messages.error(request, 'Failed to connect to the API.')

    # Render the form for GET requests
    return render(request, 'add_product.html')

# Product View
class ProductViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, product_id=None):
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


# Order View
class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, order_id=None):
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return Response({'message': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


# Measurement Data View
class MeasurementDataView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        measurements = MeasurementData.objects.all()
        serializer = MeasurementDataSerializer(measurements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MeasurementDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Payment View
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            payment_serializer = PaymentSerializer(data=request.data)
            if payment_serializer.is_valid():
                payment_serializer.save(order=order)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
