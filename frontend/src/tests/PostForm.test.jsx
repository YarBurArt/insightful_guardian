import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import PostForm from '../components/PostForm';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const mocks = vi.hoisted(() => ({
  toastInfo: vi.fn(),
  toastError: vi.fn(),
  generateUniquePostId: vi.fn().mockResolvedValue('test-post-id-12345'),
}));

vi.mock('react-toastify', () => ({
  ToastContainer: () => null,
  toast: {
    info: mocks.toastInfo,
    error: mocks.toastError,
    success: vi.fn(),
  },
}));

vi.mock('../components/UserHelper', () => ({
  generateUniquePostId: vi.fn().mockResolvedValue('test-post-id-12345'),
  notify: mocks.toastInfo,
  extractIFrameSrc: () => null,
  fetchSearchResults: vi.fn(),
}));

const server = setupServer(
  http.post('http://localhost:8000/api/blog/posts/', async ({ request }) => {
    const body = await request.json();

    if (body.title === 'My Post Title 1') {
      return HttpResponse.json({ data: { post_id: '12345' } });
    } else {
      return new HttpResponse(null, { status: 500 });
    }
  }),
  http.get('https://api.ipify.org/', () => {
    return HttpResponse.json({ ip: '127.0.0.1' });
  }),
);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  mocks.toastInfo.mockClear();
  mocks.toastError.mockClear();
  mocks.generateUniquePostId.mockClear();
});
afterAll(() => server.close());

describe('PostForm', () => {
  test('renders PostForm component', () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);
    expect(screen.getByText(/Create Post/i)).toBeInTheDocument();
  });

  test('allows user to input title and content', () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByLabelText(/Title/i);
    const contentInput = screen.getByLabelText(/Content/i);

    fireEvent.change(titleInput, { target: { value: 'My Post Title' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });

    expect(titleInput.value).toBe('My Post Title');
    expect(contentInput.value).toBe('This is the content of the post.');
  });

  test('submits the form and creates a post', async () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByLabelText(/Title/i);
    const contentInput = screen.getByLabelText(/Content/i);
    const form = titleInput.closest('form');

    fireEvent.change(titleInput, { target: { value: 'My Post Title 1' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mocks.toastInfo).toHaveBeenCalledWith('Post created successfully');
    });
  });

  test('handles error when creating a post', async () => {
    render(<MemoryRouter><PostForm /></MemoryRouter>);

    const titleInput = screen.getByLabelText(/Title/i);
    const contentInput = screen.getByLabelText(/Content/i);
    const form = titleInput.closest('form');

    fireEvent.change(titleInput, { target: { value: 'My Post Title 2' } });
    fireEvent.change(contentInput, { target: { value: 'This is the content of the post.' } });
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mocks.toastInfo).toHaveBeenCalledWith(
        expect.stringContaining('Error creating post'),
      );
    });
  });
});
