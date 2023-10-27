import { Button, Col, Form, InputGroup, Modal, Row } from "react-bootstrap";

import React from "react";
import { useState } from "react";

function EditAddress({ showAddressModal, handleCloseNewAddressModal, shippingAddress }) {
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
                        <Modal.Title>Edit Address</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        <Form.Label>
                            <strong>Contact Details</strong>
                        </Form.Label>

                        <Form.Group className="mb-3">
                            <Row>
                                <Col>
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.name}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter a name.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Phone number</Form.Label>
                                    <InputGroup className="mb-3" hasValidation>
                                        <InputGroup.Text>+91</InputGroup.Text>
                                        <Form.Control type="text"
                                            required
                                            defaultValue={shippingAddress.alternate_phone}
                                        />
                                        <Form.Control.Feedback type="invalid">
                                            Please enter phone number.
                                        </Form.Control.Feedback>
                                    </InputGroup>
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
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.address.line1}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter building name.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Area, Street, Sector, Village</Form.Label>
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.address.line2}
                                    />
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
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.address.city}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter town/city.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>State</Form.Label>
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.address.state}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter state.
                                    </Form.Control.Feedback>
                                </Col>
                                <Col>
                                    <Form.Label>Pin Code</Form.Label>
                                    <Form.Control type="text"
                                        required
                                        defaultValue={shippingAddress.address.pin_code}
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Please enter pin code.
                                    </Form.Control.Feedback>
                                </Col>
                            </Row>
                        </Form.Group>

                        <Form.Label>
                            Save address as
                        </Form.Label>
                        <Form.Group className="mb-3">
                            {
                                ["Home", "Work", "Other"].map((addressType, index) => {
                                    return (
                                        <Form.Check
                                            key={index}
                                            inline
                                            label={addressType}
                                            type="radio"
                                            defaultChecked={addressType === shippingAddress.type}
                                            required
                                        />
                                    )
                                })
                            }
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Check
                                inline
                                label="Mark as my default address"
                                name="group1"
                                type="checkbox"
                                defaultChecked={shippingAddress.is_default}
                                required
                            />
                        </Form.Group>
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="dark" onClick={() => handleCloseNewAddressModal()}>
                            Close
                        </Button>
                        <Button type="submit" variant="success">
                            Update Address
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>
    )
}

export default EditAddress;