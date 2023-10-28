import { Button, Col, Form, InputGroup, Modal, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import AlertMessage from "../AlertMessages/AlertMessage";
import Loader from "../Loader/Loader";
import React from "react";
import { editShippingAddress } from "../../actions/addressActions";
import { useState } from "react";

function EditAddress({ showAddressModal, handleCloseNewAddressModal, address }) {
    const dispatch = useDispatch()
    const [validated, setValidated] = useState(false)

    const { isLoading, addressList, error } = useSelector(state => state.address)

    const shippingAddress = addressList.find((add) => add.id === address.id);
    
    const initialFormData = {
        name: shippingAddress.name,
        alternate_phone: shippingAddress.alternate_phone,
        type: shippingAddress.type,
        is_default: shippingAddress.is_default,
        address: {
            line1: shippingAddress.address.line1,
            line2: shippingAddress.address.line2,
            city: shippingAddress.address.city,
            state: shippingAddress.address.state,
            country: "India",
            pin_code: shippingAddress.address.pin_code
        }
    }
    
    const [formData, setFormData] = useState(initialFormData)

    const { name, alternate_phone, type, is_default, address: { line1, line2, city, state, pin_code } } = formData

    const handleFieldChange = (e, fieldName, isAddressField = false, fieldWithinAddress) => {
        const value = isAddressField
            ? {
                ...formData[fieldName],
                [fieldWithinAddress]: e.target.value,
            }
            : e.target.type === "checkbox"
            ? e.target.checked
            : e.target.value;

        let isValid = true;
        if (fieldName === "alternate_phone") {
            // Check for digits in alternate_phone and pin_code
            isValid = value.length > 10 ? false : /^\d*$/.test(value);
        } else if(fieldWithinAddress === "pin_code") {
            isValid = value.pin_code.length > 6 ? false : /^\d*$/.test(value.pin_code);
        }

        if (isValid) {
            setFormData((previousFormData) => ({
                ...previousFormData,
                [fieldName]: value,
            }));
        }
    };

    const resetFormData = () => {
        setFormData(initialFormData)
    }
    
    const handleSubmit = (event) => {
        const form = event.currentTarget;
        event.preventDefault()

        if (form.checkValidity() === true) {
            dispatch(editShippingAddress(formData, shippingAddress.id))
            resetFormData()
            handleCloseNewAddressModal()
            setValidated(false)
        } else {
            setValidated(true)
        }
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
                    {
                        isLoading ?
                        <Modal.Body>
                            <Loader />
                        </Modal.Body>
                        : error ?
                        <Modal.Body>
                            <AlertMessage variant="danger">
                                Oops! Something went wrong while updating the address!
                            </AlertMessage>
                        </Modal.Body>
                        :
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
                                            value={name}
                                            onChange={(e) => handleFieldChange(e, 'name')}
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
                                                value={alternate_phone}
                                                onChange={(e) => handleFieldChange(e, 'alternate_phone')}
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
                                            value={line1}
                                            onChange={(e) => handleFieldChange(e, 'address', true, 'line1')}
                                        />
                                        <Form.Control.Feedback type="invalid">
                                            Please enter building name.
                                        </Form.Control.Feedback>
                                    </Col>
                                    <Col>
                                        <Form.Label>Area, Street, Sector, Village</Form.Label>
                                        <Form.Control type="text"
                                            required
                                            value={line2}
                                            onChange={(e) => handleFieldChange(e, 'address', true, 'line2')}
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
                                            value={city}
                                            onChange={(e) => handleFieldChange(e, 'address', true, 'city')}
                                        />
                                        <Form.Control.Feedback type="invalid">
                                            Please enter town/city.
                                        </Form.Control.Feedback>
                                    </Col>
                                    <Col>
                                        <Form.Label>State</Form.Label>
                                        <Form.Control type="text"
                                            required
                                            value={state}
                                            onChange={(e) => handleFieldChange(e, 'address', true, 'state')}
                                        />
                                        <Form.Control.Feedback type="invalid">
                                            Please enter state.
                                        </Form.Control.Feedback>
                                    </Col>
                                    <Col>
                                        <Form.Label>Pin Code</Form.Label>
                                        <Form.Control type="text"
                                            required
                                            value={pin_code}
                                            onChange={(e) => handleFieldChange(e, 'address', true, 'pin_code')}
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
                                                value={addressType}
                                                checked={type === addressType}
                                                onChange={(e) => handleFieldChange(e, 'type')}
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
                                    type="checkbox"
                                    checked={is_default}
                                    onChange={(e) => handleFieldChange(e, 'is_default')}
                                    required
                                />
                            </Form.Group>
                        </Modal.Body>
                    }

                    <Modal.Footer>
                        <Button variant="dark" onClick={() => handleCloseNewAddressModal()}>
                            Close
                        </Button>
                        {
                            ( !isLoading && !error ) &&
                            <Button type="submit" variant="success">
                                Update Address
                            </Button>
                        }
                    </Modal.Footer>
                </Form>
            </Modal>
    )
}

export default EditAddress;