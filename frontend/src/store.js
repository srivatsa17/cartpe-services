import { applyMiddleware, combineReducers, legacy_createStore as createStore } from 'redux';
import { productDetailsReducer, productListReducer } from './reducers/productReducers';

import { cartReducer } from './reducers/cartReducers';
import { composeWithDevTools } from 'redux-devtools-extension';
import secureLocalStorage from "react-secure-storage";
import thunk from 'redux-thunk';
import { userLoginReducer } from './reducers/authReducers';

const cartItemsFromStorage = secureLocalStorage.getItem('cartItems') ? 
                            JSON.parse(secureLocalStorage.getItem('cartItems')) : []

const userDetailsFromStorage = secureLocalStorage.getItem('userDetails') ? 
                            JSON.parse(secureLocalStorage.getItem('userDetails')) : {}

const reducer = combineReducers({
    productList: productListReducer,
    productDetails: productDetailsReducer,
    cart: cartReducer,
    userDetails: userLoginReducer,
})

const persistedState = {
    cart: {
        cartItems: cartItemsFromStorage,
    },
    userDetails: {
        isLoggedIn: userDetailsFromStorage.isLoggedIn ?? false
    }
}

const middleWare = [thunk]

const store = createStore(reducer, persistedState, composeWithDevTools(applyMiddleware(...middleWare)));

export default store