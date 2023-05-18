import React from "react";
import { useLocation } from "react-router-dom";
import { Container, Row, Col } from 'react-bootstrap';
import '../css/ProductSearchScreen/ProductSearchScreen.css';
import products from "../products";
import SortBy from "../components/ProductScreen/SortBy";
import Filters from "../components/ProductScreen/Filters";

function ProductSearchScreen() {
    const location = useLocation();
    const { category } = location.state;

    return (
        <div>
            <Container>
                <Row>
                    <Col>
                        <strong>{category.name}</strong> - {category.products.length} items
                    </Col>
                </Row>
                <Row className="filters-text-and-sort-by-row">
                    <Col className="filters-text-container" xs={6} sm={6} md={8} lg={9} xl={9} xxl={9}>
                        <h5>FILTERS</h5>
                    </Col>
                    <SortBy />
                </Row>
                <hr />
                <Row>
                    <Filters products={products} category={category}/>
                    <Col>
                        {
                            category?.products?.map((product, index) => {
                                return <div key={index}>{product.name}</div>
                            })
                        }
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default ProductSearchScreen;