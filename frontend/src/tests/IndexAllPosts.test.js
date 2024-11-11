import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import IndexAllPosts from '../components/IndexAllPosts';
import { jest } from "@jest/globals";
import { TextDecoder, TextEncoder } from 'util';
Object.assign(global, { TextDecoder, TextEncoder });

import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/posts', (req, res, ctx) => {
    return res(ctx.json([{ id: 1, title: 'Post 1' }, { id: 2, title: 'Post 2' }]));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('IndexAllPosts', () => {
  beforeEach(() => {}); 

  test('renders loading state initially and posts after loading', async () => {
    render(<IndexAllPosts />);

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });

  test('changes page when pagination is clicked', async () => {
    render(<IndexAllPosts />);

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();

    // Simulate pagination by modifying the mocked response
    server.use(
      rest.get('/api/posts', (req, res, ctx) => {
        return res(ctx.json([{ id: 2, title: 'Post 2' }]));
      })
    );

    const paginationButton = screen.getByText(/2/i);
    paginationButton.click();

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });
});