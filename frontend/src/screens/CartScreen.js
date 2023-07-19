import "../css/CartScreen/CartScreen.css";

import { Alert, Col, ListGroup, Row } from "react-bootstrap";

import CartItemDetails from "../components/CartScreen/CartItemDetails";
import CartQuantityDetails from "../components/CartScreen/CartQuantityDetails";
import CartSubTotal from "../components/CartScreen/CartSubTotal";
import { HOME_SCREEN } from "../constants/routes";
import React from "react";
import { useSelector } from "react-redux";

function CartScreen() {
    const cart = useSelector(state => state.cart);
    const { cartItems } = cart;

    return (
        <Row>
            <Col xs={12} sm={12} md={12} lg={7} xl={8} className="pb-4">
                <div className="shopping-cart-title">SHOPPING CART</div>
                <br />

                <CartQuantityDetails cartItems={cartItems}/>
                <br />

                {
                    cartItems.length === 0 ?
                    <Alert variant="warning">
                        Cart is empty. <Alert.Link href={HOME_SCREEN}>Continue shopping</Alert.Link>
                    </Alert>
                    :
                    <>
                        {
                            cartItems.map((cartItem, index) => {
                                const featuredImage = cartItem.product.product_images.find((imageObj) => imageObj.is_featured === true);
                                return (
                                    <ListGroup className="pb-4">
                                        <ListGroup.Item key={index} className="py-3">
                                            <CartItemDetails cartItem={cartItem} featuredImage={featuredImage}/>
                                        </ListGroup.Item>
                                    </ListGroup>
                                )
                            })
                        }
                    </>
                }
            </Col>
            <Col>
                <CartSubTotal cartItems={cartItems}/>
            </Col>
        </Row>
    )
}

export default CartScreen;