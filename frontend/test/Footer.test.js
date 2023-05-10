import { render, screen, cleanup } from '@testing-library/react';
import Footer from '../src/components/Footer';

describe('Footer component', () => {
    beforeEach(() => {
        render(<Footer />);
    })

    afterEach(() => {
        cleanup();
    })

    test('Check for copyright', () => {
        const linkElement = screen.getByText(/Copyright © CartPe/i);
        expect(linkElement).toBeInTheDocument();
    });
})


