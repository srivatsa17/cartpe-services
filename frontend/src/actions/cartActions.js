import { ADD_CART_ITEM, EMPTY_CART, REMOVE_CART_ITEM, UPDATE_CART_ITEM } from '../constants/cartConstants';

import secureLocalStorage from 'react-secure-storage';

const storeCartItemsInStorage = (cartItems) => {
    secureLocalStorage.setItem('cartItems', JSON.stringify(cartItems));
}

export const addToCart = (product, quantity = 1) => async (dispatch, getState) => {
    dispatch({
        type: ADD_CART_ITEM,
        payload: { product: product, quantity: quantity }
    })
    storeCartItemsInStorage(getState().cart.cartItems)
}

export const updateCartQuantity = (product, quantity) => async (dispatch, getState) => {
    dispatch({
        type: UPDATE_CART_ITEM,
        payload: { product: product, quantity: quantity }
    })
    storeCartItemsInStorage(getState().cart.cartItems)
}

export const removeFromCart = (productId) => async (dispatch, getState) => {
    dispatch({
        type: REMOVE_CART_ITEM,
        payload: productId
    })
    storeCartItemsInStorage(getState().cart.cartItems)
}

export const emptyCart = () => async (dispatch, getState) => {
    dispatch({
        type: EMPTY_CART
    })
    storeCartItemsInStorage(getState().cart.cartItems)
}