import React from "react";
import { Row, Col } from 'react-bootstrap';
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

function Filters({ products, category }) {
    const { uniqueBrands, uniqueCategories, uniqueAttributes } = getUniqueValues(products, category.name);

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
            <Row>
                <h6>PRICE RANGE</h6>
            </Row>
            <hr />
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