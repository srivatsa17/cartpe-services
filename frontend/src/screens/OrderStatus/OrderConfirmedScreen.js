import "../../css/Order/OrderConfirmed.css";

import { Button, Col, Container, Image, Row } from "react-bootstrap";
import { HOME_SCREEN, ORDER_SCREEN } from "../../constants/routes";

import { LATEST_ORDER } from "../../constants/localStorageConstants";
import { LinkContainer } from "react-router-bootstrap";
import React from "react";
import getItemFromStorage from "../../utils/localStorage/getItemFromStorage";
import { useSearchParams } from "react-router-dom";

function OrderConfirmedScreen() {
    const [queryParams] = useSearchParams()
    const orderIdFromUrl = Number(queryParams.get('orderId'))
    const orderFromStorage = getItemFromStorage(LATEST_ORDER)

    return (
        <Container>
        {
            (orderIdFromUrl === orderFromStorage.id) ?
            <Row>
                <Col xs={12} sm={12} md={8} lg={8} xl={6}>
                    <Image className="order-confirmed" src="/images/order_confirmed.jpg" />
                </Col>
                <Col className="order-confirmed-heading">
                    <div>
                        Yayy! Your order has been <strong>confirmed</strong>! <br />
                        and the invoice details will be sent to your email. <br />
                        The order will be delivered to you within 7 working days. <br />
                        Happy shopping at <strong>CartPe</strong>!
                    </div>
                    <LinkContainer to={HOME_SCREEN}>
                        <Button className="mt-5" variant="dark">
                            Continue Shopping
                        </Button>
                    </LinkContainer>
                    <LinkContainer to={ORDER_SCREEN}>
                        <Button className="mt-5 mx-3" variant="success">
                            Check orders
                        </Button>
                    </LinkContainer>
                </Col>
            </Row>
            :
            <Row>
                <Col xs={12} sm={12} md={8} lg={8} xl={6}>
                    <Image className="order-confirmed" src="/images/wrong_order_access.jpg" />
                </Col>
                <Col className="order-confirmed-heading">
                    <div>
                        Oops! We are unable to access the requested order. Please verify the order details and
                        ensure proper permissions, or check existing orders for the desired information.
                    </div>
                    <LinkContainer to={ORDER_SCREEN}>
                        <Button className="mt-3" variant="dark">
                            Check your orders
                        </Button>
                    </LinkContainer>
                </Col>
            </Row>
        }
        </Container>
    )
}

export default OrderConfirmedScreen;