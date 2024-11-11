import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PostForm from '../components/PostForm';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('/posts/', (req, res, ctx) => {
    // Simulate successful or error response depending on the test case

    if (req.body.title === 'My Post Title 1') {
      // Simulate successful post creation
      return res(ctx.json({ data: { post_id: '12345' } }));
    } else {
      // Simulate network error
      return res(ctx.status(500));
    }
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('PostForm', () => {
  beforeEach(() => {}); // No need for clearAllMocks with MSW

  test('renders PostForm component', () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);
    expect(screen.getByText(/Preview content/i)).toBeInTheDocument();
  });

  test('allows user to input title and content', () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByPlaceholderText(/Title/i);
    const contentInput = screen.getByPlaceholderText(/Content/i);

    fireEvent.change(titleInput, { target: { value: 'My Post Title' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });

    expect(titleInput.value).toBe('My Post Title');
    expect(contentInput.value).toBe('This is the content of the post.');
  });

  test('submits the form and creates a post', async () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByPlaceholderText(/Title/i);
    const contentInput = screen.getByPlaceholderText(/Content/i);
    const submitButton = screen.getByText(/Submit/i);

    fireEvent.change(titleInput, { target: { value: 'My Post Title 1' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Post created successfully!/i)).toBeInTheDocument(); // Assuming success message after creation
    });
  });

  test('handles error when creating a post', async () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByPlaceholderText(/Title/i);
    const contentInput = screen.getByPlaceholderText(/Content/i);
    const submitButton = screen.getByText(/Submit/i);

    fireEvent.change(titleInput, { target: { value: 'My Post Title 2' } }); // Simulate error scenario
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/An error occurred/i)).toBeInTheDocument(); // Assuming error message on failure
    });
  });
});