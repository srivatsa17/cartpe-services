import React from "react";
import { Card } from "react-bootstrap";
import Rating from "./Rating";
import { Link } from "react-router-dom";
import { FaRupeeSign } from "react-icons/fa";
import "../../../css/ProductSearchScreen/ProductCard/Product.css";

function Product({ product }) {
    const productLink = `/products/${product.slug}`;
    const featuredImageObj = product.product_images.find((image) => image.is_featured === true)

    return (
        <Card className="my-3 rounded">
            <Link
                to={productLink}
                data-testid="product-link-by-image"
            >
                <Card.Img src={featuredImageObj.image} alt="product-image"></Card.Img>
            </Link>
            <Card.Body>
                <Link
                    to={productLink}
                    id="product-link-by-name"
                    data-testid="product-link-by-name"
                >
                    <Card.Title as="div">
                        <div className="product-title">{product.name}</div>
                    </Card.Title>
                </Link>

                <Card.Subtitle as="div" className="product-description">
                    {product.description}
                </Card.Subtitle>

                <Card.Text as="div">
                    <div className="my-3">
                        <Rating rating={product.rating} text={`${product.numReviews ?? 0} reviews`} />
                    </div>
                </Card.Text>

                <Card.Text as="div" className="product-price-container">
                    <div id="product-selling-price">
                        <FaRupeeSign size={16} id="rupee-icon"/>
                        { product.selling_price }
                    </div>
                    {
                        product.discount > 0 &&
                        <div id="product-original-price">
                            <FaRupeeSign size={14} id="rupee-icon"/>
                            { product.price }
                        </div>
                    }
                    {
                        product.discount > 0 &&
                        <div id="product-discount-percent">
                            ({product.discount}% OFF)
                        </div>
                    }
                </Card.Text>
            </Card.Body>
        </Card>
    );
}

export default Product;