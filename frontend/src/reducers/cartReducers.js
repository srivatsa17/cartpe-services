import {
    ADD_CART_ITEM_SUCCESS,
    EMPTY_CART_SUCCESS,
    GET_CART_ITEMS_SUCCESS,
    REMOVE_CART_ITEM_SUCCESS,
    UPDATE_CART_ITEM_SUCCESS
} from "../constants/cartConstants";

export const cartReducer = (state = { cartItems: [] }, action) => {
    const payload = action.payload;

    switch(action.type) {
        case GET_CART_ITEMS_SUCCESS:
            return payload

        case ADD_CART_ITEM_SUCCESS:
            const isProductInCart = state.cartItems.some((cartItem) => cartItem.product.id === payload.product.id)
            if(!isProductInCart) {
                return payload
            }
            break

        case UPDATE_CART_ITEM_SUCCESS:
            return payload

        case REMOVE_CART_ITEM_SUCCESS:
            return payload

        case EMPTY_CART_SUCCESS:
            return {
                ...state,
                cartItems: []
            }

        default:
            return state
    }
}