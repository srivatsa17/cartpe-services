import React, { useEffect, useState } from "react";
import {
    addShippingAddress,
    editShippingAddress,
    getShippingAddressList,
    removeShippingAddress,
    saveSelectedShippingAddress
} from "../../../actions/checkoutActions";
import { useDispatch, useSelector } from "react-redux";

import AddNewAddress from "./AddNewAddress";
import AddressList from "./AddressList";
import { Button } from "react-bootstrap";

function ShippingAddress({ handleActiveAccordionItem, selectedAddress, setSelectedAddress, defaultAddress }) {
    const dispatch = useDispatch()
    const { isLoading, addressList, error } = useSelector(state => state.address)

    useEffect(() => {
        dispatch(getShippingAddressList())
    }, [dispatch])

    const handleAddNewShippingAddress = (newAddressData) => {
        dispatch(addShippingAddress(newAddressData))
    }

    const handleEditShippingAddress = (formData, shippingAddressId) => {
        dispatch(editShippingAddress(formData, shippingAddressId))
    }

    const handleRemoveShippingAddress = (shippingAddressId) => {
        dispatch(removeShippingAddress(shippingAddressId))
    }

    const handleUseAddressClick = () => {
        dispatch(saveSelectedShippingAddress(selectedAddress))
        handleActiveAccordionItem("1")
    }

    const [showNewAddressModal, setShowNewAddressModal] = useState(false)

    return (
        <React.Fragment>
            <AddressList
                handleEditShippingAddress={handleEditShippingAddress}
                handleRemoveShippingAddress={handleRemoveShippingAddress}
                selectedAddress={selectedAddress}
                setSelectedAddress={setSelectedAddress}
                defaultAddress={defaultAddress}
            />
            <Button
                variant="outline-success"
                onClick={handleUseAddressClick}
                disabled={ addressList.length === 0 || isLoading || error }
            >
                Use this Address
            </Button>
            <Button
                className="mx-3"
                variant="outline-dark"
                onClick={() => setShowNewAddressModal(true)}
                disabled={ isLoading || error }
            >
                Add new Address
            </Button>
            <AddNewAddress
                showNewAddressModal={showNewAddressModal}
                setShowNewAddressModal={setShowNewAddressModal}
                handleAddNewShippingAddress={handleAddNewShippingAddress}
            />
        </React.Fragment>
    );
}

export default ShippingAddress;