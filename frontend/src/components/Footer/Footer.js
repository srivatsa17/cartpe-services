import { Col, Container, Row } from "react-bootstrap";

import React from "react";

function Footer() {
    const today = new Date();
    const year = today.getFullYear();

    return (
        <footer>
            <Container>
                <Row>
                    <Col className="text-center py-3">Copyright &copy; CartPe {year}</Col>
                </Row>
            </Container>
        </footer>
    );
}

export default Footer;