import React from "react";
import { Row, Col } from 'react-bootstrap';
import { FaRupeeSign } from "react-icons/fa";
import '../../css/ProductSearchScreen/Filters.css';

function getUniqueValues(products, excludedCategory) {
    const uniqueBrands = [...new Set(products.map(product => product.brand))];
    
    const uniqueCategories = [...new Set(
        products.map(product => product.category)
    )].filter(category => category !== excludedCategory);
  
    const uniqueAttributes = products.reduce((result, product) => {
        product.attributes.forEach(attribute => {
            const attributeName = attribute.name;
            const attributeValues = attribute.attribute_values.map(value => value.value);
            result[attributeName] = [...new Set([...(result[attributeName] || []), ...attributeValues])];
        });
        return result;
    }, {});
  
    return {
        uniqueBrands,
        uniqueCategories,
        uniqueAttributes
    };
}

function PriceRange({ min_value, max_value }) {
    if(min_value === null) {
        return (
            <>
                Under <FaRupeeSign className="rupee-icon"/>{max_value}
            </>
        )
    } else if(max_value === null) {
        return (
            <>
                Above <FaRupeeSign className="rupee-icon"/>{min_value}
            </>
        )
    }
    return (
        <>
            <FaRupeeSign className="rupee-icon"/>{min_value} - <FaRupeeSign className="rupee-icon"/>{max_value}
        </>
    )
}

function Filters({ products, category }) {
    const { uniqueBrands, uniqueCategories, uniqueAttributes } = getUniqueValues(products, category);

    // console.log('brands:', uniqueBrands);
    // console.log('categories:', uniqueCategories);
    // console.log('attributes:', uniqueAttributes);

    const categories = uniqueCategories.map((category, index) => {
        return (
            <div key={index} className="filter-type">
                <input type="checkbox" />
                <div className="filter-item">{category}</div>
            </div>
        )
    })

    const brands = uniqueBrands.map((brand, index) => {
        return (
            <div key={index} className="filter-type">
                <input type="checkbox" />
                <div className="filter-item">{brand}</div>
            </div>
        )
    })

    const priceRanges = [
        {"min_value" : null, "max_value" : 1000},
        {"min_value" : 1000, "max_value" : 5000},
        {"min_value" : 5000, "max_value" : 10000},
        {"min_value" : 10000, "max_value" : 20000},
        {"min_value" : 20000, "max_value" : null}
    ]

    const colors = uniqueAttributes?.color?.map((color, index) => {
        return (
            <div key={index} className="filter-type">
                <input type="checkbox" />
                <div className="color-circle" style={{ backgroundColor: `${color}` }}></div>
                <div className="filter-item">{color}</div>
            </div>
        )
    }) || []

    const discounts = Array.from({ length: 9 }, (_, index) => (index + 1) * 10);

    return (
        <Col className="filters-types-container" xs={5} sm={5} md={4} lg={3} xl={2} xxl={2}>
            {   uniqueCategories.length > 0 && 
                <>
                    <Row>
                        <div>
                            <h6>CATEGORIES</h6> 
                            {categories}
                        </div>
                    </Row>
                    <hr />
                </>
            }
            {
                uniqueBrands.length > 0 &&
                <>
                    <Row>
                        <div>
                            <h6>BRANDS</h6>
                            {brands}
                        </div>
                    </Row>
                    <hr />
                </>
            }
            {
                priceRanges.length > 0 &&
                <>
                    <Row>
                        <h6>PRICE RANGE</h6>
                        {
                            priceRanges.map((priceRange, index) => {
                                return (
                                    <div key={index} className="filter-type">
                                        <input type="checkbox" />
                                        <div className="filter-item">
                                            <PriceRange min_value={priceRange.min_value} max_value={priceRange.max_value}/>
                                        </div>
                                    </div>
                                )
                            })
                        }
                    </Row>
                    <hr />
                </>
            }
            {
                uniqueAttributes?.color?.length > 0 &&
                <>
                    <Row>
                        <div>
                            <h6>COLORS</h6>
                            {colors}
                        </div>
                    </Row>
                    <hr />
                </>
            }
            <Row>
                <h6>DISCOUNT RANGE</h6>
                {
                    discounts.map((discount, index) => {
                        return (
                            <div key={index} className="filter-type">
                                <input type="checkbox" />
                                <div className="filter-item">{discount}% and above</div>
                            </div>
                        )
                    })
                }
            </Row>
        </Col>
    );
}

export default Filters;