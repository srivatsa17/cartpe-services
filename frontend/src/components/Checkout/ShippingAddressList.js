import { Button, Form } from "react-bootstrap";
import React, { useState } from "react";

import EditAddress from "./EditAddress";

const shippingAddress = [
    {
        "name":"Srivatsa",
        "is_default":true,
        "line1":"014 A Block, DS Max Synergy",
        "line2":"Agrahara Layout main road",
        "city":"Bangalore",
        "state":"Karnataka",
        "country":"India",
        "pin_code":"560064",
        "alternate_phone":"9008430442"
    },
    {
        "name":"Chaithra",
        "is_default":false,
        "line1":"014 A Block, DS Max Synergy",
        "line2":"Agrahara Layout main road",
        "city":"Bangalore",
        "state":"Karnataka",
        "country":"India",
        "pin_code":"560064",
        "alternate_phone":"8277452193"
    }
]

function ShippingAddressList() {
    const defaultAddressId = shippingAddress?.findIndex((shippingAddress) => shippingAddress.is_default)

    const [selectedItem, setSelectedItem] = useState(defaultAddressId);

    const [showAddressModal, setShowAddressModal] = useState(false);

    const handleShowNewAddressModal = () => setShowAddressModal(true);
    const handleCloseNewAddressModal = () => setShowAddressModal(false);

    const addressLabel = (shippingAddress) => {
        return (
            <div>
                <b>{shippingAddress.name}</b> - {shippingAddress.line1}, {shippingAddress.line2}, {shippingAddress.city}, {shippingAddress.state}, {shippingAddress.country}, {shippingAddress.pin_code}, {shippingAddress.alternate_phone}
            </div>
        )
    }

    const handleCheckboxClick = (index) => {
        setSelectedItem(index)
    }

    return (
        <React.Fragment>
        {
            shippingAddress?.map((address, index) => {
                return (
                    <div key={index}>
                        <Form.Check
                            inline
                            label={addressLabel(address)}
                            name="group1"
                            type="checkbox"
                            checked={index === selectedItem}
                            onChange={() => handleCheckboxClick(index)}
                        />
                        {
                            selectedItem === index &&
                            <div>
                                <Button
                                    className="mx-4 mt-2"
                                    variant="outline-dark"
                                    onClick={handleShowNewAddressModal}
                                >
                                    Edit
                                </Button>
                                <Button className="mt-2" variant="outline-danger">
                                    Remove
                                </Button>
                                <EditAddress
                                    showAddressModal={showAddressModal}
                                    handleCloseNewAddressModal={handleCloseNewAddressModal}
                                    address={address}
                                />
                            </div>
                        }
                        <hr />
                    </div>
                )
            })
        }
        </React.Fragment>
    );
}

export default ShippingAddressList;