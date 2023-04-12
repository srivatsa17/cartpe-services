import { screen, render } from '@testing-library/react';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import Header from '../components/Header';

test('Check for Navbar in document', () => {
    render(
        <Router>
            <Header />
        </Router>
    );
    const navbar = screen.getByTestId("navbar");
    expect(navbar).toBeInTheDocument();
});

test('Check for background of Navbar', () => {
    render(
        <Router>
            <Header />
        </Router>
    );
    const navbar = screen.getByTestId("navbar");
    expect(navbar).toHaveStyle(`background: dark`);
});

test('Test Brand Name and Logo in Navbar', () => {
    render(
        <Router>
            <Header />
        </Router>
    );
    
    const logoSrc = '/images/cartpe-logo.png';
    const brandLogo = screen.getByAltText("brandLogo");

    expect(brandLogo).toHaveAttribute('src', logoSrc);
    expect(brandLogo).toHaveAttribute('alt', 'brandLogo');
});

test('Check for Wishlist link', () => {
    render(
        <Router>
            <Link to="/wishlist">Wishlist</Link>
        </Router>
    );
    expect(screen.getByText('Wishlist').closest('a')).toHaveAttribute('href', '/wishlist');

});

test('Check for Cart link', () => {
    render(
        <Router>
            <Header />
        </Router>
    );
    expect(screen.getByText('Cart').closest('a')).toHaveAttribute('href', '/cart');
});