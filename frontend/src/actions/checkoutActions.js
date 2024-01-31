import {
    ADD_ORDER_ITEMS_FAIL,
    ADD_ORDER_ITEMS_REQUEST,
    ADD_ORDER_ITEMS_SUCCESS,
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
    REMOVE_SHIPPING_ADDRESS_SUCCESS,
    USE_SELECTED_SHIPPING_ADDRESS_FAIL,
    USE_SELECTED_SHIPPING_ADDRESS_REQUEST,
    USE_SELECTED_SHIPPING_ADDRESS_SUCCESS
} from "../constants/checkoutConstants";

import { ADDRESS_LIST } from "../constants/localStorageConstants";
import axiosInstance from "../utils/axios/axiosInterceptor";
import saveItemInStorage from '../utils/localStorage/saveItemInStorage';
import throwErrorResponse from '../utils/errorResponse/throwErrorResponse';

const shippingUri = "shipping/user-address";
const shippingByIdUri = (userAddressId) => {
    return `shipping/user-address/${userAddressId}`;
}

export const getShippingAddressList = () => async (dispatch, getState) => {
    try {
        dispatch({ type: GET_SHIPPING_ADDRESS_LIST_REQUEST })
        const { data } = await axiosInstance.get(shippingUri)
        dispatch({
            type: GET_SHIPPING_ADDRESS_LIST_SUCCESS,
            payload: data
        })
        saveItemInStorage(ADDRESS_LIST, getState().address.addressList)
    } catch (error) {
        dispatch({
            type: GET_SHIPPING_ADDRESS_LIST_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const addShippingAddress = (shippingAddress) => async (dispatch, getState) => {
    try {
        dispatch({ type: ADD_SHIPPING_ADDRESS_REQUEST })
        await axiosInstance.post(shippingUri, shippingAddress)
        dispatch(getShippingAddressList())
        dispatch({ type: ADD_SHIPPING_ADDRESS_SUCCESS })
        saveItemInStorage(ADDRESS_LIST, getState().address.addressList)
    } catch (error) {
        dispatch({
            type: ADD_SHIPPING_ADDRESS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const editShippingAddress = (shippingAddress, shippingAddressId) => async (dispatch, getState) => {
    try {
        dispatch({ type: EDIT_SHIPPING_ADDRESS_REQUEST })
        await axiosInstance.put(shippingByIdUri(shippingAddressId), shippingAddress)
        dispatch(getShippingAddressList())
        dispatch({ type: EDIT_SHIPPING_ADDRESS_SUCCESS })
        saveItemInStorage(ADDRESS_LIST, getState().address.addressList)
    } catch (error) {
        dispatch({
            type: EDIT_SHIPPING_ADDRESS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const removeShippingAddress = (shippingAddressId) => async (dispatch, getState) => {
    try {
        dispatch({ type: REMOVE_SHIPPING_ADDRESS_REQUEST })
        await axiosInstance.delete(shippingByIdUri(shippingAddressId))
        dispatch(getShippingAddressList())
        dispatch({ type: REMOVE_SHIPPING_ADDRESS_SUCCESS })
        saveItemInStorage(ADDRESS_LIST, getState().address.addressList)
    } catch (error) {
        dispatch({
            type: REMOVE_SHIPPING_ADDRESS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const saveSelectedShippingAddress = (shippingAddress) => async (dispatch, getState) => {
    try {
        dispatch({ type: USE_SELECTED_SHIPPING_ADDRESS_REQUEST })
        dispatch({ type: USE_SELECTED_SHIPPING_ADDRESS_SUCCESS, payload: shippingAddress })
    } catch (error) {
        dispatch({
            type: USE_SELECTED_SHIPPING_ADDRESS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const addOrderItems = (cartItems, amount) => async (dispatch, getState) => {
    try {
        dispatch({ type: ADD_ORDER_ITEMS_REQUEST })
        dispatch({
            type: ADD_ORDER_ITEMS_SUCCESS,
            payload: {
                orderItems: cartItems,
                amount: amount
            }
        })
    } catch (error) {
        dispatch({
            type: ADD_ORDER_ITEMS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}