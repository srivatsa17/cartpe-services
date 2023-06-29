import React from "react";
import { ListGroup, Button } from "react-bootstrap";
import { FaRupeeSign } from "react-icons/fa";
import "../../css/CartScreen/CartSubTotal.css";

function CartSubTotal({ cartItems }) {
    const totalCartItemsQuantity = cartItems.length;
    const totalMRP = cartItems.reduce((sum, cartItem) => sum + cartItem.quantity * cartItem.product.price, 0).toFixed(2);
    const minusSign = "-";
    const totalDiscountPrice = cartItems.reduce(
        (sum, cartItem) => sum + cartItem.quantity * cartItem.product.discounted_price, 0
    ).toFixed(2)
    const totalSellingPrice = cartItems.reduce(
        (sum, cartItem) => sum + cartItem.quantity * cartItem.product.selling_price, 0
    ).toFixed(2)
    const isCartEmpty = (cartItems.length === 0);

    return (
        <>
            <div className="cart-subtotal-title">
                SUBTOTAL ({totalCartItemsQuantity} items)
            </div>
            <br />
            <ListGroup className="cart-subtotal-price-container">
                <ListGroup.Item className="cart-subtotal-mrp-container">
                    <div>Total MRP</div>
                    <div>
                        <FaRupeeSign id="rupee-icon"/>{totalMRP}
                    </div>
                </ListGroup.Item>

                <ListGroup.Item className="cart-subtotal-discounted-price-container">
                    <div>Discount on MRP</div>
                    <div className="cart-subtotal-discounted-price">
                        {minusSign}<FaRupeeSign id="rupee-icon"/>{totalDiscountPrice}
                    </div>
                </ListGroup.Item>

                <ListGroup.Item className="cart-subtotal-selling-price-container">
                    <div>Total Amount</div>
                    <div className="cart-subtotal-selling-price">
                        <FaRupeeSign id="rupee-icon"/>{totalSellingPrice}
                    </div>
                </ListGroup.Item>
            </ListGroup>
            <br />
            <Button className="checkout-button" variant="dark" disabled={isCartEmpty}>
                Proceed to checkout
            </Button>
        </>
    );
}

export default CartSubTotal