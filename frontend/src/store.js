import { applyMiddleware, combineReducers, legacy_createStore as createStore } from 'redux';
import { productDetailsReducer, productListReducer } from './reducers/productReducers';
import { userLoginReducer, userRegisterReducer } from './reducers/authReducers';

import { cartReducer } from './reducers/cartReducers';
import { composeWithDevTools } from 'redux-devtools-extension';
import secureLocalStorage from "react-secure-storage";
import thunk from 'redux-thunk';

const cartItemsFromStorage = secureLocalStorage.getItem('cartItems') ? 
                            JSON.parse(secureLocalStorage.getItem('cartItems')) : []

const userLoginDetailsFromStorage = secureLocalStorage.getItem('userLoginDetails') ? 
                            JSON.parse(secureLocalStorage.getItem('userLoginDetails')) : {}

const userRegisterDetailsFromStorage = secureLocalStorage.getItem('userRegisterDetails') ?
                            JSON.parse(secureLocalStorage.getItem('userRegisterDetails')) : {}

const reducer = combineReducers({
    productList: productListReducer,
    productDetails: productDetailsReducer,
    cart: cartReducer,
    userLoginDetails: userLoginReducer,
    userRegisterDetails: userRegisterReducer,
})

const persistedState = {
    cart: {
        cartItems: cartItemsFromStorage,
    },
    userLoginDetails: {
        isLoggedIn: userLoginDetailsFromStorage.isLoggedIn ?? false
    },
    userRegisterDetails: {
        isUserRegistered: userRegisterDetailsFromStorage.isUserRegistered ?? false,
        isUserVerified: userRegisterDetailsFromStorage.isUserVerified ?? false,
    }
}

const middleWare = [thunk]

const store = createStore(reducer, persistedState, composeWithDevTools(applyMiddleware(...middleWare)));

export default store