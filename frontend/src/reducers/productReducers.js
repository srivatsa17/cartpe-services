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

export const productListReducer = (state = { products: []}, action) => {
    switch(action.type) {
        case PRODUCT_LIST_REQUEST:
            return { isLoading: true, products: [] }
        case PRODUCT_LIST_SUCCESS:
            return { isLoading: false, products: action.payload.products, searchedCategory: action.payload.searchedCategory }
        case PRODUCT_LIST_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}

export const productDetailsReducer = (state = { product : {}}, action) => {
    switch(action.type) {
        case PRODUCT_DETAIL_REQUEST:
            return { isLoading: true, ...state }
        case PRODUCT_DETAIL_SUCCESS:
            return { isLoading: false, product: action.payload }
        case PRODUCT_DETAIL_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}

export const categorySearchReducer = (state = { categories : [] }, action) => {
    switch(action.type) {
        case CATEGORY_SEARCH_REQUEST:
            return { isLoading: true, ...state }
        case CATEGORY_SEARCH_SUCCESS:
            return { isLoading: false, categories: action.payload }
        case CATEGORY_SEARCH_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}

export const categoryListReducer = (state = { categories : [] }, action) => {
    switch(action.type) {
        case CATEGORY_LIST_REQUEST:
            return { isLoading: true, ...state }
        case CATEGORY_LIST_SUCCESS:
            return { isLoading: false, categories: action.payload }
        case CATEGORY_LIST_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}