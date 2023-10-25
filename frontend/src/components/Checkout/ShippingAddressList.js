import { Form } from "react-bootstrap";
import React from "react";

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
        "alternate_phone":"9008430442"
    }
]

function ShippingAddressList() {
    return (
        <React.Fragment>
        {
            shippingAddress?.map((shippingAddress, index) => {
                return (
                    <div key={index}>
                        <Form.Check
                            inline
                            label={
                                <div>
                                    <b>{shippingAddress.name}</b> {shippingAddress.line1}, {shippingAddress.line2}, {shippingAddress.city}, {shippingAddress.state}, {shippingAddress.country}, {shippingAddress.pin_code}, {shippingAddress.alternate_phone}
                                </div>
                            }
                            name="group1"
                            type="radio"
                            defaultChecked={shippingAddress.is_default}
                        />
                        <hr />
                    </div>
                )
            })
        }
        </React.Fragment>
    );
}

export default ShippingAddressList;