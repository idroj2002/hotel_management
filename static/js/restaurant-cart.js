function setColor(itemID) {
    const quantityElement = document.getElementById(`quantity-${itemID}`);
    const quantity = parseInt(quantityElement.textContent);
    const realQuantity = parseInt(quantityElement.dataset.realQuantity)
    const completePriceElement = document.getElementById(`complete-price-${itemID}`);
    if (realQuantity > quantity) {
        completePriceElement.classList.add('text-danger');
        quantityElement.classList.add('text-danger');
    } else if (realQuantity == quantity) {
        completePriceElement.classList.remove('text-danger');
        completePriceElement.classList.remove('text-success');
        quantityElement.classList.remove('text-danger');
        quantityElement.classList.remove('text-success');
    } else {
        completePriceElement.classList.add('text-success');
        quantityElement.classList.add('text-success');
    }
}

function setPrice(itemID) {
    const quantityElement = document.getElementById(`quantity-${itemID}`);
    const quantity = parseInt(quantityElement.textContent);
    const priceElement = document.getElementById(`price-${itemID}`);
    const price = document.getElementById(`modify-cart-${itemID}`).dataset.price;

    cartTotal = parseFloat((quantity * price)).toFixed(2);
    priceElement.textContent = cartTotal;
    setColor(itemID);
}

// Increment items number
document.querySelectorAll('.increment').forEach(button => {
    button.addEventListener('click', () => {
        const itemID = button.getAttribute('id').split('-')[2];
        const quantityElement = document.getElementById(`quantity-${itemID}`);
        let quantity = parseInt(quantityElement.textContent);
        quantity++;
        quantityElement.textContent = quantity;
        setPrice(itemID);
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
        setPrice(itemID);
    });
});

// Add products to cart
$(document).ready(function() {
    $('.modify-cart').click(function() {
        const itemID = $(this).attr('id').split('-')[2];
        const quantityElement = document.getElementById(`quantity-${itemID}`);
        const quantity = parseInt(quantityElement.textContent);
        const reservationID = $(this).data('reservation-id');

        quantityElement.dataset.realQuantity = quantity;
        setPrice(itemID);
        
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: '../../modify_cart/',
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