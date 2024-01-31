import * as yup from "yup";

import { Button, Col, Form, InputGroup, Modal, Row } from "react-bootstrap";
import { ErrorMessage, Field, Formik, getIn } from "formik";

import AlertMessage from "../../AlertMessages/AlertMessage";
import Loader from "../../Loader/Loader";
import React from "react";
import { useSelector } from "react-redux";

function EditAddress({ showEditAddressModal, setShowEditAddressModal, address, handleEditShippingAddress }) {
    const { isLoading, addressList, error } = useSelector(state => state.address)
    const shippingAddress = addressList.find((add) => add.id === address.id) || {};

    const schema = yup.object().shape({
        name:   yup.string()
                .trim()
                .matches(/^[a-zA-Z0-9\s]+$/, "Enter a valid First Name.")
                .min(2, "Length is too short.")
                .max(200, "Length is too long.")
                .required("Name is required."),
        alternate_phone: yup.string()
                        .trim()
                        .matches(/^\d+$/, "Phone number must contain only digits.")
                        .length(10, "Phone number must have exactly 10 digits.")
                        .required("Phone number is required"),
        type:   yup.string().default("Home").required().oneOf(["Home" , "Work", "Other"], "Address type is required"),
        is_default: yup.bool().oneOf([true, false]).required(),
        address: yup.object().shape({
            line1:  yup.string()
                    .trim()
                    .min(2, "Length is too short.")
                    .max(200, "Length is too long.")
                    .required("Building Name is required."),
            line2:  yup.string()
                    .trim()
                    .min(2, "Length is too short.")
                    .max(200, "Length is too long.")
                    .required("Area is required."),
            city:   yup.string()
                    .trim()
                    .min(2, "Length is too short.")
                    .max(150, "Length is too long.")
                    .matches(/^[a-zA-Z0-9]+$/, "Enter a valid city name.")
                    .required("City is required."),
            state:  yup.string()
                    .trim()
                    .min(2, "Length is too short.")
                    .max(100, "Length is too long.")
                    .matches(/^[a-zA-Z0-9]+$/, "Enter a valid state name.")
                    .required("State is required."),
            pin_code: yup.string()
                    .trim()
                    .matches(/^\d+$/, "Pin code must contain only digits.")
                    .length(6, "Pin code must have exactly 6 digits.")
                    .required("Pin code is required"),
        })
    });

    const handleCloseEditAddressModal = () => {
        setShowEditAddressModal(false)
    }

    return (
        <Modal
            show={showEditAddressModal}
            onHide={handleCloseEditAddressModal}
            backdrop="static"
            centered
            size="lg"
        >
            <Formik
                validationSchema={schema}
                initialValues={shippingAddress}
                onSubmit={(formData, { setSubmitting }) => {
                    setTimeout(() => {
                        handleEditShippingAddress(formData, shippingAddress.id)
                        setSubmitting(false)
                        handleCloseEditAddressModal()
                    }, 500);
                }}
            >
            {({ handleSubmit, handleBlur, handleChange, touched, errors, isValid, isSubmitting }) => (
                <Form onSubmit={handleSubmit}>
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
                                Oops! Something went wrong while adding new address!
                            </AlertMessage>
                        </Modal.Body>
                        :
                        <Modal.Body>
                            <Form.Label>
                                <strong>Contact Details</strong>
                            </Form.Label>
                            <Form.Group className="mb-2">
                                <Row>
                                    <Col>
                                        <Form.Label>Name</Form.Label>
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="name"
                                            onBlur={handleBlur}
                                            isInvalid={!!touched.name && !!errors.name}
                                            isValid={!!touched.name && !errors.name}
                                        />
                                        <ErrorMessage
                                            name="name"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
                                    </Col>
                                    <Col>
                                        <Form.Label>Phone number</Form.Label>
                                        <InputGroup className="mb-3" hasValidation>
                                            <InputGroup.Text
                                                // Adding the style manually because `hasValidation` has no effect
                                                // on right border here for some unknown reason.
                                                style={{ "borderTopRightRadius": 0, "borderBottomRightRadius": 0 }}
                                            >
                                                +91
                                            </InputGroup.Text>
                                            <Field
                                                as={Form.Control}
                                                type="text"
                                                name="alternate_phone"
                                                onBlur={handleBlur}
                                                isInvalid={!!touched.alternate_phone && !!errors.alternate_phone}
                                                isValid={!!touched.alternate_phone && !errors.alternate_phone}
                                            />
                                            <ErrorMessage
                                                name="alternate_phone"
                                                render={(errorMessage) => (
                                                    <Form.Control.Feedback type="invalid">
                                                        {errorMessage}
                                                    </Form.Control.Feedback>
                                                )}
                                            />
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
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="address.line1"
                                            onBlur={handleBlur}
                                            isInvalid={!!getIn(touched, "address.line1") && !!getIn(errors, "address.line1")}
                                            isValid={!!getIn(touched, "address.line1") && !getIn(errors, "address.line1")}
                                        />
                                        <ErrorMessage
                                            name="address.line1"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
                                    </Col>

                                    <Col>
                                        <Form.Label>Area, Street, Sector, Village</Form.Label>
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="address.line2"
                                            onBlur={handleBlur}
                                            isInvalid={!!getIn(touched, "address.line2") && !!getIn(errors, "address.line2")}
                                            isValid={!!getIn(touched, "address.line2") && !getIn(errors, "address.line2")}
                                        />
                                        <ErrorMessage
                                            name="address.line2"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
                                    </Col>
                                </Row>
                            </Form.Group>

                            <Form.Group className="mb-3">
                                <Row>
                                    <Col>
                                        <Form.Label>Town/City</Form.Label>
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="address.city"
                                            isInvalid={!!getIn(touched, "address.city") && !!getIn(errors, "address.city")}
                                            isValid={!!getIn(touched, "address.city") && !getIn(errors, "address.city")}
                                        />
                                        <ErrorMessage
                                            name="address.city"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
                                    </Col>
                                    <Col>
                                        <Form.Label>State</Form.Label>
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="address.state"
                                            isInvalid={!!getIn(touched, "address.state") && !!getIn(errors, "address.state")}
                                            isValid={!!getIn(touched, "address.state") && !getIn(errors, "address.state")}
                                        />
                                        <ErrorMessage
                                            name="address.state"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
                                    </Col>
                                    <Col>
                                        <Form.Label>Pin Code</Form.Label>
                                        <Field
                                            as={Form.Control}
                                            type="text"
                                            name="address.pin_code"
                                            isInvalid={!!getIn(touched, "address.pin_code") && !!getIn(errors, "address.pin_code")}
                                            isValid={!!getIn(touched, "address.pin_code") && !getIn(errors, "address.pin_code")}
                                        />
                                        <ErrorMessage
                                            name="address.pin_code"
                                            render={(errorMessage) => (
                                                <Form.Control.Feedback type="invalid">
                                                    {errorMessage}
                                                </Form.Control.Feedback>
                                            )}
                                        />
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
                                            <Field
                                                as={Form.Check}
                                                name="type"
                                                key={index}
                                                inline
                                                label={addressType}
                                                type="radio"
                                                value={addressType}
                                                onChange={handleChange}
                                                isInvalid={!!touched.type && !!errors.type}
                                                isValid={!!touched.type && !errors.type}
                                            />
                                        )
                                    })
                                }
                                <ErrorMessage
                                    name="type"
                                    render={(errorMessage) => (
                                        <Form.Control.Feedback type="invalid">
                                            {errorMessage}
                                        </Form.Control.Feedback>
                                    )}
                                />
                            </Form.Group>

                            <Form.Group className="mb-3">
                                <Field
                                    as={Form.Check}
                                    inline
                                    name="is_default"
                                    label="Mark as my default address"
                                    type="checkbox"
                                    onChange={handleChange}
                                    isInvalid={!!touched.is_default && !!errors.is_default}
                                    isValid={!!touched.is_default && !errors.is_default}
                                />
                            </Form.Group>

                        </Modal.Body>
                    }
                    <Modal.Footer>
                        <Button variant="dark" onClick={handleCloseEditAddressModal} disabled={isSubmitting}>
                            Close
                        </Button>
                        {
                            ( !isLoading && !error ) &&
                            <Button
                                type="submit"
                                variant="success"
                                disabled={!isValid || isSubmitting}
                            >
                                {
                                    isSubmitting ?
                                    <>Updating Address <Loader size={"sm"}/></> :
                                    <>Update Address</>
                                }
                            </Button>
                        }
                    </Modal.Footer>
                </Form>
            )}
            </Formik>
        </Modal>
    )
}

export default EditAddress;