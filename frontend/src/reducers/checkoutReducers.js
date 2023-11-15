import {
    ADD_ORDER_ITEMS_FAIL,
    ADD_ORDER_ITEMS_REQUEST,
    ADD_ORDER_ITEMS_SUCCESS,
    ADD_SHIPPING_ADDRESS_FAIL,
    ADD_SHIPPING_ADDRESS_REQUEST,
    ADD_SHIPPING_ADDRESS_SUCCESS,
    EDIT_SHIPPING_ADDRESS_FAIL,
    EDIT_SHIPPING_ADDRESS_REQUEST,
    EDIT_SHIPPING_ADDRESS_SUCCESS,
    GET_SHIPPING_ADDRESS_LIST_FAIL,
    GET_SHIPPING_ADDRESS_LIST_REQUEST,
    GET_SHIPPING_ADDRESS_LIST_SUCCESS,
    REMOVE_SHIPPING_ADDRESS_FAIL,
    REMOVE_SHIPPING_ADDRESS_REQUEST,
    REMOVE_SHIPPING_ADDRESS_SUCCESS,
    USE_SELECTED_SHIPPING_ADDRESS_FAIL,
    USE_SELECTED_SHIPPING_ADDRESS_REQUEST,
    USE_SELECTED_SHIPPING_ADDRESS_SUCCESS
} from "../constants/checkoutConstants";

export const addressReducer = (state = { addressList : [] }, action) => {
    const payload = action.payload;

    switch(action.type) {
        case GET_SHIPPING_ADDRESS_LIST_REQUEST:
        case ADD_SHIPPING_ADDRESS_REQUEST:
        case EDIT_SHIPPING_ADDRESS_REQUEST:
        case REMOVE_SHIPPING_ADDRESS_REQUEST:
            return { isLoading: true, ...state }

        case GET_SHIPPING_ADDRESS_LIST_SUCCESS:
            return { isLoading: false, addressList: payload }

        case ADD_SHIPPING_ADDRESS_SUCCESS:
        case EDIT_SHIPPING_ADDRESS_SUCCESS:
        case REMOVE_SHIPPING_ADDRESS_SUCCESS:
            return { isLoading: false, ...state }

        case GET_SHIPPING_ADDRESS_LIST_FAIL:
        case ADD_SHIPPING_ADDRESS_FAIL:
        case EDIT_SHIPPING_ADDRESS_FAIL:
        case REMOVE_SHIPPING_ADDRESS_FAIL:
            return { isLoading: false, error: payload, ...state }

        default:
            return state
    }
}

const initialCheckoutState = {
    shippingAddress : {},
    orderItems: [],
    amount: 0
}

export const checkoutReducer = (state = initialCheckoutState, action) => {
    const payload = action.payload;

    switch(action.type) {
        case USE_SELECTED_SHIPPING_ADDRESS_REQUEST:
        case ADD_ORDER_ITEMS_REQUEST:
            return { ...state, isLoading: true }

        case USE_SELECTED_SHIPPING_ADDRESS_SUCCESS:
            return { ...state, isLoading: false, shippingAddress: payload }
        case ADD_ORDER_ITEMS_SUCCESS:
            const extractedData = payload.orderItems?.map((item) => ({
                product: item.product.id, quantity: item.quantity
            }))
            return { ...state, isLoading: false, orderItems: extractedData, amount: payload.amount }

        case USE_SELECTED_SHIPPING_ADDRESS_FAIL:
        case ADD_ORDER_ITEMS_FAIL:
            return { ...state, isLoading: false, error: payload }

        default:
            return state
    }
}