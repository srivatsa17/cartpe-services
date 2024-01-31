import "../../css/Order/OrderPaymentFailed.css";

import { Button, Col, Container, Image, Row } from "react-bootstrap";

import { CHECKOUT_SCREEN } from "../../constants/routes";
import { LinkContainer } from "react-router-bootstrap";
import React from "react";
import { useLocation } from "react-router-dom";

function OrderPaymentFailedScreen() {
    const { state } = useLocation()
    const paymentErrorDescription = state?.paymentError ??
        "Encountered an issue processing your payment. Verify your details again";

    return (
        <Container>
            <Row>
                <Col xs={12} sm={12} md={7} lg={7} xl={6}>
                    <Image className="order-payment-failed" src="/images/payment_failed.jpg" />
                </Col>
                <Col className="order-payment-failed-heading">
                    <div>
                        Oops! Payment failed due to the following reason: <br />
                        <strong>{paymentErrorDescription}</strong><br /><br />
                        Please try once again!
                    </div>
                    <LinkContainer to={CHECKOUT_SCREEN}>
                        <Button className="mt-4" variant="dark">
                            Proceed to checkout
                        </Button>
                    </LinkContainer>
                </Col>
            </Row>
        </Container>
    )
}

export default OrderPaymentFailedScreen;