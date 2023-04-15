import { screen, render, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Product from '../src/components/Product';

describe("Product component", () => {

    const product = {
        '_id': '3',
        'name': 'Cannon EOS 80D DSLR Camera',
        'image': '/images/camera.jpg',
        'price': 929.99,
    };

    beforeEach(() => {
        return render(
            <Router>
                <Product product={product}/>
            </Router>
        );
    });

    test('Check for product name', () => {
        const productName = product.name;
        expect(screen.getByText(productName)).toBeInTheDocument();
    });

    test('Check for product image', () => {
        const sampleImage = product.image;
        expect(screen.getByAltText('product-image')).toHaveAttribute('src', sampleImage);
        expect(screen.getByAltText('product-image')).toBeInTheDocument();
    });

    test('Check for product link in product name', () => {
        const productName = product.name;
        const productLink = `/product/${product._id}`;
        expect(screen.getByText(productName).closest('a')).toHaveAttribute('href', productLink);
    });

    test('Check for product link in product image', () => {
        const productLink = '/product/3';
        expect(screen.getByAltText('product-image').closest('a')).toHaveAttribute('href', productLink);
    });

    test('Check for navigation via product name', () => {
        fireEvent.click(screen.getByTestId("product-link-by-name"));
        waitFor(() => expect(screen.getByText(product.name)).toBeInTheDocument());
    });

    test('Check for navigation via product image', () => {
        fireEvent.click(screen.getByTestId("product-link-by-image"));
        waitFor(() => expect(screen.getByAllText(product.name)).toBeInTheDocument());
    });

    test('Check for product price', () => {
        const price = "Rs. " +  product.price;
        expect(screen.getByText(price)).toBeInTheDocument();
    })
});