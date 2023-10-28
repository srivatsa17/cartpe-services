import { Button, Form } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import { getShippingAddressList, removeShippingAddress } from "../../actions/addressActions";
import { useDispatch, useSelector } from "react-redux";

import AlertMessage from "../AlertMessages/AlertMessage";
import EditAddress from "./EditAddress";
import Loader from "../Loader/Loader";

function ShippingAddressList() {
    const dispatch = useDispatch()
    useEffect(() => {
        dispatch(getShippingAddressList())
    }, [dispatch])

    const { isLoading, addressList, error } = useSelector(state => state.address)

    const defaultAddressIndex = addressList.findIndex((shippingAddress) => shippingAddress.is_default);
    const defaultSelectedItem = defaultAddressIndex !== -1 ? defaultAddressIndex : 0;

    const [selectedItem, setSelectedItem] = useState(defaultSelectedItem);

    const [showAddressModal, setShowAddressModal] = useState(false);

    const handleShowNewAddressModal = () => setShowAddressModal(true);
    const handleCloseNewAddressModal = () => setShowAddressModal(false);

    const addressLabel = (shippingAddress) => {
        return (
            <div>
                <b>{shippingAddress.name}</b> - {shippingAddress.address.line1}, {shippingAddress.address.line2}, {shippingAddress.address.city}, {shippingAddress.address.state}, {shippingAddress.address.country}, {shippingAddress.address.pin_code}, {shippingAddress.alternate_phone}
            </div>
        )
    }

    const handleCheckboxClick = (index) => {
        setSelectedItem(index)
    }

    const handleRemoveShippingAddress = (shippingAddressId) => {
        dispatch(removeShippingAddress(shippingAddressId))
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
            : addressList?.map((address, index) => {
                return (
                    <div key={index}>
                        <Form.Check
                            inline
                            label={addressLabel(address)}
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
                                <Button 
                                    className="mt-2" 
                                    variant="outline-danger"
                                    onClick={handleRemoveShippingAddress}
                                >
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