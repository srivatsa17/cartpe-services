import '../css/ProductSearchScreen/ProductSearchScreen.css';

import { Col, Container, Row } from 'react-bootstrap';
import React, { useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';

import AlertMessage from '../components/AlertMessages/AlertMessage';
import Filters from "../components/ProductSearchScreen/Filters/Filters";
import Loader from "../components/Loader/Loader";
import Product from "../components/ProductSearchScreen/ProductCard/Product";
import SortBy from "../components/ProductSearchScreen/SortBy/SortBy";
import { getProducts } from '../actions/productActions';
import { getUniqueFilterValues } from '../utils/ProductSearchScreen/getUniqueFilterValues';
import { parseISO } from 'date-fns';
import { useFilterSearchParams } from "../utils/ProductSearchScreen/useFilterSearchParams";

function ProductSearchScreen() {
    const dispatch = useDispatch()
    const productList = useSelector(state => state.productList)
    const { products, error, isLoading } = productList;

    const { uniqueCategories, uniqueBrands, uniqueColors, discountRanges, minAndMaxPrices } = getUniqueFilterValues(products ?? []);
    const { searchedCategory, filteredCategories, filteredBrands, filteredColors, filteredDiscount, filteredMaxPrice, sortBy } = useFilterSearchParams();

    useEffect(() => {
        dispatch(getProducts(searchedCategory))
    }, [dispatch, searchedCategory])

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
        return filteredDiscount ? product.discount >= filteredDiscount : true;
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
                                    ?.filter(handleFilterCategories)
                                    .filter(handleFilterBrands)
                                    .filter(handleFilterColors)
                                    .filter(handleFilterDiscount)
                                    .filter(handleFilterPrice)
                                    .sort(sortProduct);

    return (
        <Container>
            {   isLoading ?
                <Loader /> : error ?
                    <AlertMessage variant="danger">
                        {error}
                    </AlertMessage> 
                    :
                    <>
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
                                <Row>
                                {
                                    filteredAndSortedProducts?.map((product, index) => {
                                        return (
                                            <Col key={index} xs={12} sm={12} md={12} lg={6} xl={4}>
                                                <Product product={product} />
                                            </Col>
                                        )
                                    })
                                }
                                </Row>
                            </Col>
                        </Row>
                    </>
            }
        </Container>
    );
}

export default ProductSearchScreen;