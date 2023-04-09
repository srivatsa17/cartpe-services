import React from "react";
import { Card } from "react-bootstrap";

function Product({ product }) {
    return (
        <Card className="my-3 p-3 rounded">
            <a href={`/product/${product._id}`}>
                <Card.Img src={product.image}></Card.Img>
            </a>
            <Card.Body>
                <a href={`/product/${product._id}`} style={{ color: "black", textDecoration: "none" }}>
                    <Card.Title as="div">
                        <strong>{product.name}</strong>
                    </Card.Title>
                </a>

                <Card.Text as="div">
                    <div className="my-3">
                        {product.rating} from {product.numReviews} reviews
                    </div>
                </Card.Text>

                <Card.Text>
                    <h3>
                        Rs. {product.price}
                    </h3>
                </Card.Text>
            </Card.Body>
        </Card>
    );
}

export default Product;