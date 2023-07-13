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
} from '../constants/cartConstants';

import axiosInstance from '../utils/axios/axiosInterceptor';
import secureLocalStorage from 'react-secure-storage';

const storeCartItemsInStorage = (cartItems) => {
    secureLocalStorage.setItem('cartItems', JSON.stringify(cartItems));
}

const throwErrorResponse = (error) => {
    return error.response && error.response.data.message ? error.response.data.message : error.message
}

export const getCartItems = () => async (dispatch, getState) => {
    const cartUri = 'cart/'

    try {
        dispatch({ type: GET_CART_ITEMS_REQUEST })
        const { data } = await axiosInstance.get(cartUri)
        dispatch({ type: GET_CART_ITEMS_SUCCESS, payload: data })
        storeCartItemsInStorage(getState().cart.cartItems)
    } catch (error) {
        dispatch({
            type: GET_CART_ITEMS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const addToCart = (product, quantity = 1) => async (dispatch, getState) => {
    const cartUri = 'cart/'
    const cartData = { product: product, quantity: quantity }

    try {
        dispatch({ type: ADD_CART_ITEM_REQUEST })
        const { data } = await axiosInstance.post(cartUri, cartData)
        dispatch({ type: ADD_CART_ITEM_SUCCESS, payload: data })
        storeCartItemsInStorage(getState().cart.cartItems)
    } catch (error) {
        dispatch({
            type: ADD_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const updateCartQuantity = (product, quantity) => async (dispatch, getState) => {
    const cartByIdUri = `cart/${product.id}`
    const updateCartQuantityData = { quantity: quantity }

    try {
        dispatch({ type: UPDATE_CART_ITEM_REQUEST })
        const { data } = await axiosInstance.patch(cartByIdUri, updateCartQuantityData)
        dispatch({ type: UPDATE_CART_ITEM_SUCCESS, payload: data })
        storeCartItemsInStorage(getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: UPDATE_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const removeFromCart = (productId) => async (dispatch, getState) => {
    const cartByIdUri = `cart/${productId}`

    try {
        dispatch({ type: REMOVE_CART_ITEM_REQUEST })
        const { data } = await axiosInstance.delete(cartByIdUri)
        dispatch({ type: REMOVE_CART_ITEM_SUCCESS, payload: data })
        storeCartItemsInStorage(getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: REMOVE_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const emptyCart = () => async (dispatch, getState) => {
    const cartUri = 'cart/'

    try {
        dispatch({ type: EMPTY_CART_REQUEST })
        await axiosInstance.delete(cartUri)
        dispatch({ type: EMPTY_CART_SUCCESS })
        storeCartItemsInStorage(getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: EMPTY_CART_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}