import { Button, Col, Form, Modal, Row } from "react-bootstrap";

import React from "react";
import { useState } from "react";

function AddNewAddress({ showAddressModal, handleCloseNewAddressModal }) {
    const [validated, setValidated] = useState(false);

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        setValidated(true);
    };

    return (
            <Modal
                show={showAddressModal}
                onHide={handleCloseNewAddressModal}
                backdrop="static"
                centered
                size="lg"
            >
                <Form noValidate validated={validated} onSubmit={handleSubmit}>
                    <Modal.Header closeButton>
                        <Modal.Title>Add new Address</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        <Form.Label>
                            <strong>Contact Details</strong>
                        </Form.Label>

                        <Form.Group className="mb-3">
                            <Row>
                                <Col>
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter a name.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Phone number</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter phone number.
                                    </Form.Control.Feedback>
                                </Col>
                            </Row>
                        </Form.Group>

                        <Form.Label>
                            <strong>Address</strong>
                        </Form.Label>

                        <Form.Group className="mb-3">
                            <Row>
                                <Col>
                                    <Form.Label>Flat, House no., Building, Company, Apartment</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter building name.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Area, Street, Sector, Village</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter area name.
                                    </Form.Control.Feedback>
                                </Col>
                            </Row>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Row>
                                <Col>
                                    <Form.Label>Town/City</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter town/city.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>State</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter state.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Pin Code</Form.Label>
                                    <Form.Control type="text" required />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter pin code.
                                    </Form.Control.Feedback>
                                </Col>
                            </Row>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Check
                                inline
                                label="Set as default address"
                                name="group1"
                                type="checkbox"
                                required
                            />
                        </Form.Group>
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="dark" onClick={() => handleCloseNewAddressModal()}>
                            Close
                        </Button>
                        <Button type="submit" variant="success">
                            Save Address
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>
    )
}

export default AddNewAddress;