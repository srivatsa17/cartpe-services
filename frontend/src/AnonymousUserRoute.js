import { Navigate, Outlet } from "react-router-dom";

import { Container } from 'react-bootstrap';
import { HOME_SCREEN } from "./constants/routes";
import React from "react";
import { USER_LOGIN_DETAILS } from "./constants/localStorageConstants";
import getItemFromStorage from "./utils/localStorage/getItemFromStorage";

function AnonymousUserRoute() {
    const token = getItemFromStorage(USER_LOGIN_DETAILS);

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