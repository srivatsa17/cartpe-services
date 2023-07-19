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

import { CART_ITEMS } from '../constants/localStorageConstants';
import axiosInstance from '../utils/axios/axiosInterceptor';
import saveItemInStorage from '../utils/localStorage/saveItemInStorage';
import throwErrorResponse from '../utils/errorResponse/throwErrorResponse';

const cartUri = 'cart/';
const cartByIdUri = (productId) => {
    return `cart/${productId}`
}

export const getCartItems = () => async (dispatch, getState) => {
    try {
        dispatch({ type: GET_CART_ITEMS_REQUEST })
        const { data } = await axiosInstance.get(cartUri)
        dispatch({ type: GET_CART_ITEMS_SUCCESS, payload: data })
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems)
    } catch (error) {
        dispatch({
            type: GET_CART_ITEMS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const addToCart = (product, quantity = 1) => async (dispatch, getState) => {
    const cartData = { product: product, quantity: quantity }

    try {
        dispatch({ type: ADD_CART_ITEM_REQUEST })
        await axiosInstance.post(cartUri, cartData)
        dispatch({
            type: ADD_CART_ITEM_SUCCESS,
            payload: cartData
        })
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems)
    } catch (error) {
        dispatch({
            type: ADD_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const updateCartQuantity = (product, quantity) => async (dispatch, getState) => {
    const updateCartQuantityData = { quantity: quantity }

    try {
        dispatch({ type: UPDATE_CART_ITEM_REQUEST })
        const { data } = await axiosInstance.patch(cartByIdUri(product.id), updateCartQuantityData)
        dispatch({ type: UPDATE_CART_ITEM_SUCCESS, payload: data })
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: UPDATE_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const removeFromCart = (productId) => async (dispatch, getState) => {
    try {
        dispatch({ type: REMOVE_CART_ITEM_REQUEST })
        const { data } = await axiosInstance.delete(cartByIdUri(productId))
        dispatch({ type: REMOVE_CART_ITEM_SUCCESS, payload: data })
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: REMOVE_CART_ITEM_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const emptyCart = () => async (dispatch, getState) => {
    try {
        dispatch({ type: EMPTY_CART_REQUEST })
        await axiosInstance.delete(cartUri)
        dispatch({ type: EMPTY_CART_SUCCESS })
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems)
    } catch(error) {
        dispatch({
            type: EMPTY_CART_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}