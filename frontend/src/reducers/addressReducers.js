import {
    ADD_SHIPPING_ADDRESS_FAIL,
    ADD_SHIPPING_ADDRESS_REQUEST,
    ADD_SHIPPING_ADDRESS_SUCCESS,
    GET_SHIPPING_ADDRESS_LIST_FAIL,
    GET_SHIPPING_ADDRESS_LIST_REQUEST,
    GET_SHIPPING_ADDRESS_LIST_SUCCESS
} from "../constants/addressConstants";

export const addressReducer = (state = { addressList : [] }, action) => {
    const payload = action.payload;

    switch(action.type) {
        case GET_SHIPPING_ADDRESS_LIST_REQUEST:
        case ADD_SHIPPING_ADDRESS_REQUEST:
            return { isLoading: true, ...state }

        case GET_SHIPPING_ADDRESS_LIST_SUCCESS:
            return { isLoading: false, addressList: payload }
        case ADD_SHIPPING_ADDRESS_SUCCESS:
            return { isLoading: false, addressList: [...state.addressList, payload] }

        case GET_SHIPPING_ADDRESS_LIST_FAIL:
        case ADD_SHIPPING_ADDRESS_FAIL:
            return { isLoading: false, error: action.payload, ...state }

        default:
            return state
    }
}