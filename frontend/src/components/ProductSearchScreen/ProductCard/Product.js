import "../../../css/ProductSearchScreen/ProductCard/Product.css";

import { Card } from "react-bootstrap";
import { FaRupeeSign } from "react-icons/fa";
import { Link } from "react-router-dom";
import { PLACEHOLDER_IMAGE } from "../../../constants/imageConstants";
import Rating from "./Rating";
import React from "react";

const getProductFeaturedImage = (product) => {
    if(
        !product ||
        !product.product_images ||
        !product.product_images.find((image) => image.is_featured === true)
    ) {
        return PLACEHOLDER_IMAGE
    }
    return product.product_images.find((image) => image.is_featured === true).image
}

function Product({ product }) {
    const productLink = `/products/${product.slug}/${product.id}/buy`;
    const featuredImageObj = getProductFeaturedImage(product)

    return (
        <Card className="my-3 rounded">
            <Link
                to={productLink}
                data-testid="product-link-by-image"
            >
                <Card.Img src={featuredImageObj} alt="product-image"></Card.Img>
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