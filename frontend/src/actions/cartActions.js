import { ADD_CART_ITEM } from '../constants/cartConstants';

export const addToCart = (product, quantity = 1) => async (dispatch) => {
    dispatch({
        type: ADD_CART_ITEM,
        payload: { product: product, quantity: quantity }
    })
}