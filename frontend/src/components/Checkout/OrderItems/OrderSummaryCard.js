import "../../../css/Checkout/OrderSummaryCard.css";

import { Button, Card } from 'react-bootstrap';

import { FaRupeeSign } from "react-icons/fa";
import React from 'react';

function OrderSummaryCard({ 
    handleActiveAccordionItem, 
    cartItems, 
    nextAccordionItemEventKey, 
    isTermsAndConditionsChecked 
}) {
    const totalCartItemsQuantity = cartItems.length;
    const totalMRP = cartItems.reduce((sum, cartItem) => sum + cartItem.quantity * cartItem.product.price, 0).toFixed(2);
    const minusSign = "-";
    const totalDiscountPrice = cartItems.reduce(
        (sum, cartItem) => sum + cartItem.quantity * cartItem.product.discounted_price, 0
    ).toFixed(2)
    const convenienceFee = 20;
    const totalSellingPrice =
        Number(
            cartItems.reduce(
                (sum, cartItem) => sum + cartItem.quantity * cartItem.product.selling_price, 0
            ).toFixed(2)
        ) + Number(convenienceFee);
    const roundOffPrice = (Math.round(totalSellingPrice) - totalSellingPrice).toFixed(2);
    const finalAmount = Math.round(totalSellingPrice);
    const savingsAmount = Math.round(totalMRP - finalAmount);
    const savingsPercent = ((savingsAmount / totalMRP).toFixed(2) * 100).toFixed(2);

    return (
        <>
            <Card className="checkout-order-summary-card-container">
                <Card.Body>
                    <div className="checkout-order-summary-card-heading">
                        Order Summary ({totalCartItemsQuantity} items)
                    </div>
                    <hr />

                    <div className="checkout-order-summary-mrp">
                        <div>Total MRP</div>
                        <div>
                            <FaRupeeSign id="rupee-icon"/>{totalMRP}
                        </div>
                    </div>

                    <div className="checkout-order-summary-discount-price">
                        <div>Discount on MRP</div>
                        <div className="cart-subtotal-discounted-price">
                            {minusSign}<FaRupeeSign id="rupee-icon"/>{totalDiscountPrice}
                        </div>
                    </div>

                    <div className="checkout-order-summary-convenience-fee">
                        <div>Convenience Fee</div>
                        <div>
                            <FaRupeeSign id="rupee-icon"/>{convenienceFee}
                        </div>
                    </div>

                    <div className="checkout-order-summary-round-off">
                        <div>Round Off</div>
                        <div>
                            { finalAmount < totalSellingPrice ? minusSign : "" }
                            <FaRupeeSign id="rupee-icon"/>{roundOffPrice}
                        </div>
                    </div>

                    <hr />
                    <div className="checkout-order-summary-total-amount">
                        <div>Total Amount</div>
                        <div>
                            <FaRupeeSign id="rupee-icon" size={18}/>{finalAmount}
                        </div>
                    </div>

                    <div className="checkout-order-summary-savings">
                        Your savings: <FaRupeeSign id="rupee-icon"/>{savingsAmount} ({savingsPercent}%)
                    </div>

                    <hr />

                    <Button
                        variant='dark' className='w-100'
                        onClick={() => handleActiveAccordionItem(nextAccordionItemEventKey)}
                        disabled={isTermsAndConditionsChecked === false}
                    >
                        Place order
                    </Button>
                </Card.Body>
            </Card>
        </>
    )
}

export default OrderSummaryCard;