import {
    ADD_CART_ITEM_FAIL,
    ADD_CART_ITEM_REQUEST,
    ADD_CART_ITEM_SUCCESS,
    EMPTY_CART_FAIL,
    EMPTY_CART_REQUEST,
    EMPTY_CART_SUCCESS,
    GET_CART_ITEMS_FAIL,
    GET_CART_ITEMS_REQUEST,
    GET_CART_ITEMS_SUCCESS,
    REMOVE_CART_ITEM_FAIL,
    REMOVE_CART_ITEM_REQUEST,
    REMOVE_CART_ITEM_SUCCESS,
    UPDATE_CART_ITEM_FAIL,
    UPDATE_CART_ITEM_REQUEST,
    UPDATE_CART_ITEM_SUCCESS
} from "../constants/cartConstants";

export const cartReducer = (state = { cartItems: [] }, action) => {
    const payload = action.payload;

    switch(action.type) {
        case GET_CART_ITEMS_REQUEST:
        case ADD_CART_ITEM_REQUEST:
        case UPDATE_CART_ITEM_REQUEST:
        case REMOVE_CART_ITEM_REQUEST:
        case EMPTY_CART_REQUEST:
            return { ...state, isLoading : true }

        case GET_CART_ITEMS_SUCCESS:
        case UPDATE_CART_ITEM_SUCCESS:
        case REMOVE_CART_ITEM_SUCCESS:
            return { isLoading: false, cartItems: payload.cartItems }

        case ADD_CART_ITEM_SUCCESS:
            const isProductInCart = state.cartItems.some((cartItem) => cartItem.product.id === payload.product.id)
            if(!isProductInCart) {
                return {
                    ...state,
                    cartItems: [...state.cartItems, payload]
                }
            }
            break

        case EMPTY_CART_SUCCESS:
            return { isLoading: false, cartItems: [] }

        case GET_CART_ITEMS_FAIL:
        case ADD_CART_ITEM_FAIL:
        case UPDATE_CART_ITEM_FAIL:
        case REMOVE_CART_ITEM_FAIL:
        case EMPTY_CART_FAIL:
            return { ...state, isLoading: false, error: payload }

        default:
            return state
    }
}