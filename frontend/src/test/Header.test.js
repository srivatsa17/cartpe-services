import { render, fireEvent, screen, queryAllByText, queryAllByLabelText } from '@testing-library/react';
import Header from '../components/Header';

test('tests navbar items', () => {
    render(<Header />);
});