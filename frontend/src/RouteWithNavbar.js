import React from "react";
import { Outlet } from "react-router-dom";
import { Container } from 'react-bootstrap';
import Navbar from "../src/components/Header/Navbar";
import Footer from './components/Footer/Footer';

function RouteWithNavbar() {
    return (
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
    );
};

export default RouteWithNavbar;