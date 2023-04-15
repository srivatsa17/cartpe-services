import { render, screen } from '@testing-library/react';
import Footer from '../src/components/Footer';

describe('Footer component', () => {
    beforeEach(() => {
        render(<Footer />);
    })

    test('Check for copyright', () => {
        const linkElement = screen.getByText(/Copyright © CartPe/i);
        expect(linkElement).toBeInTheDocument();
    });
})


