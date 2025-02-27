import { render, screen } from '@testing-library/react';
import AppV1 from './App';

test('renders learn react link', () => {
  render(<AppV1 />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
