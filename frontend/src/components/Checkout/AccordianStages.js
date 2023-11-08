import "../../css/Checkout/AccordianStages.css";

import { Accordion, Button } from "react-bootstrap";
import React, { useState } from "react";

import DisplayCartItems from "./OrderItems/DisplayCartItems";
import PaymentOptions from "./PaymentOptions/PaymentOptions";
import ShippingAddress from "./ShippingAddress/ShippingAddress";
import ShippingAddressList from "./ShippingAddress/AddressList";
import { useSelector } from "react-redux";

function AccordianStages({
    activeKey,
    handleActiveAccordionItem,
    cartItems,
    isTermsAndConditionsChecked,
    setIsTermsAndConditionsChecked,
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
                        />
                    </Accordion.Body>
                </Accordion.Item>
                
                
                
                {/* <Accordion.Item eventKey="1">
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
                </Accordion.Item> */}
            </Accordion>
        </div>
    )
}

export default AccordianStages;