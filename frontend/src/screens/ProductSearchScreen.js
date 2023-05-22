import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Container, Row, Col } from 'react-bootstrap';
import { parseISO } from 'date-fns';
import axios from 'axios';
import SortBy from "../components/ProductScreen/SortBy/SortBy";
import Filters from "../components/ProductScreen/Filters/Filters";
import '../css/ProductSearchScreen/ProductSearchScreen.css';

function ProductSearchScreen() {
    const [products, setProducts] = useState([]);
    const [queryParams] = useSearchParams();
    const category = queryParams.get('searchItem');
    const discount = queryParams.get('discount');
    const sortBy = queryParams.get('sort');

    useEffect(() => {
        axios.get('https://mocki.io/v1/00263173-72a7-48fd-87b9-f70a90ec64b2', {
        params: {
            category : category ?? ""
        }}).then((response) => {
            setProducts(response.data);
        })
    }, [category])

    const filterDiscount = (product) => {
        if (discount) {
            return product.discount > discount;
        } else {
            return product;
        }
    };

    const sortProduct = (a, b) => {
        switch(sortBy) {
            case 'new' : return parseISO(b.created_at) - parseISO(a.created_at);
            case 'discount' : return b.discount - a.discount;
            case 'price_desc' : return b.price - a.price;
            case 'price_asc' : return a.price - b.price;
            default : return a.name.localeCompare(b.name);
        }
    }

    const filteredAndSortedProducts = products.filter(filterDiscount).sort(sortProduct);

    return (
        <div>
            <Container>
                <Row>
                    <Col>
                        <strong>{category}</strong> - {filteredAndSortedProducts.length} items
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
                    <Filters />
                    <Col>
                        {
                            filteredAndSortedProducts?.map((product, index) => {
                                return (
                                    <div key={index}>
                                        {product.name} - {product.price} - {product.discount} - {product.created_at}
                                    </div>
                                )
                            })
                        }
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default ProductSearchScreen;