import { USER_LOGIN_DETAILS, USER_REGISTER_DETAILS } from '../constants/localStorageConstants';
import {
    USER_LOGIN_FAIL,
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_LOGOUT_FAIL,
    USER_LOGOUT_REQUEST,
    USER_LOGOUT_SUCCESS,
    USER_REGISTER_FAIL,
    USER_REGISTER_REQUEST,
    USER_REGISTER_RESET,
    USER_REGISTER_SUCCESS,
    USER_VERIFY_FAIL,
    USER_VERIFY_REQUEST,
    USER_VERIFY_SUCCESS
} from '../constants/authConstants'

import axiosInstance from '../utils/axios/axiosInterceptor';
import clearStorage from '../utils/localStorage/clearStorage';
import getItemFromStorage from '../utils/localStorage/getItemFromStorage';
import publicAxiosInstance from '../utils/axios/publicAxios';
import saveItemInStorage from '../utils/localStorage/saveItemInStorage';
import throwAuthenticationErrorResponse from '../utils/errorResponse/throwAuthenticationErrorResponse';
import throwErrorResponse from '../utils/errorResponse/throwErrorResponse';
import updateItemInStorage from '../utils/localStorage/updateItemInStorage';

export const loginUser = (email, password) => async (dispatch) => {
    const loginUri = 'users/login'

    try {
        dispatch({ type: USER_LOGIN_REQUEST })
        const loginData = { email: email, password: password }
        const { data } = await publicAxiosInstance.post(loginUri, loginData)
        dispatch({ type: USER_LOGIN_SUCCESS, payload: true })
        dispatch({ type: USER_VERIFY_SUCCESS })
        const userLoginDetails = {
            isLoggedIn: true,
            access_token: data.tokens.access,
            refresh_token: data.tokens.refresh
        }
        saveItemInStorage(USER_LOGIN_DETAILS, userLoginDetails)
    } catch(error) {
        dispatch({
            type: USER_LOGIN_FAIL,
            payload: throwAuthenticationErrorResponse(error)
        })
    }
}

export const registerUser = (email, password) => async (dispatch) => {
    const registerUri = 'users/register'

    try {
        dispatch({ type: USER_REGISTER_REQUEST })
        const registerData = { email: email, password: password }
        const { data } = await publicAxiosInstance.post(registerUri, registerData)
        dispatch({ type: USER_REGISTER_SUCCESS })
        const storageData = {
            isUserRegistered: true,
            isUserVerified: false,
            userDetails: data
        }
        saveItemInStorage(USER_REGISTER_DETAILS, storageData)
    } catch(error) {
        dispatch({
            type: USER_REGISTER_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const verifyUserEmail = (id, token) => async (dispatch) => {
    const verifyUserEmailUri = 'users/verify-email'
    try {
        dispatch({ type: USER_VERIFY_REQUEST })
        const verifyUserEmailData = { uidb64: id, token: token }
        await publicAxiosInstance.patch(verifyUserEmailUri, verifyUserEmailData)
        dispatch({ type: USER_VERIFY_SUCCESS })
        const updateData = {
            isUserVerified: true
        }
        updateItemInStorage(USER_REGISTER_DETAILS, updateData)
    } catch(error) {
        dispatch({
            type: USER_VERIFY_FAIL,
            payload: throwErrorResponse(error)
        })
    }
}

export const logoutUser = () => async (dispatch) => {
    const logoutUri = 'users/logout'
    const loginDetails = getItemFromStorage(USER_LOGIN_DETAILS)
    const refresh_token = loginDetails ? loginDetails.refresh_token : null;

    try {
        dispatch({ type: USER_LOGOUT_REQUEST })
        const logoutData = { refresh_token: refresh_token }
        await axiosInstance.post(logoutUri, logoutData)
        dispatch({ type: USER_LOGOUT_SUCCESS, payload: false })
        dispatch({ type: USER_REGISTER_RESET })
        clearStorage()
    } catch(error) {
        dispatch({
            type: USER_LOGOUT_FAIL,
            payload: throwAuthenticationErrorResponse(error)
        })
    }
}