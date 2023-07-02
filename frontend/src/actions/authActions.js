import {
    USER_LOGIN_FAIL,
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_REGISTER_FAIL,
    USER_REGISTER_REQUEST,
    USER_REGISTER_SUCCESS
} from '../constants/authConstants'

import axios from 'axios';
import secureLocalStorage from 'react-secure-storage';

const storeUserLoggedInDetailsInStorage = (userTokens) => {
    const userLoginDetails = {
        isLoggedIn: true,
        access_token: userTokens.access,
        refresh_token: userTokens.refresh
    }
    secureLocalStorage.setItem('userLoginDetails', JSON.stringify(userLoginDetails));
}

const storeUserRegisteredDetailsInStorage = (userRegisterDetails) => {
    secureLocalStorage.setItem('userRegisterDetails', JSON.stringify(userRegisterDetails))
}

export const loginUser = (email, password) => async (dispatch) => {
    const loginUrl = 'http://localhost:8000/api/v1/users/login'
    try {
        dispatch({ type: USER_LOGIN_REQUEST })

        const loginData = { email: email, password: password }
        const config = { headers: { 'Content-type': 'application/json'} }
        const { data } = await axios.post(loginUrl, loginData, config)

        dispatch({ type: USER_LOGIN_SUCCESS, payload: true })

        storeUserLoggedInDetailsInStorage(data.tokens);
    } catch(error) {
        dispatch({
            type: USER_LOGIN_FAIL,
            payload: error.response && error.response.data.detail
                    ? error.response.data.detail
                    : error.message
        })
    }
}

export const registerUser = (email, password) => async (dispatch) => {
    const registerUrl = 'http://localhost:8000/api/v1/users/register'
    try {
        dispatch({ type: USER_REGISTER_REQUEST })

        const registerData = { email: email, password: password }
        const config = { headers: { 'Content-type': 'application/json' } }
        const { data } = await axios.post(registerUrl, registerData, config)
        dispatch({ type: USER_REGISTER_SUCCESS })

        const storageData = { isUserRegistered: true, isUserVerified: false, userDetails: data }
        storeUserRegisteredDetailsInStorage(storageData)

    } catch(error) {
        dispatch({
            type: USER_REGISTER_FAIL,
            payload: error.response && error.response.data.message
                    ? error.response.data.message
                    : error.message
        })
    }
}