import "../../css/CartScreen/CartItemDetails.css";

import { Col, Image, OverlayTrigger, Row, Tooltip } from "react-bootstrap";
import { FaRupeeSign, FaTrash } from "react-icons/fa";
import { removeFromCart, updateCartQuantity } from "../../actions/cartActions";

import { Link } from "react-router-dom";
import React from "react";
import { useDispatch } from "react-redux";

function CartItemDetails({ cartItem, featuredImage }) {
    const maxCartItemQuantity = Array.from({ length: 10 }, (_, index) => (index + 1));
    const productLink = `/products/${cartItem.product.slug}/${cartItem.product.id}/buy`;
    const dispatch = useDispatch();

    return (
        <Row>
            <Col xs={7} sm={6} md={6} lg={5} xl={4}>
                <Link to={productLink}>
                    <Image className="cart-featured-image" src={featuredImage} rounded/>
                </Link>
            </Col>
            <Col>
                <Link to={productLink} className="cart-item-to-product-link">
                    <div className="cart-item-brand-name">
                        {cartItem.product.brand}
                    </div>
                    <div className="cart-item-product-name">
                        {cartItem.product.name}
                    </div>
                </Link>

                <div className="cart-item-price-container">
                    <div id="cart-item-selling-price">
                        <FaRupeeSign size={16} id="rupee-icon"/>
                        { cartItem.product.selling_price }
                    </div>
                    {
                        cartItem.product.discount > 0 &&
                        <div id="cart-item-original-price">
                            <FaRupeeSign size={16} id="rupee-icon"/>
                            { cartItem.product.price }
                        </div>
                    }
                    {
                        cartItem.product.discount > 0 &&
                        <div id="cart-item-discount-percent">
                            ({cartItem.product.discount}% OFF)
                        </div>
                    }
                </div>

                <div className="cart-item-quantity">
                    <div className="quantity-title">Quantity</div>
                    <div>
                        <select
                            className="cart-item-quantity-select"
                            defaultValue={cartItem.quantity}
                            onChange={
                                (event) => dispatch(updateCartQuantity(cartItem.product, Number(event.target.value)))
                            }
                        >
                            {
                                maxCartItemQuantity.map((itemQuantity, index) => (
                                    <option key={index} value={itemQuantity}>
                                        {itemQuantity}
                                    </option>
                                ))
                            }
                        </select>
                    </div>

                    <div
                        className="cart-item-remove-button"
                        onClick={() => dispatch(removeFromCart(cartItem.product.id))}
                    >
                        <OverlayTrigger
                            placement="top"
                            overlay={
                                <Tooltip>
                                    Remove item from cart
                                </Tooltip>
                            }
                        >
                            <div><FaTrash size={20}/></div>
                        </OverlayTrigger>
                    </div>
                </div>
            </Col>
        </Row>
    )
}

export default CartItemDetails