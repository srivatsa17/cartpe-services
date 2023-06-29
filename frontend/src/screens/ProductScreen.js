import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getProductDetails } from "../actions/productActions";
import { addToCart } from "../actions/cartActions";
import { Row, Col, ListGroup } from 'react-bootstrap';
import { FaRupeeSign, FaExchangeAlt } from "react-icons/fa";
import { BsTruck, BsCashStack } from "react-icons/bs";
import { TbTruckDelivery } from "react-icons/tb";
import Rating from "../components/ProductSearchScreen/ProductCard/Rating";
import ImageSlider from "../components/ProductScreen/ImageSlider";
import Loader from "../components/Loader/Loader";
import ErrorMessage from "../components/ErrorMessages/ErrorMessage";
import AddedToCartAlert from "../components/CartScreen/AddedToCartAlert";
import "../css/ProductScreen/ProductScreen.css";

function getDeliveryDate() {
    var today = new Date();
    var options = { weekday: 'short', month: 'short', day: 'numeric' };
    today.setDate(today.getDate() + 3);
    var formattedDate = today.toLocaleDateString('en-IN', options);
    return formattedDate;
}

function ProductScreen() {
    const { id } = useParams();
    const [showAlert, setShowAlert] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertVariant, setAlertVariant] = useState("");
    const navigate = useNavigate();
    
    const dispatch = useDispatch();
    const productDetails = useSelector(state => state.productDetails);
    const {product, loading, error} = productDetails;
    
    const cart = useSelector(state => state.cart);
    const { cartItems } = cart;
    const isProductInCart = cartItems.some((item) => item.product.id === product.id);

    useEffect(() => {
        dispatch(getProductDetails(id));
    }, [dispatch, id]);

    const addToCartHandler = () => {
        if(isProductInCart) {
            setAlertMessage("Item is already present in the cart");
            setAlertVariant("primary")
        } else {
            const defaultQuantity = 1;
            dispatch(addToCart(product, defaultQuantity));
            setAlertMessage("Amazing! Item has been added to the cart");
            setAlertVariant("success");
        }
        setShowAlert(true);
    }

    const closeAlertHandler = () => {
        setShowAlert(false);
    }
    
    return (
        <>
        {   loading ? <Loader /> : error ?
                <ErrorMessage variant="danger" >{error}</ErrorMessage> :
            <div>
                <Link onClick={() => navigate(-1)} className="btn btn-outline-secondary my-3">
                    Go back
                </Link>
                <Row>
                    <Col>
                        <ImageSlider product={product} />
                    </Col>

                    <Col>
                        {   showAlert && 
                            <AddedToCartAlert 
                                closeAlertHandler={closeAlertHandler}
                                alertMessage={alertMessage}
                                alertVariant={alertVariant}
                            /> 
                        }
                        <ListGroup variant="flush">
                            <ListGroup.Item >
                                <div className="brand-name">
                                    {product.brand}
                                </div>
                                <div className="product-name">{product.name}</div>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Rating rating={product.rating} text={`${product.reviews ?? 0} Reviews`} />
                            </ListGroup.Item>

                            <ListGroup.Item className="price-container">
                                <div id="product-selling-price">
                                    <FaRupeeSign size={22} id="rupee-icon"/>
                                    { product.selling_price }
                                </div>
                                {
                                    product.discount > 0 &&
                                    <div id="product-original-price">
                                        <FaRupeeSign size={22} id="rupee-icon"/>
                                        { product.price }
                                    </div>
                                }
                                {
                                    product.discount > 0 &&
                                    <div id="product-discount-percent">
                                        ({product.discount}% OFF)
                                    </div>
                                }
                            </ListGroup.Item>
                                
                            <ListGroup.Item>
                                <div className="product-availability">Availability:&nbsp;
                                    <strong style={{ color: product.stock_count > 0 ? "green" : "red"}}>
                                        {
                                            product.stock_count > 0 ? "In Stock" : "Out of Stock"
                                        }
                                    </strong>
                                </div>
                            </ListGroup.Item>

                            <ListGroup.Item className="button-container">
                                <button className="add-to-cart-button" disabled={product.stock_count === 0} onClick={addToCartHandler}>
                                    ADD TO CART
                                </button>
                                <button className="wishlist-button">
                                    WISHLIST
                                </button>
                            </ListGroup.Item>
                            
                            {   product.stock_count > 0 &&
                                <ListGroup.Item>
                                    <div className="delivery-options-title">
                                        Delivery Options <BsTruck size={24} className="delivery-truck-icon"/>
                                    </div>
                                    <div className="delivery-details">
                                        <div>
                                            <TbTruckDelivery size={22} className="delivery-details-icons"/>
                                            Get it by {getDeliveryDate()}
                                        </div>
                                        <div>
                                            <BsCashStack size={22} className="delivery-details-icons"/>
                                            Pay on Delivery available
                                        </div>
                                        <div>
                                            <FaExchangeAlt size={22} className="delivery-details-icons"/>
                                            Easy 14 days return & exchange available
                                        </div>
                                    </div>
                                </ListGroup.Item>
                            }

                            <ListGroup.Item className="product-details">
                                <div id="title">Product Details</div>
                                <div id="description">{product.description}</div>
                            </ListGroup.Item>
                        </ListGroup>
                    </Col>
                </Row>
            </div>
        }
        </>
    )
}

export default ProductScreen;