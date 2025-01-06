// PayPal payment integration
class PaymentHandler {
    constructor() {
        this.paypalButtonsContainer = document.getElementById('paypal-button-container');
        this.orderData = null;
    }

    async initializePayPal(amount, orderId, productId) {
        if (!this.paypalButtonsContainer) {
            console.error('PayPal button container not found');
            return;
        }

        this.orderData = {
            order_id: orderId,
            product_id: productId,
            amount: amount
        };

        try {
            paypal.Buttons({
                createOrder: (data, actions) => {
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                value: amount.toFixed(2),
                                currency_code: 'USD'
                            }
                        }]
                    });
                },
                onApprove: async (data, actions) => {
                    try {
                        // Capture the PayPal order
                        const details = await actions.order.capture();
                        console.log('Payment completed:', details);

                        // Send payment details to our backend
                        await this.processPayment(details);

                    } catch (error) {
                        console.error('Payment processing error:', error);
                        this.showError('Payment processing failed. Please try again.');
                    }
                },
                onError: (err) => {
                    console.error('PayPal error:', err);
                    this.showError('PayPal encountered an error. Please try again.');
                }
            }).render(this.paypalButtonsContainer);

        } catch (error) {
            console.error('PayPal initialization error:', error);
            this.showError('Failed to initialize payment system.');
        }
    }

    async processPayment(paypalDetails) {
        try {
            const response = await fetch('/api/orders/' + this.orderData.order_id + '/payment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                    'Authorization': this.getAccessToken()
                },
                body: JSON.stringify({
                    payment_details: paypalDetails,
                    amount: this.orderData.amount,
                    product_id: this.orderData.product_id,
                    payment_method: 'paypal'
                })
            });

            if (!response.ok) {
                throw new Error('Payment verification failed');
            }

            const result = await response.json();
            console.log('Payment processed:', result);

            // Show success message and redirect
            this.showSuccess('Payment successful! Redirecting to orders...');
            setTimeout(() => {
                window.location.href = '/orders/';
            }, 2000);

        } catch (error) {
            console.error('Payment processing error:', error);
            this.showError('Failed to process payment. Please contact support.');
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    getAccessToken() {
        // Token already includes 'Bearer ' prefix from session
        return document.getElementById('access-token').value;
    }

    showSuccess(message) {
        const container = document.querySelector('.container');
        const alert = document.createElement('div');
        alert.className = 'alert alert-success';
        alert.innerHTML = message;
        container.insertBefore(alert, container.firstChild);
    }

    showError(message) {
        const container = document.querySelector('.container');
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger';
        alert.innerHTML = message;
        container.insertBefore(alert, container.firstChild);
    }
}

// Export for use in other files
window.PaymentHandler = PaymentHandler;
