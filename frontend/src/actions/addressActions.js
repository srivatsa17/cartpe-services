import {
    ADD_SHIPPING_ADDRESS_FAIL,
    ADD_SHIPPING_ADDRESS_REQUEST,
    ADD_SHIPPING_ADDRESS_SUCCESS,
    GET_SHIPPING_ADDRESS_LIST_FAIL,
    GET_SHIPPING_ADDRESS_LIST_REQUEST,
    GET_SHIPPING_ADDRESS_LIST_SUCCESS
} from "../constants/addressConstants";

import { ADDRESS_LIST } from "../constants/localStorageConstants";
import axiosInstance from "../utils/axios/axiosInterceptor";
import saveItemInStorage from '../utils/localStorage/saveItemInStorage';
import throwErrorResponse from '../utils/errorResponse/throwErrorResponse';

const shippingUri = "shipping/user-address";

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