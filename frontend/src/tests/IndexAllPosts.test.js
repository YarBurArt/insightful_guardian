import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import IndexAllPosts from '../components/IndexAllPosts';
import config from '../config';
import '@testing-library/jest-dom';


describe('IndexAllPosts', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state initially', () => {
    render(<IndexAllPosts />);
    const loadingImage = screen.getByAltText(/Loading.../i);
    expect(loadingImage).toBeInTheDocument();
  });

  test('renders posts after loading', async () => {
    // Mocking axios via mock object to simulate API response
    jest.mock('../config', () => ({
        mock_axios_b: {
        get: jest.fn(),
        },
    }));
    // Mocking response from API
    config.mock_axios_b.get.mockResolvedValueOnce({
      data: {
        posts: [{ id: 1, title: 'Post 1' }, { id: 2, title: 'Post 2' }],
        total: 20,
      },
    });

    render(<IndexAllPosts />);

    // Waiting for loading to finish
    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    // Checking that posts are rendered
    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });

  test('changes page when pagination is clicked', async () => {
    // Mocking response from API
    config.mock_axios_b.get.mockResolvedValueOnce({
      data: {
        posts: [{ id: 1, title: 'Post 1' }],
        total: 20,
      },
    });

    render(<IndexAllPosts />);

    // Waiting for loading to finish
    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    // Checking that posts are rendered
    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();

    // Mocking response from API for second page
    config.mock_axios_b.get.mockResolvedValueOnce({
      data: {
        posts: [{ id: 2, title: 'Post 2' }],
        total: 20,
      },
    });

    // Clicking on pagination button
    const paginationButton = screen.getByText(/2/i); 
    paginationButton.click();

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    // checking that posts are rendered
    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });
});
