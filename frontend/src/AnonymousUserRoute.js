import { Navigate, Outlet } from "react-router-dom";

import { Container } from 'react-bootstrap';
import { HOME_SCREEN } from "./constants/routes";
import React from "react";
import secureLocalStorage from "react-secure-storage";

const getUserTokenFromStorage = () => {
    const userDetailsFromStorage = secureLocalStorage.getItem('userDetails') ?
                            JSON.parse(secureLocalStorage.getItem('userDetails')) : {}
    return userDetailsFromStorage.access_token;
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