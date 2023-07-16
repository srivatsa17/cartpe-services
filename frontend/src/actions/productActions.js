import {
    PRODUCT_DETAIL_FAIL,
    PRODUCT_DETAIL_REQUEST,
    PRODUCT_DETAIL_SUCCESS,
    PRODUCT_LIST_FAIL,
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS
} from "../constants/productConstants";

import axiosInstance from "../utils/axios/axiosInterceptor";
import throwErrorResponse from "../utils/errorResponse/throwErrorResponse";

export const getProducts = (searchedCategory) => async (dispatch) => {
    const params = {
        params: {
            category : searchedCategory ?? ""
        }
    }

    try {
        dispatch({ type: PRODUCT_LIST_REQUEST })
        const { data } = await axiosInstance.get('products', params)
        dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const getProductDetails = (id) => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_DETAIL_REQUEST })
        const { data } = await axiosInstance.get(`products/${id}`)
        dispatch({ type: PRODUCT_DETAIL_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: PRODUCT_DETAIL_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}