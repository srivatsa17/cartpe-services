import { Button, ListGroup } from "react-bootstrap";

import CartItemDetails from "../../CartScreen/CartItemDetails";
import { PLACEHOLDER_IMAGE } from "../../../constants/imageConstants";
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

function DisplayCartItems({ handleActiveAccordionItem, cartItems }) {
    return (
        <React.Fragment>
            {
                cartItems.map((cartItem, index) => {
                    const featuredImage = getProductFeaturedImage(cartItem.product)
                    return (
                        <ListGroup key={index} className="py-2">
                            <ListGroup.Item className="py-3">
                                <CartItemDetails cartItem={cartItem} featuredImage={featuredImage} />
                            </ListGroup.Item>
                        </ListGroup>
                    )
                })
            }
            <div className="mt-2">
                <Button
                    variant="success"
                    onClick={() => handleActiveAccordionItem("2")}
                >
                    Place Order
                </Button>
                <Button
                    variant="warning"
                    className="mx-3"
                    onClick={() => handleActiveAccordionItem("0")}
                >
                    Go Back & Edit Address
                </Button>
            </div>
        </React.Fragment>
    )
}

export default DisplayCartItems;