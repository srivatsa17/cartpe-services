import { screen, render, fireEvent, waitFor, cleanup } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from '../src/components/Header';

describe("Header component", () => {

    beforeEach(() => {
        return render(
            <Router>
                <Header />
            </Router>
        );
    });

    afterEach(() => {
        cleanup();
    })

    test('Check for Navbar in document', () => {
        const navbar = screen.getByTestId("navbar");
        expect(navbar).toBeInTheDocument();
    });

    test('Check for background of Navbar', () => {
        const navbar = screen.getByTestId("navbar");
        expect(navbar).toHaveStyle(`background: dark`);
    });

    test('Check for Brand Name and Logo in Navbar', () => {
        const logoSrc = '/images/cartpe-logo.png';
        const brandLogo = screen.getByAltText("brandLogo");

        expect(brandLogo).toHaveAttribute('src', logoSrc);
        expect(brandLogo).toHaveAttribute('alt', 'brandLogo');
    });

    test('Check for Categories dropdown', async () => {
        fireEvent.click(screen.getByText('Categories'));
        await waitFor(() => screen.getByTestId('categories-dropdown'));
        expect(screen.getByText('Action')).toBeInTheDocument();
        expect(screen.getByText('Another action')).toBeInTheDocument();
        expect(screen.getByText('Something')).toBeInTheDocument();
        expect(screen.getByText('Separated link')).toBeInTheDocument();
    });

    test('Check for Searchbar', () => {
        expect(screen.getByTestId('Searchbar')).toBeInTheDocument();
    });

    test('Check for valid searching', () => {
        const input = screen.getByTestId("Searchbar");
        expect(input.value).toBe('');
        fireEvent.change(input, { target: { value: 'abc' }})
        expect(input.value).toBe('abc');
    })

    test('Check for invalid searching', () => {
        const input = screen.getByTestId("Searchbar");
        expect(input.value).toBe('');
        fireEvent.change(input, { target: { value: 'abc' }})
        expect(input.value).not.toBe('cd');
    })

    test('Check for Wishlist link', () => {
        expect(screen.getByText('Wishlist').closest('a')).toHaveAttribute('href', '/wishlist');
    });

    test('Check for Cart link', () => {
        expect(screen.getByText('Cart').closest('a')).toHaveAttribute('href', '/cart');
    });

    test('Check for Profile dropdown', () => {
        // Hover over profile dropdown
        fireEvent.mouseEnter(screen.getByText('Profile'));
        waitFor(() => expect(screen.getByTestId('profile-dropdown')).toBeTruthy);
        expect(screen.getByText('Action')).toBeInTheDocument();
        expect(screen.getByText('Another action')).toBeInTheDocument();
        expect(screen.getByText('Something')).toBeInTheDocument();
        expect(screen.getByText('Separated link')).toBeInTheDocument();

        // Hover away from profile dropdown
        fireEvent.mouseLeave(screen.getByText('Profile'));
        waitFor(() => expect(screen.getByTestId('profile-dropdown')).toBeFalsy);
    });
});