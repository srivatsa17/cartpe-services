import React from "react";
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Row, Col, Button, Card, ListGroup } from 'react-bootstrap';
import { FaRupeeSign } from "react-icons/fa";
import Rating from '../components/Rating';
import ImageSlider from "../components/ImageSlider";
import products from "../products";
import "../css/ProductScreen.css";

function ProductScreen() {
    const { id } = useParams();
    const product = products.find((p) => p._id === id)
    let navigate = useNavigate();

    return (
        <div>
            <Link onClick={() => navigate(-1)} className="btn btn-outline-secondary my-3">
                Go back
            </Link>
            <Row>
                <Col md={6}>
                    <ImageSlider product={product} />
                </Col>

                <Col md={3}>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            <h3>{product.name}</h3>
                        </ListGroup.Item>
                        <ListGroup.Item>
                            <Rating rating={product.rating} text={`${product.numReviews} reviews`} />
                        </ListGroup.Item>
                        <ListGroup.Item>
                            <h5>
                                Price: <FaRupeeSign size={18} id="rupee-icon" />{product.price}
                            </h5>
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Description: {product.description}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>

                <Col md={3}>
                    <Card>
                        <ListGroup variant="flush">
                            <ListGroup.Item>
                                <Row>
                                    <Col>Price:</Col>
                                    <Col>
                                        <strong>
                                            <FaRupeeSign size={16} id="rupee-icon" />{product.price}
                                        </strong>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Availability:</Col>
                                    <Col>
                                        <strong style={{ color: product.countInStock > 0 ? "green" : "red"}}>
                                            {
                                                product.countInStock > 0 ? "In Stock" : "Out of Stock"
                                            }
                                        </strong>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item className="d-grid gap-2">
                                <Button variant="dark" type="button" disabled={product.countInStock === 0}>
                                    Add to cart
                                </Button>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default ProductScreen;