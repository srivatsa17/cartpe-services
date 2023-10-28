import {
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
    REMOVE_SHIPPING_ADDRESS_SUCCESS
} from "../constants/addressConstants";

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
        const { data } = await axiosInstance.post(shippingUri, shippingAddress)
        dispatch({
            type: ADD_SHIPPING_ADDRESS_SUCCESS,
            payload: data
        })
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
        const { data } = await axiosInstance.put(shippingByIdUri(shippingAddressId), shippingAddress)
        dispatch({
            type: EDIT_SHIPPING_ADDRESS_SUCCESS,
            payload: data
        })
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
        dispatch({
            type: REMOVE_SHIPPING_ADDRESS_SUCCESS,
            payload: shippingAddressId
        })
        saveItemInStorage(ADDRESS_LIST, getState().address.addressList)
    } catch (error) {
        dispatch({
            type: REMOVE_SHIPPING_ADDRESS_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}