import {
    USER_LOGIN_FAIL,
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_REGISTER_FAIL,
    USER_REGISTER_REQUEST,
    USER_REGISTER_SUCCESS,
    USER_VERIFY_FAIL,
    USER_VERIFY_REQUEST,
    USER_VERIFY_SUCCESS
} from '../constants/authConstants'

const loginUserInitialState = {
    userLoginDetails: {
        isLoggedIn: false
    }
}

export const userLoginReducer = (state = loginUserInitialState, action) => {
    switch(action.type) {
        case USER_LOGIN_REQUEST:
            return { isLoading: true }
        case USER_LOGIN_SUCCESS:
            return { isLoading: false, isLoggedIn: action.payload }
        case USER_LOGIN_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}

const registerUserInitialState = {}

export const userRegisterReducer = (state = registerUserInitialState, action) => {
    switch(action.type) {
        case USER_REGISTER_REQUEST:
            return { isLoading: true }
        case USER_REGISTER_SUCCESS:
            return { isLoading: false, isUserRegistered: true, isUserVerified: false }
        case USER_REGISTER_FAIL:
            return { isLoading: false, error: action.payload }
        case USER_VERIFY_REQUEST:
            return { isLoading: true }
        case USER_VERIFY_SUCCESS:
            return { isLoading: false, isUserRegistered: true, isUserVerified: true }
        case USER_VERIFY_FAIL:
            return { isLoading: false, error: action.payload }
        default:
            return state
    }
}