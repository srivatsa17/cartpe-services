import "../../css/Order/OrderFailed.css";

import { Button, Col, Container, Image, Row } from "react-bootstrap";

import { CHECKOUT_SCREEN } from "../../constants/routes";
import { LinkContainer } from "react-router-bootstrap";
import React from "react";

function OrderFailedScreen() {
    return (
        <Container>
            <Row>
                <Col xs={12} sm={12} md={12} lg={9} xl={8}>
                    <Image className="order-failed" src="/images/400_bad_request.jpg" />
                </Col>
                <Col className="order-failed-heading">
                    <div>
                        Oops! Something went wrong while creating your order. Please try once again!
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

export default OrderFailedScreen;