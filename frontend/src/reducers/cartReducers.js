import { ADD_CART_ITEM, EMPTY_CART, REMOVE_CART_ITEM, UPDATE_CART_ITEM } from "../constants/cartConstants";

export const cartReducer = (state = { cartItems: []}, action) => {
    const payload = action.payload;

    switch(action.type) {
        case ADD_CART_ITEM:
            const isProductInCart = state.cartItems.some((cartItem) => cartItem.product.id === payload.product.id)
            if(!isProductInCart) {
                return {
                    ...state,
                    cartItems: [...state.cartItems, payload]
                }
            }
            break

        case UPDATE_CART_ITEM:
            return {
                ...state,
                cartItems: state.cartItems.map((cartItem) => {
                    if (cartItem.product.id === payload.product.id) {
                        return {
                            ...cartItem,
                            quantity: payload.quantity
                        };
                    }
                    return cartItem;
                })
            }

        case REMOVE_CART_ITEM:
            return {
                ...state,
                cartItems: state.cartItems.filter((cartItem) => cartItem.product.id !== payload)
            }

        case EMPTY_CART:
            return {
                ...state,
                cartItems: []
            }

        default:
            return state
    }
}