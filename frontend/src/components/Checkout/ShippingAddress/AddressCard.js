import "../../../css/Checkout/AddressCard.css";

import { Button, Card } from 'react-bootstrap';

import { FaRupeeSign } from "react-icons/fa";
import React from 'react';
import { useSelector } from "react-redux/es/hooks/useSelector";

function AddressCard({ handleActiveAccordionItem, cartItems, nextAccordionItemEventKey }) {

    const totalSellingPrice = cartItems.reduce(
        (sum, cartItem) => sum + cartItem.quantity * cartItem.product.selling_price, 0
    ).toFixed(2)

    const { isLoading, addressList, error } = useSelector(state => state.address)

    return (
        <>
            <Card className="address-card-container">
                <Card.Body>
                    <Button
                        variant='success'
                        className='w-100'
                        onClick={() => handleActiveAccordionItem(nextAccordionItemEventKey)}
                        disabled={ addressList.length === 0 || isLoading || error }
                    >
                        Use this address
                    </Button>
                    <div id="address-note">
                        Choose an address to continue checking out.
                        You will still have a chance to review and edit your order before it is final.
                    </div>
                    <hr />
                    <div className="checkout-order-summary-info">
                        Order Summary
                        <div id="items-info-placeholder">
                            <div>Items</div>
                            <div>---</div>
                        </div>
                        <div id="delivery-info-placeholder">
                            <div>Delivery</div>
                            <div>---</div>
                        </div>
                    </div>
                    <hr />
                    <div className="checkout-order-total-info">
                        <b>Order Total:</b>
                        <b>
                            <FaRupeeSign id="rupee-icon" size={18}/>{totalSellingPrice}
                        </b>
                    </div>
                    <hr />
                </Card.Body>
            </Card>
        </>
    )
}

export default AddressCard;