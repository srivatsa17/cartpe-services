import { Badge, Button, Form } from "react-bootstrap";
import React, { useEffect, useState } from "react";

import AlertMessage from "../../AlertMessages/AlertMessage";
import EditAddress from "./EditAddress";
import Loader from "../../Loader/Loader";
import { useSelector } from "react-redux";

const getDefaultAddress = (addressList) => {
    const isDefaultAddressFound = addressList.find((address) => address.is_default);
    const defaultAddress = isDefaultAddressFound || (addressList.length > 0 ? addressList[0] : {});
    return defaultAddress;
}

function AddressList({ handleRemoveShippingAddress, handleEditShippingAddress }) {
    const { isLoading, addressList, error } = useSelector(state => state.address)

    const defaultAddress = getDefaultAddress(addressList ?? {})
    const [selectedAddress, setSelectedAddress] = useState(defaultAddress)

    // On POST/DELETE operations, selectedAddress still holds the previous state value.
    // To resolve this issue, we trigger useEffect to set the latest value of defaultAddress as the selectedAddress.
    useEffect(() => {
        setSelectedAddress(defaultAddress);
    }, [defaultAddress]);

    const  handleShippingAddressSelect = (address) => {
        setSelectedAddress(address)
    }

    const [showEditAddressModal, setShowEditAddressModal] = useState(false)

    const addressLabel = (shippingAddress) => {
        return (
            <div className="mx-3">
                <div>
                    <strong>{shippingAddress.name}</strong>
                    <Badge pill bg="dark" style={{ "marginLeft": "40px"}}>{shippingAddress.type}</Badge>
                </div>
                <div className="mt-2">
                {
                    // Doing this to format the content to fit in the editor screen without losing the whitespace in between.
                    `${shippingAddress.address.line1}, ${shippingAddress.address.line2}, ${shippingAddress.address.city},
                    ${shippingAddress.address.state}, ${shippingAddress.address.country} - ${shippingAddress.address.pin_code}`
                }
                </div>
                <div className="mt-2">
                    Phone Number - {shippingAddress.alternate_phone}
                </div>
            </div>
        )
    }

    return (
        <React.Fragment>
        {
            isLoading ?
            <>
                <Loader />
                <br /><br />
            </>
            : error ?
                <div className="mb-3">
                    <AlertMessage variant="danger">Error in obtaining shipping address list.</AlertMessage>
                </div>
            : addressList.length === 0 ?
                <div className="mb-3">
                    Looks like there is no shipping address added yet. Please go ahead and add one!
                </div>
            :
            <React.Fragment>
            {
                addressList?.map((address, index) => {
                    return (
                        <div key={index}>
                            <Form.Check
                                inline
                                label={addressLabel(address)}
                                type="radio"
                                checked={
                                    selectedAddress ?
                                    address.id === selectedAddress.id :
                                    address.id === defaultAddress?.id
                                }
                                onChange={() => handleShippingAddressSelect(address)}
                            />
                            {
                                (
                                    selectedAddress ?
                                    address.id === selectedAddress.id :
                                    address.id === defaultAddress?.id
                                ) &&
                                <div className="my-3" style={{ "marginLeft": "40px"}}>
                                    <Button
                                        variant="outline-dark"
                                        onClick={() => setShowEditAddressModal(true)}
                                    >
                                        Edit
                                    </Button>
                                    <Button
                                        variant="outline-danger"
                                        className="mx-3"
                                        onClick={() => handleRemoveShippingAddress(address.id)}
                                    >
                                        Remove
                                    </Button>
                                    <EditAddress
                                        showEditAddressModal={showEditAddressModal}
                                        setShowEditAddressModal={setShowEditAddressModal}
                                        address={address}
                                        handleEditShippingAddress={handleEditShippingAddress}
                                    />
                                </div>
                            }
                            <hr />
                        </div>
                    )
                })
            }
            </React.Fragment>
        }
        </React.Fragment>
    )
}

export default AddressList;