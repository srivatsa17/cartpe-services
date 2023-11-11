import { Col, Container, Row } from 'react-bootstrap';

import AccordianStages from '../components/Checkout/AccordianStages';
import AddressCard from '../components/Checkout/ShippingAddress/AddressCard';
import OrderSummaryCard from '../components/Checkout/OrderItems/OrderSummaryCard';
import Progress from '../components/Checkout/Progress';
import React from 'react';
import { useSelector } from 'react-redux';
import { useState } from 'react';

const getDefaultAddress = (addressList) => {
    const isDefaultAddressFound = addressList.find((address) => address.is_default);
    const defaultAddress = isDefaultAddressFound || (addressList.length > 0 ? addressList[0] : {});
    return defaultAddress;
}

function CheckoutScreen() {
    const { isLoggedIn } = useSelector(state => state.userLoginDetails)
    const { cartItems } = useSelector(state => state.cart)
    const { addressList } = useSelector(state => state.address)

    const steps = ['Logged In', 'Delivery Address', 'Order Summary', 'Payment Options'];

    const [activeStep, setActiveStep] = useState(isLoggedIn ? 1 : 0);
    const [activeKey, setActiveKey] = useState("0");

    const defaultAddress = getDefaultAddress(addressList ?? {})
    const [selectedAddress, setSelectedAddress] = useState(defaultAddress)

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
                                selectedAddress={selectedAddress}
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
                        selectedAddress={selectedAddress}
                        setSelectedAddress={setSelectedAddress}
                        defaultAddress={defaultAddress}
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