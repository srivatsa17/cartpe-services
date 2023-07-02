import { Navigate, Outlet } from "react-router-dom";

import { Container } from 'react-bootstrap';
import Footer from './components/Footer/Footer';
import { LOGIN_USER_SCREEN } from "./constants/routes";
import Navbar from "./components/Header/Navbar";
import React from "react";
import secureLocalStorage from "react-secure-storage";

const getUserTokenFromStorage = () => {
    const userLoginDetailsFromStorage = secureLocalStorage.getItem('userLoginDetails') ?
                            JSON.parse(secureLocalStorage.getItem('userLoginDetails')) : {}
    return userLoginDetailsFromStorage.access_token;
}

function ProtectedUserRoute() {
    const token = getUserTokenFromStorage();

    return (
        token ?
        <>
            <Navbar />
            <main className='py-3'>
                <Container>
                    <Outlet />
                </Container>
            </main>
            <hr />
            <Footer />
        </>
        :
        <Navigate to={LOGIN_USER_SCREEN} replace={true} />
    );
};

export default ProtectedUserRoute;