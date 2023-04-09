import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders main app link', () => {
    render(<App />);
    const linkElement = screen.getByText(/Hello, Welcome/i);
    expect(linkElement).toBeInTheDocument();
});
