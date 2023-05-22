import React, { useState } from "react";
import { Col } from 'react-bootstrap';
import '../../../css/ProductSearchScreen/Filters.css';
import FilterDiscounts from "./FilterDiscounts";
import { useSearchParams } from "react-router-dom";

function Filters() {
    const [discount, setDiscount] = useState(null);
    const [queryParams, setQueryParams] = useSearchParams();

    const handleDiscounts = (discountValue) => {
        setDiscount(discountValue)
        if(discountValue) {
            queryParams.set('discount', discountValue)
        } else {
            queryParams.delete('discount')
        }
        setQueryParams(queryParams)
    }

    return (
        <Col className="filters-types-container" xs={5} sm={5} md={4} lg={3} xl={2} xxl={2}>
            <FilterDiscounts discount={discount} handleDiscounts={handleDiscounts}/>
        </Col>
    );
}

export default Filters;