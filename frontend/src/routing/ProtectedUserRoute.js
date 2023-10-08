import { Navigate, Outlet } from "react-router-dom";

import { Container } from 'react-bootstrap';
import Footer from '../components/Footer/Footer';
import { LOGIN_USER_SCREEN } from "../constants/routes";
import Navbar from "../components/Header/Navbar";
import React from "react";
import { USER_LOGIN_DETAILS } from "../constants/localStorageConstants";
import getItemFromStorage from "../utils/localStorage/getItemFromStorage";

function ProtectedUserRoute() {
    const token = getItemFromStorage(USER_LOGIN_DETAILS);

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