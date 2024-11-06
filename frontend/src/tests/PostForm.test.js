import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PostForm from '../components/PostForm';
import config from '../config';
import { jest } from '@jest/globals';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';

// mocking axios
jest.mock('../config', () => ({
  axios_b: {
    post: jest.fn(),
  },
}));

describe('PostForm', () => {
  beforeEach(() => {
    jest.clearAllMocks(); // reset all mocks before each test
  });

  test('renders PostForm component', () => {
    render(
      <MemoryRouter>
        <PostForm />
      </MemoryRouter>
    );
    expect(screen.getByText(/Preview content/i)).toBeInTheDocument();
  });

  test('allows user to input title and content', () => {
    // simulate navigation without setting up a full browser-based routing
    render(
      <MemoryRouter>
        <PostForm />
      </MemoryRouter>
    );

    const titleInput = screen.getByPlaceholderText(/Title/i); // assuming you have a placeholder for the title
    const contentInput = screen.getByPlaceholderText(/Content/i); // assuming you have a placeholder for the content

    fireEvent.change(titleInput, { target: { value: 'My Post Title' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });

    expect(titleInput.value).toBe('My Post Title');
    expect(contentInput.value).toBe('This is the content of the post.');
  });

  test('submits the form and creates a post', async () => {
    const mockPostResponse = { data: { post_id: '12345' } };
    config.axios_b.post.mockResolvedValueOnce(mockPostResponse); // mocking a successful response

    render(
      <MemoryRouter>
        <PostForm />
      </MemoryRouter>
    );

    const titleInput = screen.getByPlaceholderText(/Title/i);
    const contentInput = screen.getByPlaceholderText(/Content/i);
    const submitButton = screen.getByText(/Submit/i); // assuming you have a "submit" button

    fireEvent.change(titleInput, { target: { value: 'My Post Title' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(config.axios_b.post).toHaveBeenCalledWith('/posts/', {
        post_id: expect.any(String), // checking that post_id is a string
        title: 'My Post Title',
        content: 'This is the content of the post.',
        category: '', // checking that category is empty
      });
    });
  });

  test('handles error when creating a post', async () => {
    config.axios_b.post.mockRejectedValueOnce(new Error('Network Error')); // mocking an error

    render(
      <MemoryRouter>
        <PostForm />
      </MemoryRouter>
    );

    const titleInput = screen.getByPlaceholderText(/Title/i);
    const contentInput = screen.getByPlaceholderText(/Content/i);
    const submitButton = screen.getByText(/Submit/i);

    fireEvent.change(titleInput, { target: { value: 'My Post Title' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.click(submitButton);

    await waitFor(() => { // checking that the alert was called with the correct message
      expect(alert).toHaveBeenCalledWith("Error creating post: Error: Network Error"); 
    });
  });
});
