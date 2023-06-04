import { ADD_CART_ITEM, UPDATE_CART_ITEM, REMOVE_CART_ITEM } from '../constants/cartConstants';

export const addToCart = (product, quantity = 1) => async (dispatch) => {
    dispatch({
        type: ADD_CART_ITEM,
        payload: { product: product, quantity: quantity }
    })
}

export const updateCartQuantity = (product, quantity) => async (dispatch) => {
    dispatch({
        type: UPDATE_CART_ITEM,
        payload: { product: product, quantity: quantity }
    })
}

export const removeFromCart = (productId) => async (dispatch) => {
    dispatch({
        type: REMOVE_CART_ITEM,
        payload: productId
    })
}