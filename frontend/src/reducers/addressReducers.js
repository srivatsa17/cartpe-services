import {
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
    REMOVE_SHIPPING_ADDRESS_SUCCESS
} from "../constants/addressConstants";

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
            return { isLoading: false, addressList: [...state.addressList, payload] }
        case EDIT_SHIPPING_ADDRESS_SUCCESS:
            const updatedAddressIndex = state.addressList.findIndex(
                (address) => address.id === payload.id
            );

            // If the address is found, remove it from the list and add the updated one.
            if (updatedAddressIndex !== -1) {
                const updatedAddressList = state.addressList.filter(
                    (address) => address.id !== payload.id
                );
                return {
                    isLoading: false,
                    addressList: [...updatedAddressList, payload],
                }
            } else {
                // If the address is not found, simply add the updated one.
                return {
                    isLoading: false,
                    addressList: [...state.addressList, payload],
                };
            }
        case REMOVE_SHIPPING_ADDRESS_SUCCESS:
            const updatedAddressList = state.addressList.filter(
                (address) => address.id !== payload
            );
            return { ...state, isLoading: false, addressList: updatedAddressList }

        case GET_SHIPPING_ADDRESS_LIST_FAIL:
        case ADD_SHIPPING_ADDRESS_FAIL:
        case EDIT_SHIPPING_ADDRESS_FAIL:
        case REMOVE_SHIPPING_ADDRESS_FAIL:
            return { isLoading: false, error: action.payload, ...state }

        default:
            return state
    }
}