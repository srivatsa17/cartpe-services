import {
    ADDRESS_LIST,
    CART_ITEMS,
    CATEGORY_LIST,
    PRODUCT_LIST,
    USER_LOGIN_DETAILS,
    USER_REGISTER_DETAILS
} from './constants/localStorageConstants';
import { addressReducer, checkoutReducer } from './reducers/checkoutReducers';
import { applyMiddleware, combineReducers, legacy_createStore as createStore } from 'redux';
import { categoryListReducer, categorySearchReducer, productDetailsReducer, productListReducer } from './reducers/productReducers';
import { userLoginReducer, userRegisterReducer } from './reducers/authReducers';

import { cartReducer } from './reducers/cartReducers';
import { composeWithDevTools } from 'redux-devtools-extension';
import getItemFromStorage from './utils/localStorage/getItemFromStorage';
import thunk from 'redux-thunk';

const productListFromStorage = getItemFromStorage(PRODUCT_LIST) ?? {}
const cartItemsFromStorage = getItemFromStorage(CART_ITEMS) ?? []
const addressListFromStorage = getItemFromStorage(ADDRESS_LIST) ?? []
const userLoginDetailsFromStorage = getItemFromStorage(USER_LOGIN_DETAILS) ?? {}
const userRegisterDetailsFromStorage = getItemFromStorage(USER_REGISTER_DETAILS) ?? {}
const categoryListFromStorage = getItemFromStorage(CATEGORY_LIST) ?? {}

const reducer = combineReducers({
    productList: productListReducer,
    productDetails: productDetailsReducer,
    categoryList: categoryListReducer,
    searchedCategories: categorySearchReducer,
    cart: cartReducer,
    address: addressReducer,
    checkoutInfo: checkoutReducer,
    userLoginDetails: userLoginReducer,
    userRegisterDetails: userRegisterReducer,
})

const persistedState = {
    productList: {
        products: productListFromStorage.products ?? [],
        searchedCategory: productListFromStorage.searchedCategory
    },
    categoryList: categoryListFromStorage,
    cart: {
        cartItems: cartItemsFromStorage,
    },
    address: {
        addressList: addressListFromStorage,
    },
    userLoginDetails: {
        isLoggedIn: userLoginDetailsFromStorage.isLoggedIn || false
    },
    userRegisterDetails: {
        isUserRegistered:   userLoginDetailsFromStorage.isLoggedIn ||
                            userRegisterDetailsFromStorage.isUserRegistered ||
                            false,
        isUserVerified: userLoginDetailsFromStorage.isLoggedIn ||
                        userRegisterDetailsFromStorage.isUserVerified ||
                        false,
    }
}

const middleWare = [thunk]

const store = createStore(reducer, persistedState, composeWithDevTools(applyMiddleware(...middleWare)));

export default store