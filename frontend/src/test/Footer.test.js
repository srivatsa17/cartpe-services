import { render, screen } from '@testing-library/react';
import Footer from '../components/Footer';

test('renders footer link', () => {
    render(<Footer />);
    const linkElement = screen.getByText(/Copyright/i);
    expect(linkElement).toBeInTheDocument();
});

