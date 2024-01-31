import { ORDER_CONFIRMED_SCREEN, ORDER_FAILED_SCREEN, ORDER_PAYMENT_FAILED_SCREEN } from "../../../constants/routes";

import { CARTPE_LOGO_BLACK } from "../../../constants/imageConstants";
import { LATEST_ORDER } from "../../../constants/localStorageConstants";
import axiosInstance from "../../../utils/axios/axiosInterceptor";
import saveItemInStorage from "../../../utils/localStorage/saveItemInStorage";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useRazorpay from "../../../utils/razorpay/react-razorpay";
import { useSelector } from "react-redux";

const createOrder = async (razorpayOrderDetails, shippingAddress, orderItems, amount) => {
    const orderApi = "orders/";
    const orderData = {
        user_address: shippingAddress.id,
        amount: amount,
        order_items: orderItems,
        razorpay_order_id: razorpayOrderDetails.razorpay_order_id,
        razorpay_payment_id: razorpayOrderDetails.razorpay_payment_id,
        razorpay_signature: razorpayOrderDetails.razorpay_signature
    }
    const { data } = await axiosInstance.post(orderApi, orderData)
    return data
}

const displayRazorPayCheckoutForm = (Razorpay, navigate, shippingAddress, orderItems, amount) => {
    const razorpayOrderApi = "orders/razorpay";
    const razorpayOrderData = { amount: amount }

    axiosInstance.post(razorpayOrderApi, razorpayOrderData)
    .then((response) => {
        const razorpayOrder = response.data

        const options = {
            key: "rzp_test_q6yYG9cg3J2Ozn",
            amount: amount * 100,
            name: "CartPe",
            description: "Test Transaction",
            image: CARTPE_LOGO_BLACK,
            order_id: razorpayOrder.id,
            handler: function (response) {
                createOrder(response, shippingAddress, orderItems, amount)
                .then((order) => {
                    saveItemInStorage(LATEST_ORDER, order);
                    navigate(`${ORDER_CONFIRMED_SCREEN}?orderId=${order.id}`)
                })
            },
            prefill: {
                name: "Piyush Garg",
                email: "youremail@example.com",
                contact: "9999999999",
            },
            theme: {
                color: "#004493",
            }
        };

        const rzp1 = new Razorpay(options);

        rzp1.on("payment.failed", function (response) {
            const orderIdQueryParam = `orderId=${response.error.metadata.order_id}`;
            const paymentIdQueryParam = `paymentId=${response.error.metadata.payment_id}`;
            
            navigate(
                `${ORDER_PAYMENT_FAILED_SCREEN}?${orderIdQueryParam}&${paymentIdQueryParam}`, {
                    state: {
                        "paymentError": response.error.description
                    }
                }
            )
            // alert(response.error.code);
            // alert(response.error.description);
            // alert(response.error.source);
            // alert(response.error.step);
            // alert(response.error.reason);
            // alert(response.error.metadata.order_id);
            // alert(response.error.metadata.payment_id);
        });

        rzp1.open();
    })
    .catch(() => {
        navigate(`${ORDER_FAILED_SCREEN}`)
    })
}

function DisplayRazorPayCard() {
    const { shippingAddress, orderItems, amount } = useSelector(state => state.checkoutInfo)
    const [Razorpay] = useRazorpay()
    const navigate = useNavigate()

    useEffect(() => {
        displayRazorPayCheckoutForm(Razorpay, navigate, shippingAddress, orderItems, amount);
    }, [Razorpay, navigate, shippingAddress, orderItems, amount]);

    return null;
}

export default DisplayRazorPayCard;