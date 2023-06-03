import { ADD_CART_ITEM } from "../constants/cartConstants";

export const cartReducer = (state = { cartItems: []}, action) => {
    switch(action.type) {
        case ADD_CART_ITEM:
            const productToAdd = action.payload;
            const isProductInCart = state.cartItems.some((cartItem) => cartItem.product.id === productToAdd.product.id)
            if(! isProductInCart) {
                return {
                    ...state,
                    cartItems: [...state.cartItems, productToAdd]
                }
            }
            break

        default:
            return state
    }
}