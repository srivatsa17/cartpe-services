import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { Col } from 'react-bootstrap';
import FilterCategories from "./FilterCategories";
import FilterBrands from "./FilterBrands";
import FilterColors from "./FilterColors";
import FilterDiscounts from "./FilterDiscounts";
import FilterPrices from "./FilterPrices";
import '../../../css/ProductSearchScreen/Filters/Filters.css';

function Filters({ uniqueCategories, uniqueBrands, uniqueColors, discountRanges, minAndMaxPrices }) {
    const [queryParams, setQueryParams] = useSearchParams();
    const filteredCategories = queryParams.get('categories');
    const filteredBrands = queryParams.get('brands');
    const filteredColors = queryParams.get('colors');
    const filteredDiscount = queryParams.get('discount');
    const filteredPrice = queryParams.get('maxPrice');

    const [discount, setDiscount] = useState(filteredDiscount ?? null);
    const [selectedCategories, setSelectedCategories] = useState(filteredCategories?.split(',') ?? []);
    const [selectedBrands, setSelectedBrands] = useState(filteredBrands?.split(',') ?? []);
    const [selectedColors, setSelectedColors] = useState(filteredColors?.split(',') ?? []);
    const [selectedPrice, setSelectedPrice] = useState(filteredPrice ?? null);

    useEffect(() => {
        setSelectedCategories(filteredCategories?.split(',') ?? []);
        setSelectedBrands(filteredBrands?.split(',') ?? []);
        setSelectedColors(filteredColors?.split(',') ?? []);
        setDiscount(filteredDiscount ?? null);
        setSelectedPrice(filteredPrice ?? null);
    }, [filteredCategories, filteredColors, filteredBrands, filteredDiscount, filteredPrice]);

    const handleCategories = (category) => {
        if (selectedCategories.includes(category)) {
            setSelectedCategories(selectedCategories.filter((_category) => _category !== category));
        } else {
            setSelectedCategories([...selectedCategories, category]);
        }
    }

    const handleBrands = (brand) => {
        if (selectedBrands.includes(brand)) {
            setSelectedBrands(selectedBrands.filter((_brand) => _brand !== brand));
        } else {
            setSelectedBrands([...selectedBrands, brand]);
        }
    }

    const handleColors = (color) => {
        if (selectedColors.includes(color)) {
            setSelectedColors(selectedColors.filter((_color) => _color !== color));
        } else {
            setSelectedColors([...selectedColors, color]);
        }
    }

    const handleDiscounts = (discountValue) => {
        setDiscount(discountValue)
        if(discountValue) {
            queryParams.set('discount', discountValue)
        } else {
            queryParams.delete('discount', { replace : true })
        }
        setQueryParams(queryParams)
    }

    const handlePrices = (event) => {
        const maxPrice = event.target.value;
        setSelectedPrice(maxPrice);
        if(maxPrice && maxPrice > minAndMaxPrices.minPrice) {
            queryParams.set('maxPrice', maxPrice);
        } else {
            queryParams.delete('maxPrice')
        }
        setQueryParams(queryParams);
    }

    return (
        <Col className="filters-types-container" xs={8} sm={6} md={4} lg={3} xl={2} xxl={2}>
            {
                uniqueCategories.length > 0 &&
                <>
                    <FilterCategories
                        uniqueCategories={uniqueCategories}
                        selectedCategories={selectedCategories}
                        setSelectedCategories={setSelectedCategories}
                        handleCategories={handleCategories}
                    />
                    <hr />
                </>
            }
            {
                uniqueBrands.length > 0 &&
                <>
                    <FilterBrands
                        uniqueBrands={uniqueBrands}
                        selectedBrands={selectedBrands}
                        setSelectedBrands={setSelectedBrands}
                        handleBrands={handleBrands}
                    />
                    <hr />
                </>
            }
            {
                uniqueColors.length > 0 && 
                <>
                    <FilterColors 
                        uniqueColors={uniqueColors}
                        selectedColors={selectedColors}
                        setSelectedColors={setSelectedColors}
                        handleColors={handleColors}
                    />
                    <hr />
                </>
            }
            {
                discountRanges.length > 0 &&
                <>
                    <FilterDiscounts
                        discountRanges={discountRanges}
                        discount={discount}
                        handleDiscounts={handleDiscounts}
                    />
                    <hr />
                </>
            }
            {
                minAndMaxPrices.minPrice && minAndMaxPrices.maxPrice &&
                <>
                    <FilterPrices 
                        minAndMaxPrices={minAndMaxPrices}
                        selectedPrice={selectedPrice}
                        handlePrices={handlePrices}
                    />
                    <hr />
                </>
            }
        </Col>
    );
}

export default Filters;