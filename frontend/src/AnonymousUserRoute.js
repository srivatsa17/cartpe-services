import { Navigate, Outlet } from "react-router-dom";

import { Container } from 'react-bootstrap';
import { HOME_SCREEN } from "./constants/routes";
import React from "react";
import secureLocalStorage from "react-secure-storage";

const getUserTokenFromStorage = () => {
    const userLoginDetailsFromStorage = secureLocalStorage.getItem('userLoginDetails') ?
                            JSON.parse(secureLocalStorage.getItem('userLoginDetails')) : {}
    return userLoginDetailsFromStorage.access_token;
}

function AnonymousUserRoute() {
    const token = getUserTokenFromStorage();

    return (
        token ?
        <Navigate to={HOME_SCREEN} replace={true} />
        :
        <>
            <main className='py-3'>
                <Container>
                    <Outlet />
                </Container>
            </main>
        </>
    );
};

export default AnonymousUserRoute;