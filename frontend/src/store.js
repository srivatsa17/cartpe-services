import { legacy_createStore as createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import { productListReducer, productDetailsReducer } from './reducers/productReducers';
import { cartReducer } from './reducers/cartReducers';
import secureLocalStorage from "react-secure-storage";

const loadState = () => {
    try {
        const serializedState = secureLocalStorage.getItem('state');
        if(serializedState === null) {
            return undefined;
        }
        return JSON.parse(serializedState);
    } catch (e) {
        return undefined;
    }
};

const saveState = (state) => {
    try {
        const serializedState = JSON.stringify(state);
        secureLocalStorage.setItem('state', serializedState);
    } catch (e) {
        return {}
    }
};

const persistedState = loadState();

const reducer = combineReducers({
    productList: productListReducer,
    productDetails: productDetailsReducer,
    cart: cartReducer
})

// const initialState = {}

const middleWare = [thunk]

const store = createStore(reducer, persistedState, composeWithDevTools(applyMiddleware(...middleWare)));

store.subscribe(() => {
    saveState(store.getState());
})

export default store