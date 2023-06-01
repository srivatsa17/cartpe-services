import axios from 'axios';
import {
    PRODUCT_LIST_REQUEST, PRODUCT_LIST_SUCCESS, PRODUCT_LIST_FAIL,
    PRODUCT_DETAIL_REQUEST, PRODUCT_DETAIL_SUCCESS, PRODUCT_DETAIL_FAIL
} from "../constants/productConstants";


export const getProducts = (searchedCategory) => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_LIST_REQUEST })
        const { data } = await axios.get('https://mocki.io/v1/af7e74d1-7072-4804-ab1c-acd661956ea3', {
                                params: {
                                    category : searchedCategory ?? ""
                                }})
        dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.message
                    ? error.response.data.message
                    : error.message
        })
    }
}

export const getProductDetails = (id) => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_DETAIL_REQUEST })
        const { data } = await axios.get('https://mocki.io/v1/83398ea2-fbb9-4623-bd23-03d0eda2d28a')
        dispatch({ type: PRODUCT_DETAIL_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: PRODUCT_DETAIL_FAIL,
            payload: error.response && error.response.data.message
                    ? error.response.data.message
                    : error.message
        })
    }
}