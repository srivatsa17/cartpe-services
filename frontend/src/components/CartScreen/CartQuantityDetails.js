import React from "react";
import { useDispatch } from "react-redux";
import { emptyCart } from "../../actions/cartActions";
import "../../css/CartScreen/CartQuantityDetails.css";

function CartQuantityDetails({ cartItems }) {
    const dispatch = useDispatch();
    const totalCartItemsQuantity = cartItems.reduce((sum, cartItem) => sum + cartItem.quantity, 0);
    const isCartEmpty = (cartItems.length === 0);

    return (
        <div className="cart-quantity-details">
            <div>
                Total Items in Cart - {totalCartItemsQuantity}
            </div>
            <button
                className="btn btn-dark"
                onClick={() => dispatch(emptyCart())}
                disabled={isCartEmpty}
            >
                Empty cart
            </button>
        </div>
    );
}

export default CartQuantityDetails