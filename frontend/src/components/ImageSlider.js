import React, { useState, useRef } from "react";
import { Image, Row } from "react-bootstrap";
import { FaAngleLeft, FaAngleRight } from "react-icons/fa";
import "../css/ImageSlider.css";

function ImageSlider({ product }) {
    // Get these images dynamically from db for the product passed as a prop.
    const productImages = [
        {imageURL : "/images/alexa.jpg"},
        {imageURL : "/images/airpods.jpg"},
        {imageURL : "/images/camera.jpg"},
        {imageURL : "/images/mouse.jpg"},
        {imageURL : "/images/phone.jpg"},
        {imageURL : "/images/playstation.jpg"}
    ];

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

    const [featuredImage, setFeaturedImage] = useState(product.image);
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
                            productImages.map((image, imageId) => {
                                return (
                                    <Image
                                        key={imageId}
                                        src={image.imageURL}
                                        id="product-images"
                                        data-testid="product-images"
                                        onMouseOver={handleFeaturedImage}
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