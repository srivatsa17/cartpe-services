import { render } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from '../components/Header';

test('tests navbar items', () => {
    render(
        <Router>
            <Header />
        </Router>
    );
    // const linkElement = screen.getByText(/Cart/i);
    // expect(linkElement).toBeInTheDocument();
});