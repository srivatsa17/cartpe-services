import "../../css/ProductScreen/ImageSlider.css";

import { FaAngleLeft, FaAngleRight } from "react-icons/fa";
import { Image, Row } from "react-bootstrap";
import React, { useRef, useState } from "react";

import { PLACEHOLDER_IMAGE } from "../../constants/imageConstants";

const getProductImages = (product) => {
    if(
        !product || !product.product_images || product.product_images.length === 0 ||
        !product.product_images.find((image) => image.is_featured === true)
    ) {
        return {
            productImages: Array(3).fill({"image": PLACEHOLDER_IMAGE}),
            imageToShowcase: PLACEHOLDER_IMAGE
        }
    }
    return {
        productImages: product.product_images,
        imageToShowcase: product.product_images.find((image) => image.is_featured === true).image
    }
}

function ImageSlider({ product }) {
    const { productImages, imageToShowcase } = getProductImages(product)
    const [featuredImage, setFeaturedImage] = useState(imageToShowcase);

    const scrollOffset = 145;
    const scrollSlider = useRef(null);

    const handleScrollLeft = () => {
        // document.getElementById('slider').scrollLeft -= scrollOffset
        // Below is React way of doing using useRef, the above line which is in javascript. For the element with id 'slider', we have added ref={scrollSlider}.
        // So scrollSlider is same as document.getElementById('slider')
        scrollSlider.current.scrollLeft -= scrollOffset;
    }

    const handleScrollRight = () => {
        scrollSlider.current.scrollLeft += scrollOffset;
    }

    const handleFeaturedImage = (e) => {
        // document.getElementById('featured-image').src = e.target.src;
        // We are doing the same above line using useState in React.
        setFeaturedImage(e.target.src);
    }

    return (
        <>
            <Row>
                <Image
                    id="featured-image"
                    src={featuredImage}
                    alt={product.name}
                    data-testid="featured-image"
                    fluid
                />
            </Row>

            <br/>

            <Row>
                <div className="image-slider-wrapper">
                    <FaAngleLeft
                        id="slide-left"
                        className="arrow"
                        size={42}
                        onClick={handleScrollLeft}
                        data-testid="slide-left-arrow"
                    />
                    <div className="slider" data-testid="slider" ref={scrollSlider}>
                        {
                            productImages.map((productImage, imageId) => {
                                return (
                                    <Image
                                        key={imageId}
                                        src={productImage?.image}
                                        id="product-images"
                                        data-testid="product-images"
                                        onClick={handleFeaturedImage}
                                    />
                                )
                            })
                        }
                    </div>
                    <FaAngleRight
                        id="slide-right"
                        className="arrow"
                        size={42}
                        onClick={handleScrollRight}
                        data-testid="slide-right-arrow"
                    />
                </div>
            </Row>
        </>
    );
}

export default ImageSlider;