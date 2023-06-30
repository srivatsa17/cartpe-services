import "../../css/CartScreen/CartQuantityDetails.css";

import React from "react";
import { emptyCart } from "../../actions/cartActions";
import { useDispatch } from "react-redux";

function CartQuantityDetails({ cartItems }) {
    const dispatch = useDispatch();
    const totalCartItemsQuantity = cartItems.length;
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