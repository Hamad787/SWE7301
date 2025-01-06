from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Order, MeasurementData, Payment
from .serializers import ProductSerializer, OrderSerializer, MeasurementDataSerializer, PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from .utils import make_api_request
from .logging_utils import (
    logger, log_function_call, log_request_details,
    log_response_details, log_session_data
)
from urllib.parse import urljoin

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


@log_function_call
def login_view(request):
    """ Login page to authenticate using Flask API """
    log_request_details(request, prefix='Login - ')
    log_session_data(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            messages.error(request, 'Both username and password are required')
            return render(request, 'login.html')
            
        try:
            logger.info(f"Attempting login for user: {username}")
            
            # Send login request to Flask API
            response = make_api_request(
                'POST',
                settings.FLASK_API['ENDPOINTS']['AUTH'],
                json={
                    'username': username,
                    'password': password
                }
            )
            
            logger.debug(f"Login response received: {response}")
            
            # Check for tokens in response
            access_token = response.get('access_token')
            refresh_token = response.get('refresh_token')
            
            if access_token and refresh_token:
                # Store complete token with Bearer prefix in session
                request.session['access_token'] = f'Bearer {access_token}'
                request.session['refresh_token'] = refresh_token
                request.session['username'] = username
                
                logger.info(f"Login successful for user: {username}")
                logger.debug("Session updated with new tokens")
                log_session_data(request)
                
                messages.success(request, f'Welcome back, {username}!')
                return redirect(reverse('frontend:home'))
            else:
                logger.warning(f"Login failed for user {username}: Invalid credentials or server error")
                messages.error(request, 'Invalid credentials or server error')
                
        except ValidationError as e:
            logger.error(f"Login error for user {username}: {str(e)}")
            messages.error(request, str(e))
            
    return render(request, 'login.html')

@log_function_call
def home(request):
    """Home page displaying products from Flask API"""
    log_request_details(request, prefix='Home - ')
    log_session_data(request)
    
    if 'username' not in request.session:
        logger.warning("No username in session, redirecting to login")
        messages.error(request, 'Please login to view products')
        return redirect(reverse('frontend:login'))
        
    try:
        # Get products from Flask API
        token = request.session.get('access_token')
        if not token:
            logger.warning("No access token found, redirecting to login")
            messages.error(request, 'Please login again')
            return redirect(reverse('frontend:login'))
            
        # Remove 'Bearer ' prefix if it exists
        if token.startswith('Bearer '):
            token = token[7:]
            
        response = make_api_request(
            'GET',
            settings.FLASK_API['ENDPOINTS']['PRODUCTS'],
            token=token  # Pass clean token
        )
        
        logger.debug(f"Products response: {response}")
        return render(request, 'home.html', {
            'products': response,
            'username': request.session.get('username')
        })
        
    except Exception as e:
        logger.error(f"Error loading products: {str(e)}")
        messages.error(request, f'Error loading products: {str(e)}')
        return render(request, 'home.html', {'products': [], 'username': request.session.get('username')})

@log_function_call
def add_product(request):
    """Handle adding a product via the Flask API."""
    logger.debug("Entering add_product view")
    log_request_details(request, prefix='Add Product - ')
    log_session_data(request)
    
    access_token = request.session.get('access_token')
    if not access_token:
        logger.warning("Add product attempted without access token")
        return JsonResponse({'error': 'Please login to add products'}, status=401)
        
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            import json
            data = json.loads(request.body)
            logger.debug(f"Received product data: {data}")
            
            product_data = {
                'name': data.get('name'),
                'description': data.get('description'),
                'price': float(data.get('price', 0))
            }
            
            logger.debug(f"Making API request to add product with data: {product_data}")
            response = make_api_request(
                'POST',
                'products',
                data=product_data,
                token=access_token
            )
            
            logger.info("Product added successfully")
            return JsonResponse({'message': 'Product added successfully!', 'data': response})
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
        except (ValueError, TypeError) as e:
            logger.error(f"Data validation error: {str(e)}")
            return JsonResponse({'error': 'Invalid product data provided'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@log_function_call
def order_list(request):
    """Orders page displaying orders from Flask API"""
    log_request_details(request, prefix='Orders - ')
    log_session_data(request)
    
    access_token = request.session.get('access_token')
    if not access_token:
        messages.error(request, 'Please login to view orders')
        return redirect(reverse('frontend:login'))
        
    try:
        # Remove 'Bearer ' prefix if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
            
        # Get orders from Flask API
        orders = make_api_request(
            'GET',
            settings.FLASK_API['ENDPOINTS']['ORDERS'],
            token=access_token
        )
        
        logger.debug(f"Raw orders from API: {orders}")
        
        # Process each order to get product details and calculate total
        processed_orders = []
        for order in orders:
            try:
                # Get product details
                product = make_api_request(
                    'GET',
                    settings.FLASK_API['ENDPOINTS']['PRODUCT_DETAIL'].format(order['product_id']),
                    token=access_token
                )
                
                # Calculate total amount
                quantity = int(order.get('quantity', 1))
                unit_price = float(product.get('price', 0))
                total_amount = quantity * unit_price
                
                # Get payment status
                try:
                    payment = make_api_request(
                        'GET',
                        settings.FLASK_API['ENDPOINTS']['ORDER_PAYMENT'].format(order['id']),
                        token=access_token
                    )
                    payment_status = payment.get('status', 'pending') if payment else 'pending'
                except Exception as e:
                    logger.error(f"Error fetching payment status for order {order['id']}: {str(e)}")
                    payment_status = 'pending'
                
                # Add calculated fields to order
                order['total_amount'] = total_amount
                order['product_name'] = product.get('name', f'Product {order["product_id"]}')
                order['unit_price'] = unit_price
                order['payment_status'] = payment_status
                
                processed_orders.append(order)
                logger.debug(f"Processed order: {order}")
                
            except Exception as e:
                logger.error(f"Error processing order {order.get('id')}: {str(e)}")
                continue
        
        return render(request, 'orders.html', {'orders': processed_orders})
        
    except Exception as e:
        logger.error(f"Error loading orders: {str(e)}")
        messages.error(request, f'Error loading orders: {str(e)}')
        return render(request, 'orders.html', {'orders': []})

class ProductViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    @log_function_call
    def handle_api_error(self, error):
        """Handle API errors and return appropriate response"""
        logger.error(f"API Error: {str(error)}")
        if 'Authentication failed' in str(error):
            return Response(
                {'error': 'Authentication failed', 'code': 'auth_failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'error': str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @log_function_call
    def get(self, request, product_id=None):
        # Check if user is authenticated via session
        if not request.session.get('access_token'):
            return Response(
                {'error': 'Please login first', 'code': 'auth_required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        endpoint = f"{settings.FLASK_API['ENDPOINTS']['PRODUCTS']}/{product_id}" if product_id else settings.FLASK_API['ENDPOINTS']['PRODUCTS']
        try:
            data = make_api_request('GET', endpoint, token=request.session.get('access_token'))
            return Response(data)
        except ValidationError as e:
            return self.handle_api_error(e)
            
    @log_function_call
    def post(self, request):
        # Check if user is authenticated via session
        log_request_details(request, prefix='ProductViewSet.post - ')
        log_session_data(request)
        
        access_token = request.session.get('access_token')
        if not access_token:
            logger.warning("Product addition attempted without access token")
            return Response(
                {'error': 'Please login first', 'code': 'auth_required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            logger.debug(f"Received product data: {request.data}")
            
            data = make_api_request(
                'POST',
                settings.FLASK_API['ENDPOINTS']['PRODUCTS'],
                data=request.data,
                token=access_token
            )
            
            logger.info(f"Product added successfully: {data}")
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Error adding product: {str(e)}")
            return self.handle_api_error(e)
            
    @log_function_call
    def put(self, request, product_id):
        # Check if user is authenticated via session
        if not request.session.get('access_token'):
            return Response(
                {'error': 'Please login first', 'code': 'auth_required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            data = make_api_request(
                'PUT',
                f"{settings.FLASK_API['ENDPOINTS']['PRODUCTS']}/{product_id}",
                data=request.data,
                token=request.session.get('access_token')
            )
            return Response(data)
        except ValidationError as e:
            return self.handle_api_error(e)
            
    @log_function_call
    def delete(self, request, product_id):
        # Check if user is authenticated via session
        if not request.session.get('access_token'):
            return Response(
                {'error': 'Please login first', 'code': 'auth_required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            make_api_request(
                'DELETE',
                f"{settings.FLASK_API['ENDPOINTS']['PRODUCTS']}/{product_id}",
                token=request.session.get('access_token')
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return self.handle_api_error(e)

class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @log_function_call
    def get(self, request, order_id=None):
        endpoint = f"{settings.FLASK_API['ENDPOINTS']['ORDERS']}/{order_id}" if order_id else settings.FLASK_API['ENDPOINTS']['ORDERS']
        try:
            data = make_api_request('GET', endpoint, token=request.session.get('access_token'))
            return Response(data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    @log_function_call
    def post(self, request):
        try:
            data = make_api_request(
                'POST',
                settings.FLASK_API['ENDPOINTS']['ORDERS'],
                data=request.data,
                token=request.session.get('access_token')
            )
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MeasurementDataView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @log_function_call
    def get(self, request):
        measurements = MeasurementData.objects.all()
        serializer = MeasurementDataSerializer(measurements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @log_function_call
    def post(self, request):
        serializer = MeasurementDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @log_function_call
    def post(self, request, order_id=None):
        """Process payment for an order"""
        logger.debug("Processing payment request")
        log_request_details(request, prefix='Payment - ')
        log_session_data(request)
        
        try:
            # Get payment data from request
            payment_data = {
                'order_id': order_id,
                'payment_details': request.data.get('payment_details'),
                'amount': float(request.data.get('amount', 0)),
                'product_id': request.data.get('product_id'),
                'payment_method': request.data.get('payment_method', 'paypal')
            }
            logger.debug(f"Payment data: {payment_data}")
            
            # Validate payment data
            if not all([payment_data['payment_details'], payment_data['amount'], payment_data['product_id']]):
                logger.error("Missing required payment data")
                return Response(
                    {'error': 'Missing required payment data'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Forward payment to Flask API
            response = make_api_request(
                'POST',
                f'orders/{order_id}/payment' if order_id else 'payments',
                data=payment_data,
                token=request.session.get('access_token')
            )
            
            logger.info(f"Payment processed successfully: {response}")
            return Response(response, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.error(f"Payment validation error: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Payment processing error: {str(e)}")
            return Response(
                {'error': 'Payment processing failed'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@log_function_call
def create_order(request, product_id):
    """Create a new order and redirect to payment"""
    logger.debug(f"Creating order for product {product_id}")
    log_request_details(request, prefix='Create Order - ')
    
    try:
        # Get data from request
        data = json.loads(request.body)
        logger.debug(f"Order data received: {data}")
        
        # Get access token
        access_token = request.session.get('access_token')
        if not access_token:
            logger.error("No access token found in session")
            return JsonResponse({'error': 'Authentication required'}, status=401)
            
        # Remove 'Bearer ' prefix if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
        
        # Prepare order data - use total_amount from frontend if provided
        order_data = {
            'customer_name': str(data.get('customer_name', '')).strip(),
            'customer_email': str(data.get('customer_email', '')).strip(),
            'product_id': int(product_id),
            'quantity': int(data.get('quantity', 1)),
            'total_amount': float(data.get('total_amount', 0))
        }
        
        logger.debug(f"Sending order data to API: {order_data}")
        
        # Create order via Flask API
        order = make_api_request(
            'POST',
            'api/orders',  # Updated endpoint
            token=access_token,
            json=order_data
        )
        
        logger.info(f"Order created successfully: {order}")
        
        # Return success with redirect URL
        return JsonResponse({
            'status': 'success',
            'message': 'Order created successfully',
            'redirect_url': reverse('frontend:orders')
        })
        
    except json.JSONDecodeError:
        error_msg = "Invalid JSON data received"
        logger.error(error_msg)
        return JsonResponse({'error': error_msg}, status=400)
    except Exception as e:
        error_msg = f"Error creating order: {str(e)}"
        logger.error(error_msg)
        return JsonResponse({'error': error_msg}, status=500)

@log_function_call
def order_payment(request, order_id):
    """Display payment page for an order"""
    logger.debug(f"Displaying payment page for order {order_id}")
    log_request_details(request, prefix='Payment Page - ')
    log_session_data(request)
    
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            messages.error(request, 'Please login to view payment page')
            return redirect(reverse('frontend:login'))
            
        # Remove 'Bearer ' prefix if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
            
        # Get order details
        order = make_api_request(
            'GET',
            settings.FLASK_API['ENDPOINTS']['ORDER_DETAIL'].format(order_id),
            token=access_token
        )
        
        logger.debug(f"Raw order from API: {order}")
        
        # Get product details to calculate price
        product = make_api_request(
            'GET',
            settings.FLASK_API['ENDPOINTS']['PRODUCT_DETAIL'].format(order["product_id"]),
            token=access_token
        )
        
        logger.debug(f"Product details: {product}")
        
        # Calculate total amount
        quantity = int(order.get('quantity', 1))
        unit_price = float(product.get('price', 0))
        total_amount = quantity * unit_price
        
        # Update order with calculated amount and product details
        order.update({
            'total_amount': total_amount,
            'unit_price': unit_price,
            'product_name': product.get('name', f'Product {order["product_id"]}'),
            'payment_status': order.get('payment_status', 'pending')
        })
        
        logger.debug(f"Processed order: {order}")
        
        return render(request, 'order_payment.html', {
            'order': order,
            'product': product
        })
        
    except Exception as e:
        logger.error(f"Error loading payment page: {str(e)}")
        messages.error(request, f'Error loading payment page: {str(e)}')
        return redirect('frontend:orders')

@log_function_call
def process_payment(request, order_id):
    """Process payment for an order"""
    logger.debug(f"Processing payment for order {order_id}")
    log_request_details(request, prefix='Process Payment - ')
    
    try:
        # Get payment data from request
        data = json.loads(request.body)
        logger.debug(f"Payment data received: {data}")
        
        access_token = request.session.get('access_token')
        if not access_token:
            logger.error("No access token found in session")
            return JsonResponse({'error': 'Authentication required'}, status=401)
            
        # Remove 'Bearer ' prefix if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
        
        # Process payment via Flask API
        payment_data = {
            'order_id': int(order_id),
            'amount': float(data.get('amount', 0)),
            'payment_method': data.get('payment_method', 'paypal'),
            'payment_details': {
                'payment_id': data.get('payment_details', {}).get('payment_id', ''),
                'status': data.get('payment_details', {}).get('status', '')
            }
        }
        
        logger.debug(f"Sending payment data to API: {payment_data}")
        
        payment_response = make_api_request(
            'POST',
            'api/payment/order/' + str(order_id),  # Updated endpoint
            token=access_token,
            json=payment_data
        )
        
        logger.info(f"Payment processed successfully: {payment_response}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Payment processed successfully',
            'data': payment_response
        })
        
    except json.JSONDecodeError:
        error_msg = "Invalid payment data received"
        logger.error(error_msg)
        return JsonResponse({'error': error_msg}, status=400)
    except Exception as e:
        error_msg = f"Payment failed: {str(e)}"
        logger.error(error_msg)
        return JsonResponse({'error': error_msg}, status=500)

@log_function_call
def get_payment_status(request, order_id):
    """Get payment status for an order"""
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        # Remove 'Bearer ' prefix if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]

        # Get payment status from Flask API
        payment = make_api_request(
            'GET',
            settings.FLASK_API['ENDPOINTS']['ORDER_PAYMENT'].format(order_id),
            token=access_token
        )
        
        return JsonResponse({
            'status': payment.get('status', 'pending') if payment else 'pending'
        })
    except Exception as e:
        logger.error(f"Error getting payment status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
