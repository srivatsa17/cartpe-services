import "../css/CartScreen/CartScreen.css";

import { Alert, Col, ListGroup, Row } from "react-bootstrap";

import CartItemDetails from "../components/CartScreen/CartItemDetails";
import CartQuantityDetails from "../components/CartScreen/CartQuantityDetails";
import CartSubTotal from "../components/CartScreen/CartSubTotal";
import { HOME_SCREEN } from "../constants/routes";
import { PLACEHOLDER_IMAGE } from "../constants/imageConstants";
import React from "react";
import { useSelector } from "react-redux";

const getProductFeaturedImage = (product) => {
    if(
        !product ||
        !product.product_images ||
        !product.product_images.find((image) => image.is_featured === true)
    ) {
        return PLACEHOLDER_IMAGE
    }
    return product.product_images.find((image) => image.is_featured === true).image
}

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
                                const featuredImage = getProductFeaturedImage(cartItem.product)
                                return (
                                    <ListGroup key={index} className="pb-4">
                                        <ListGroup.Item className="py-3">
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