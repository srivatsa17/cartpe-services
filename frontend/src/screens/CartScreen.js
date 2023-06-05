import React from "react";
import { useSelector } from "react-redux";
import { Row, Col, ListGroup, Alert } from "react-bootstrap";
import CartQuantityDetails from "../components/CartScreen/CartQuantityDetails";
import CartSubTotal from "../components/CartScreen/CartSubTotal";
import CartItemDetails from "../components/CartScreen/CartItemDetails";
import "../css/CartScreen/CartScreen.css";

function CartScreen() {
    const cart = useSelector(state => state.cart);
    const { cartItems } = cart;

    return (
        <Row>
            <Col xs={8} sm={8} md={8} lg={8} xl={8}>
                <div className="shopping-cart-title">SHOPPING CART</div>
                <br />

                <CartQuantityDetails cartItems={cartItems}/>
                <br />

                {
                    cartItems.length === 0 ?
                    <Alert variant="warning">
                        Cart is empty. <Alert.Link href="/">Continue shopping</Alert.Link>
                    </Alert>
                    :
                    <ListGroup >
                        {
                            cartItems.map((cartItem, index) => {
                                const featuredImage = cartItem.product.product_images.find((imageObj) => imageObj.is_featured === true);
                                return (
                                    <ListGroup.Item key={index}>
                                        <CartItemDetails cartItem={cartItem} featuredImage={featuredImage}/>
                                    </ListGroup.Item>
                                )
                            })
                        }
                    </ListGroup>
                }
            </Col>
            <Col>
                <CartSubTotal cartItems={cartItems}/>
            </Col>
        </Row>
    )
}

export default CartScreen;