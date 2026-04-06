import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import IndexAllPosts from '../components/IndexAllPosts';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('http://localhost:8000/api/blog/posts', () => {
    return HttpResponse.json({ posts: [{ post_id: '1', _id: '1', title: 'Post 1', content: 'Content 1', category: 'test' }, { post_id: '2', _id: '2', title: 'Post 2', content: 'Content 2', category: 'test' }], total: 20 });
  }),
  http.get('http://localhost:8000/api/blog/posts/:start/:end', () => {
    return HttpResponse.json({ posts: [{ post_id: '1', _id: '1', title: 'Post 1', content: 'Content 1', category: 'test' }, { post_id: '2', _id: '2', title: 'Post 2', content: 'Content 2', category: 'test' }], total: 20 });
  }),
  http.get('http://localhost:8000/api/blog/category', () => {
    return HttpResponse.json({ cts: [] });
  }),
  http.get('/api/posts/:postId/stats', () => {
    return HttpResponse.json({ likes: 5, views: 10 });
  }),
  http.post('/api/posts/:postId/like', () => {
    return HttpResponse.json({ message: 'Post liked' });
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('IndexAllPosts', () => {
  test('renders loading state initially and posts after loading', async () => {
    render(<MemoryRouter><IndexAllPosts /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });

  test('changes page when pagination is clicked', async () => {
    render(<MemoryRouter><IndexAllPosts /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 1/i)).toBeInTheDocument();

    server.use(
      http.get('http://localhost:8000/api/blog/posts/:start/:end', () => {
        return HttpResponse.json({ posts: [{ post_id: '2', _id: '2', title: 'Post 2', content: 'Content 2', category: 'test' }], total: 20 });
      })
    );

    const paginationButton = screen.getByRole('button', { name: /2/i });
    paginationButton.click();

    await waitFor(() => {
      expect(screen.queryByAltText(/Loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Post 2/i)).toBeInTheDocument();
  });
});
