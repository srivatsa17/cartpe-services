import React from "react";
import { Container } from 'react-bootstrap';
import { Outlet } from "react-router-dom";

function RouteWithoutNavbar() {
    return (
        <>
            <main className='py-3'>
                <Container>
                    <Outlet />
                </Container>
            </main>
        </>
    );
};

export default RouteWithoutNavbar;