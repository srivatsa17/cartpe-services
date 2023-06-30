import 'bootstrap/dist/css/bootstrap.min.css';

import {
    CART_SCREEN,
    HOME_SCREEN,
    LOGIN_USER_SCREEN,
    PRODUCT_SCREEN,
    PRODUCT_SEARCH_SCREEN,
    REGISTER_USER_SCREEN,
    RESET_PASSWORD_CONFIRM_SCREEN,
    RESET_PASSWORD_SCREEN
} from '../src/constants/routes';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import AnonymousUserRoute from './AnonymousUserRoute';
import CartScreen from './screens/CartScreen';
import HomeScreen from './screens/HomeScreen';
import ProductScreen from './screens/ProductScreen';
import ProductSearchScreen from './screens/ProductSearchScreen';
import ProtectedUserRoute from './ProtectedUserRoute';
import React from 'react';
import UserLoginScreen from './screens/AuthService/UserLoginScreen';
import UserRegisterScreen from './screens/AuthService/UserRegisterScreen';
import UserResetPasswordConfirmScreen from './screens/AuthService/UserResetPasswordConfirmScreen';
import UserResetPasswordScreen from './screens/AuthService/UserResetPasswordScreen';

function App() {

    return (
        <Router>
            <Routes>
                <Route element={<AnonymousUserRoute />}>
                    <Route path={REGISTER_USER_SCREEN} element={<UserRegisterScreen />}/>
                    <Route path={LOGIN_USER_SCREEN} element={<UserLoginScreen />}/>
                    <Route path={RESET_PASSWORD_SCREEN} element={<UserResetPasswordScreen />} exact/>
                    <Route path={RESET_PASSWORD_CONFIRM_SCREEN} element={<UserResetPasswordConfirmScreen />} />
                </Route>
                <Route element={<ProtectedUserRoute />} >
                    <Route path={HOME_SCREEN} element={<HomeScreen />} exact />
                    <Route path={PRODUCT_SEARCH_SCREEN} element={<ProductSearchScreen />}/>
                    <Route path={PRODUCT_SCREEN} element={<ProductScreen />} />
                    <Route path={CART_SCREEN} element={<CartScreen />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
