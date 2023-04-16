import React from "react";
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Row, Col, Image, Button, Card, ListGroup } from 'react-bootstrap';
import Rating from '../components/Rating';
import products from "../products";

function ProductScreen() {
    const { id } = useParams();
    const product = products.find((p) => p._id === id)
    let navigate = useNavigate();

    return (
        <div>
            <Link onClick={() => navigate(-1)} className="btn btn-outline-secondary my-3">Go back</Link>
            <Row>
                <Col md={6}>
                    <Image src={product.image} alt={product.name} fluid/>
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
                            Price: Rs. {product.price}
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
                                            {product.price}
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
                                <Button variant="dark" type="button" disabled={product.countInStock === 0}>Add to cart</Button>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default ProductScreen;