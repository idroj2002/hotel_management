// Increment items number
document.querySelectorAll('.increment').forEach(button => {
    button.addEventListener('click', () => {
        const itemID = button.getAttribute('id').split('-')[2];
        const quantityElement = document.getElementById(`quantity-${itemID}`);
        let quantity = parseInt(quantityElement.textContent);
        quantity++;
        quantityElement.textContent = quantity;
    });
});

// Decrement items number
document.querySelectorAll('.decrement').forEach(button => {
    button.addEventListener('click', () => {
        const itemID = button.getAttribute('id').split('-')[2];
        const quantityElement = document.getElementById(`quantity-${itemID}`);
        let quantity = parseInt(quantityElement.textContent);
        if (quantity > 0) {
            quantity--;
            quantityElement.textContent = quantity;
        }
    });
});

// Add products to cart
$(document).ready(function() {
    $('.add-to-cart').click(function() {
        const itemID = $(this).attr('id').split('-')[2];
        const quantityElement = document.getElementById(`quantity-${itemID}`);
        const quantity = parseInt(quantityElement.textContent);
        const price = $(this).data('price');
        const reservationID = $(this).data('reservation-id');
        const total = document.getElementById('total-price');

        const priceButtons = document.querySelectorAll('.price-button');
        priceButtons.forEach(function(button) {
            button.classList.remove('disabled');
            console.log("DIS");
        });
        
        if (quantity == 0){
            return;
        } else {
            quantityElement.textContent = 0;
            cartIncrement = parseFloat((quantity * price).toFixed(2));
            cartTotal = parseFloat(total.textContent) + cartIncrement;
            cartTotal = cartTotal.toFixed(2);
            total.textContent = cartTotal;
        }

        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        $.ajax({
            url: '../../add_to_cart/',
            type: 'POST',
            data: JSON.stringify({
                'item_id': itemID,
                'quantity': quantity,
                'reservation_id': reservationID
            }),
            dataType: 'json',
            contentType: 'application/json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            success: function(response) {
                // Success response
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Error response
                console.error(xhr.responseText);
            }
        });
    });
});