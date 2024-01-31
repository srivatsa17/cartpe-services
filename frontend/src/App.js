import 'bootstrap/dist/css/bootstrap.min.css';

import {
    CART_SCREEN,
    CHECKOUT_SCREEN,
    HOME_SCREEN,
    LOGIN_USER_SCREEN,
    ORDER_CONFIRMED_SCREEN,
    ORDER_FAILED_SCREEN,
    ORDER_PAYMENT_FAILED_SCREEN,
    PRODUCT_SCREEN,
    PRODUCT_SEARCH_SCREEN,
    REGISTER_USER_SCREEN,
    RESET_PASSWORD_CONFIRM_SCREEN,
    RESET_PASSWORD_SCREEN,
    VERIFY_USER_EMAIL_SCREEN
} from './constants/routes';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import AnonymousUserRoute from './routing/AnonymousUserRoute';
import CartScreen from './screens/CartScreen';
import CheckoutScreen from './screens/CheckoutScreen';
import HomeScreen from './screens/HomeScreen';
import OrderConfirmedScreen from './screens/OrderStatus/OrderConfirmedScreen';
import OrderFailedScreen from './screens/OrderStatus/OrderFailedScreen';
import OrderPaymentFailedScreen from './screens/OrderStatus/OrderPaymentFailedScreen';
import ProductScreen from './screens/ProductScreen';
import ProductSearchScreen from './screens/ProductSearchScreen';
import ProtectedUserRoute from './routing/ProtectedUserRoute';
import React from 'react';
import UserLoginScreen from './screens/AuthService/UserLoginScreen';
import UserRegisterScreen from './screens/AuthService/UserRegisterScreen';
import UserResetPasswordConfirmScreen from './screens/AuthService/UserResetPasswordConfirmScreen';
import UserResetPasswordScreen from './screens/AuthService/UserResetPasswordScreen';
import UserVerifyEmailScreen from './screens/AuthService/UserVerifyEmailScreen';

function App() {

    return (
        <Router>
            <Routes>
                <Route element={<AnonymousUserRoute />}>
                    <Route path={REGISTER_USER_SCREEN} element={<UserRegisterScreen />}/>
                    <Route path={VERIFY_USER_EMAIL_SCREEN} element={<UserVerifyEmailScreen />}/>
                    <Route path={LOGIN_USER_SCREEN} element={<UserLoginScreen />}/>
                    <Route path={RESET_PASSWORD_SCREEN} element={<UserResetPasswordScreen />} exact/>
                    <Route path={RESET_PASSWORD_CONFIRM_SCREEN} element={<UserResetPasswordConfirmScreen />} />
                </Route>
                <Route element={<ProtectedUserRoute />} >
                    <Route path={HOME_SCREEN} element={<HomeScreen />} exact />
                    <Route path={PRODUCT_SEARCH_SCREEN} element={<ProductSearchScreen />}/>
                    <Route path={PRODUCT_SCREEN} element={<ProductScreen />} />
                    <Route path={CART_SCREEN} element={<CartScreen />} />
                    <Route path={CHECKOUT_SCREEN} element={<CheckoutScreen />} />
                    <Route path={ORDER_CONFIRMED_SCREEN} element={<OrderConfirmedScreen />} />
                    <Route path={ORDER_FAILED_SCREEN} element={<OrderFailedScreen />} />
                    <Route path={ORDER_PAYMENT_FAILED_SCREEN} element={<OrderPaymentFailedScreen />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
