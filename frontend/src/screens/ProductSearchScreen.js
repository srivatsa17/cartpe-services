import React, { useEffect, useState } from "react";
import { Container, Row, Col } from 'react-bootstrap';
import { parseISO } from 'date-fns';
import axios from 'axios';
import SortBy from "../components/ProductScreen/SortBy/SortBy";
import Filters from "../components/ProductScreen/Filters/Filters";
import '../css/ProductSearchScreen/ProductSearchScreen.css';
import { getUniqueFilterValues } from '../utils/ProductSearchScreen/getUniqueFilterValues';
import { useFilterSearchParams } from "../utils/ProductSearchScreen/useFilterSearchParams";

function ProductSearchScreen() {
    const [products, setProducts] = useState([]);
    const { uniqueCategories, uniqueBrands, uniqueColors, discountRanges, minAndMaxPrices } = getUniqueFilterValues(products);
    const { searchedCategory, filteredCategories, filteredBrands, filteredColors, filteredDiscount, filteredMaxPrice, sortBy } = useFilterSearchParams();

    useEffect(() => {
        axios.get('https://mocki.io/v1/00263173-72a7-48fd-87b9-f70a90ec64b2', {
        params: {
            category : searchedCategory ?? ""
        }}).then((response) => {
            setProducts(response.data ?? []);
        })
    }, [searchedCategory])

    const handleFilterCategories = (product) => {
        return filteredCategories.length > 0 ? filteredCategories.includes(product.category) : true;
    }

    const handleFilterBrands = (product) => {
        return filteredBrands.length > 0 ? filteredBrands.includes(product.brand) : true;
    }

    const handleFilterColors = (product) => {
        return  filteredColors.length > 0
                ? product.attributes.some((attribute) =>
                    attribute.attribute_values.some((value) =>
                        filteredColors.includes(value.value)
                    )
                ) : true
    }

    const handleFilterDiscount = (product) => {
        return filteredDiscount ? product.discount > filteredDiscount : true;
    };

    const handleFilterPrice = (product) => {
        return filteredMaxPrice ? product.price <= filteredMaxPrice : true;
    }

    const sortProduct = (a, b) => {
        switch(sortBy) {
            case 'new' : return parseISO(b.created_at) - parseISO(a.created_at);
            case 'discount' : return b.discount - a.discount;
            case 'price_desc' : return b.price - a.price;
            case 'price_asc' : return a.price - b.price;
            default : return a.name.localeCompare(b.name);
        }
    }

    const filteredAndSortedProducts = products
                                    .filter(handleFilterCategories)
                                    .filter(handleFilterBrands)
                                    .filter(handleFilterColors)
                                    .filter(handleFilterDiscount)
                                    .filter(handleFilterPrice)
                                    .sort(sortProduct);

    return (
        <Container>
            <Row>
                <Col>
                    <strong>{searchedCategory}</strong> - {filteredAndSortedProducts.length} items
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
                <Filters
                    uniqueCategories={uniqueCategories}
                    uniqueBrands={uniqueBrands}
                    uniqueColors={uniqueColors}
                    discountRanges={discountRanges}
                    minAndMaxPrices={minAndMaxPrices}
                />
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
    );
}

export default ProductSearchScreen;