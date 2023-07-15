import { USER_LOGIN_DETAILS, USER_REGISTER_DETAILS } from "../../constants/localStorageConstants";

import { LOGIN_USER_SCREEN } from "../../constants/routes";
import axios from "axios";
import clearStorage from "../localStorage/clearStorage";
import getItemFromStorage from "../localStorage/getItemFromStorage";
import updateItemInStorage from "../localStorage/updateItemInStorage";

// Create the axios instance.
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
});

// Using axios interceptor before sending a http request
axiosInstance.interceptors.request.use(
    (config) => {
        const tokens = getItemFromStorage(USER_LOGIN_DETAILS);
        if (tokens) {
            config.headers.Authorization = `Bearer ${tokens.access_token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Wrap the interceptor in a function, so that i can be re-instantiated
function createAxiosResponseInterceptor() {
    const interceptor = axiosInstance.interceptors.response.use(
        (response) => response,
        async (error) => {
            // Reject promise if status code is other than 401(un-authorized).
            if (error.response.status !== 401) {
                return Promise.reject(error);
            }

            /*
                When response code is 401, try to refresh the token.
                Eject the interceptor so it doesn't loop in case token refresh causes the 401 response.
                Must be re-attached later on or the token refresh will only happen once.
            */
            axiosInstance.interceptors.response.eject(interceptor);
            const tokens = getItemFromStorage(USER_LOGIN_DETAILS) ?? {};
            const refresh_token = tokens.refresh_token;

            return await axiosInstance
                .post("users/token/refresh", {
                    refresh: refresh_token,
                })
                .then((response) => {
                    const updateData = {
                        "access_token": response.data.access,
                        "refresh_token": response.data.refresh
                    }
                    updateItemInStorage(USER_REGISTER_DETAILS, updateData);
                    error.response.config.headers["Authorization"] = "Bearer " + response.data.access;
                    // Retry the initial call, but with the updated token in the headers.
                    // Resolves the promise if successful
                    return axios(error.response.config);
                })
                .catch((error2) => {
                    // Retry failed, clean up storage, redirect to login and reject the promise.
                    clearStorage();
                    window.location.href = LOGIN_USER_SCREEN;
                    return Promise.reject(error2);
                })
                // Re-attach the interceptor by running the method
                .finally(createAxiosResponseInterceptor);
        }
    );
}

createAxiosResponseInterceptor();

export default axiosInstance;