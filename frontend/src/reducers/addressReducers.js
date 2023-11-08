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
        case EDIT_SHIPPING_ADDRESS_SUCCESS:
        case REMOVE_SHIPPING_ADDRESS_SUCCESS:
            return { isLoading: false, ...state }
            
        case GET_SHIPPING_ADDRESS_LIST_FAIL:
        case ADD_SHIPPING_ADDRESS_FAIL:
        case EDIT_SHIPPING_ADDRESS_FAIL:
        case REMOVE_SHIPPING_ADDRESS_FAIL:
            return { isLoading: false, error: action.payload, ...state }

        default:
            return state
    }
}