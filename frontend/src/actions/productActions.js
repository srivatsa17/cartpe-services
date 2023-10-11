import { CATEGORY_LIST, PRODUCT_LIST } from "../constants/localStorageConstants";
import {
    CATEGORY_LIST_FAIL,
    CATEGORY_LIST_REQUEST,
    CATEGORY_LIST_SUCCESS
} from "../constants/categoryConstants";
import {
    CATEGORY_SEARCH_FAIL,
    CATEGORY_SEARCH_REQUEST,
    CATEGORY_SEARCH_SUCCESS
} from "../constants/categorySearchConstants";
import {
    PRODUCT_DETAIL_FAIL,
    PRODUCT_DETAIL_REQUEST,
    PRODUCT_DETAIL_SUCCESS,
    PRODUCT_LIST_FAIL,
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS
} from "../constants/productConstants";

import axiosInstance from "../utils/axios/axiosInterceptor";
import getItemFromStorage from "../utils/localStorage/getItemFromStorage";
import saveItemInStorage from "../utils/localStorage/saveItemInStorage";
import throwErrorResponse from "../utils/errorResponse/throwErrorResponse";

export const getProducts = (searchedCategory) => async (dispatch, getState) => {
    const params = {
        params: {
            category : searchedCategory ?? ""
        }
    }

    try {
        dispatch({ type: PRODUCT_LIST_REQUEST })

        const productListFromStorage = getItemFromStorage(PRODUCT_LIST)
        /*
            If productList already exists in local storage and the searched category is same,
            don't make API call, rather send data stored in local storage itself. Thereby, reducing unnecessary
            hits to backend.
        */
        if(productListFromStorage && productListFromStorage.searchedCategory === searchedCategory) {
            dispatch({
                type: PRODUCT_LIST_SUCCESS,
                payload: {
                    products: productListFromStorage.products,
                    searchedCategory: searchedCategory
                }
            })
        } else {
            const { data } = await axiosInstance.get('products', params)
            dispatch({
                type: PRODUCT_LIST_SUCCESS,
                payload: {
                    products: data,
                    searchedCategory: searchedCategory
                }
            })
            saveItemInStorage(PRODUCT_LIST, getState().productList)
        }
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

export const getSearchedCategories = (searchedCategory) => async (dispatch) => {
    try {
        dispatch({ type: CATEGORY_SEARCH_REQUEST })
        const { data } = await axiosInstance.get(`products/categories/search?q=${searchedCategory}`)
        dispatch({ type: CATEGORY_SEARCH_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: CATEGORY_SEARCH_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const getCategoriesList = () => async (dispatch, getState) => {
    try {
        dispatch({ type: CATEGORY_LIST_REQUEST })
        const categoryListFromStorage = getItemFromStorage(CATEGORY_LIST)
        if(! categoryListFromStorage) {
            const { data } = await axiosInstance.get("products/categories")
            dispatch({ type: CATEGORY_LIST_SUCCESS, payload: data })
            saveItemInStorage(CATEGORY_LIST, getState().categoryList)
        } else {
            dispatch({
                type: CATEGORY_LIST_SUCCESS,
                payload: categoryListFromStorage.categories
            })
        }
    } catch(error) {
        dispatch({
            type: CATEGORY_LIST_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}