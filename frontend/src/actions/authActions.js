import {
    USER_LOGIN_REQUEST, USER_LOGIN_SUCCESS, USER_LOGIN_FAIL
} from '../constants/authConstants'
import axios from 'axios';

export const loginUser = (email, password) => async (dispatch) => {
    try {
        dispatch({ type: USER_LOGIN_REQUEST })
        const { data } = await axios.post('http://localhost:8000/api/v1/users/login', {
            data: {
                email: email,
                password: password
            }
        })
        dispatch({ type: USER_LOGIN_SUCCESS, payload: data })
    } catch(error) {
        dispatch({
            type: USER_LOGIN_FAIL,
            payload: error.response && error.response.data.message
                    ? error.response.data.message
                    : error.message
        })
    }
}
