import "../../css/Checkout/AccordianStages.css";

import { Accordion, Button } from "react-bootstrap";
import React, { useState } from "react";

import AddNewAddress from "./AddNewAddress";
import DisplayCartItems from "./DisplayCartItems";
import PaymentOptions from "./PaymentOptions";
import ShippingAddressList from "./ShippingAddressList";

function AccordianStages({
    activeKey,
    handleActiveAccordionItem,
    cartItems,
    isTermsAndConditionsChecked,
    setIsTermsAndConditionsChecked
}) {
    const [showAddressModal, setShowAddressModal] = useState(false);

    const handleShowNewAddressModal = () => setShowAddressModal(true);
    const handleCloseNewAddressModal = () => setShowAddressModal(false);

    return (
        <div className="accordian-container">
            <Accordion activeKey={activeKey}>
                <Accordion.Item eventKey="0">
                    <Accordion.Header>
                        Select a Delivery Address
                    </Accordion.Header>
                    <Accordion.Body>
                        <ShippingAddressList />
                        <Button variant="success" onClick={() => handleActiveAccordionItem("1")}>
                            Use this Address
                        </Button>
                        <Button className="mx-3" variant="dark" onClick={handleShowNewAddressModal}>
                            Add new Address
                        </Button>
                        <AddNewAddress
                            showAddressModal={showAddressModal}
                            handleCloseNewAddressModal={handleCloseNewAddressModal}
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