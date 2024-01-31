import "../../css/Checkout/AccordianStages.css";

import { Accordion } from "react-bootstrap";
import DisplayCartItems from "./OrderItems/DisplayCartItems";
import PaymentOptions from "./PaymentOptions/PaymentOptions";
import React from "react";
import ShippingAddress from "./ShippingAddress/ShippingAddress";

function AccordianStages({
    activeKey,
    handleActiveAccordionItem,
    cartItems,
    isTermsAndConditionsChecked,
    setIsTermsAndConditionsChecked,
    selectedAddress,
    setSelectedAddress,
    defaultAddress
}) {


    return (
        <div className="accordian-container">
            <Accordion activeKey={activeKey}>
                <Accordion.Item eventKey="0">
                    <Accordion.Header>
                        Select a Delivery Address
                    </Accordion.Header>
                    <Accordion.Body>
                        <ShippingAddress
                            handleActiveAccordionItem={handleActiveAccordionItem}
                            selectedAddress={selectedAddress}
                            setSelectedAddress={setSelectedAddress}
                            defaultAddress={defaultAddress}
                        />
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="1">
                    <Accordion.Header>Order Summary</Accordion.Header>
                    <Accordion.Body>
                        <DisplayCartItems
                            cartItems={cartItems}
                            handleActiveAccordionItem={handleActiveAccordionItem}
                        />
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="2">
                    <Accordion.Header>Payment Options</Accordion.Header>
                    <Accordion.Body>
                        <PaymentOptions
                            handleActiveAccordionItem={handleActiveAccordionItem}
                            isTermsAndConditionsChecked={isTermsAndConditionsChecked}
                            setIsTermsAndConditionsChecked={setIsTermsAndConditionsChecked}
                        />
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </div>
    )
}

export default AccordianStages;