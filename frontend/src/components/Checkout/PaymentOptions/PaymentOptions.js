import "../../../css/Checkout/PaymentOptions.css";

import { Button, Form } from "react-bootstrap";

import React from "react";
import { SiRazorpay } from "react-icons/si";

function PaymentOptions({ handleActiveAccordionItem, isTermsAndConditionsChecked, setIsTermsAndConditionsChecked }) {

    const termsAndConditionsLabel = () => {
        return (
            <div>
                Please agree to the <a href="##">terms and conditions</a> of <b>CartPe</b> to place the order.
            </div>
        )
    }

    const handlePayment = () => {
        // Trigger razorpay's api's
        handleActiveAccordionItem("3");
    }

    return (
        <div className="payment-options">
            <Form>
                <Form.Check
                    type="checkbox"
                    checked={isTermsAndConditionsChecked}
                    onChange={() => setIsTermsAndConditionsChecked(!isTermsAndConditionsChecked)}
                    label={termsAndConditionsLabel()}
                />
            </Form>
            {
                isTermsAndConditionsChecked &&
                <div className="mt-3">
                    You will be redirected to <SiRazorpay /> Razorpay's payment gateway to complete the order payment.
                </div>
            }
            <div className="mt-3">
                <Button
                    variant="success"
                    onClick={handlePayment}
                    disabled={isTermsAndConditionsChecked === false}
                >
                    Pay & Order
                </Button>
                <Button
                    variant="warning"
                    className="mx-2"
                    onClick={() => handleActiveAccordionItem("1")}
                >
                    Go Back & Review Cart Items
                </Button>
            </div>
        </div>
    )
}

export default PaymentOptions;