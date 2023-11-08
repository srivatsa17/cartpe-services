import { Col, Container, Row } from 'react-bootstrap';

import AccordianStages from '../components/Checkout/AccordianStages';
import AddressCard from '../components/Checkout/ShippingAddress/AddressCard';
import OrderSummaryCard from '../components/Checkout/OrderItems/OrderSummaryCard';
import Progress from '../components/Checkout/Progress';
import React from 'react';
import { useSelector } from 'react-redux';
import { useState } from 'react';

function CheckoutScreen() {
    const { isLoggedIn } = useSelector(state => state.userLoginDetails)
    const { cartItems } = useSelector(state => state.cart)

    const steps = ['Logged In', 'Delivery Address', 'Order Summary', 'Payment Options'];

    const [activeStep, setActiveStep] = useState(isLoggedIn ? 1 : 0);
    const [activeKey, setActiveKey] = useState("0");
    const [isTermsAndConditionsChecked, setIsTermsAndConditionsChecked] = useState(false);

    const handleNextAccordionItem = () => {
        setActiveStep(activeStep + 1);
    };

    const handlePreviousAccordionItem = () => {
        setActiveStep(activeStep - 1);
    }

    const handleActiveAccordionItem = (eventKey) => {
        activeKey < eventKey ? handleNextAccordionItem() : handlePreviousAccordionItem();
        setActiveKey(eventKey);
    }

    const checkoutCardComponent = () => {
        switch(activeStep) {
            case 1: return  <AddressCard
                                handleActiveAccordionItem={handleActiveAccordionItem}
                                cartItems={cartItems}
                                nextAccordionItemEventKey={"1"}
                            />;
            case 2: return <OrderSummaryCard
                                handleActiveAccordionItem={handleActiveAccordionItem}
                                cartItems={cartItems}
                                nextAccordionItemEventKey={"2"}
                            />;
            case 3: return  <OrderSummaryCard
                                handleActiveAccordionItem={handleActiveAccordionItem}
                                cartItems={cartItems}
                                nextAccordionItemEventKey={"3"}
                                isTermsAndConditionsChecked={isTermsAndConditionsChecked}
                            />;
            default:return <></>;
        }
    }

    return (
        <Container>
            <Row>
                <Progress steps={steps} activeStep={activeStep} />
            </Row>
            <Row>
                <Col lg={8}>
                    <AccordianStages
                        activeKey={activeKey}
                        handleActiveAccordionItem={handleActiveAccordionItem}
                        cartItems={cartItems}
                        isTermsAndConditionsChecked={isTermsAndConditionsChecked}
                        setIsTermsAndConditionsChecked={setIsTermsAndConditionsChecked}
                    />
                </Col>
                <Col>
                    {checkoutCardComponent()}
                </Col>
            </Row>
        </Container>
    );
}

export default CheckoutScreen;