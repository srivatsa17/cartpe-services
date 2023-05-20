import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Container, Row, Col } from 'react-bootstrap';
import { parseISO } from 'date-fns';
import axios from 'axios';
import SortBy from "../components/ProductScreen/SortBy";
import Filters from "../components/ProductScreen/Filters";
import '../css/ProductSearchScreen/ProductSearchScreen.css';

function ProductSearchScreen() {
    const [queryParams] = useSearchParams();
    const category = queryParams.get('searchItem');
    const [products, setProducts] = useState([]);

    useEffect(() => {
        axios.get('https://mocki.io/v1/d609f5e7-e6b4-4206-bd90-d54a465a4b3f', {
        params: {
            category : category ?? ""
        }}).then((response) => {
            setProducts(response.data);
        })
    }, [category])

    const handleSort = (sortByValue) => {
        const sortedProducts = products.sort((a, b) => {
            switch(sortByValue) {
                case 'new' : return parseISO(b.created_at) - parseISO(a.created_at);
                case 'discount' : return b.discount - a.discount;
                case 'price_desc' : return b.price - a.price;
                case 'price_asc' : return a.price - b.price;
                default : return a.name.localeCompare(b.name);
            }
        })
        setProducts(sortedProducts)
    }

    return (
        <div>
            <Container>
                <Row>
                    <Col>
                        <strong>{category}</strong> - {products.length} items
                    </Col>
                </Row>
                <Row className="filters-text-and-sort-by-row">
                    <Col className="filters-text-container" xs={6} sm={6} md={8} lg={9} xl={9} xxl={9}>
                        <h5>FILTERS</h5>
                    </Col>
                    <SortBy handleSort={handleSort} />
                </Row>
                <hr />
                <Row>
                    <Filters products={products} category={category}/>
                    <Col>
                        {
                            products?.map((product, index) => {
                                return <div key={index}>{product.name} - {product.price} - {product.discount} - {product.created_at}</div>
                            })
                        }
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default ProductSearchScreen;