function getUniqueCategories(products) {
    return [...new Set(products.map((product) => product.category))]
}

function getUniqueBrands(products) {
    return [ ...new Set(products.map((product) => product.brand))]
}

function getDiscountRanges() {
    return Array.from({ length: 9 }, (_, index) => (index + 1) * 10);
}

function getUniqueColors(products) {
    return products.reduce((result, product) => {
        product.attributes.map((attribute) => {
            const attributeName = attribute.name;
            const attributeValues = attribute.attribute_values.map(value => value.value);
            return result[attributeName] = [...new Set([...(result[attributeName] || []), ...attributeValues])];
        });
        return result;
    }, {})['color'];
}

function getMinAndMaxPrice(products) {
    let maxPrice = products[0]?.price;
    let minPrice = products[0]?.price;

    for (let i = 0; i < products.length; i++) {
        const price = products[i].price;
        if (price > maxPrice) {
            maxPrice = price;
        }
        if (price < minPrice) {
            minPrice = price;
        }
    }

    return { maxPrice, minPrice };
}

export function getUniqueFilterValues(products) {
    const uniqueCategories = getUniqueCategories(products);
    const uniqueBrands = getUniqueBrands(products);
    const uniqueColors = getUniqueColors(products) ?? [];
    const discountRanges = getDiscountRanges();
    const minAndMaxPrices = getMinAndMaxPrice(products)

    return {
        uniqueCategories,
        uniqueBrands,
        uniqueColors,
        discountRanges,
        minAndMaxPrices
    };
}