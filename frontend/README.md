# Frontend (React, react-router-dom, axios)

The frontend of Insightful Guardian is designed to provide a user-friendly and efficient platform for creating, submitting, and consuming content. It utilizes React and React Router DOM to deliver a responsive and dynamic user experience.
### Key Components:

- Link: Navigation links
- IndexAllPosts: Displays a list of posts
- PostForm: Provides a form to create new posts
- PostPage: Displays a single post in detail
- Footer: Renders the application footer
### Routing:

- /: Displays all posts (IndexAllPosts). By default, pagination shows 10 posts per page.
- /create_post: Renders the PostForm
- /sq: Placeholder for search functionality (currently displays IndexAllPosts). Essentially it searches through the text in the category, then the title, then the content.
- /post/:post_id: Displays a single post (PostPage). Each post is assigned a unique identifier (UUID) upon creation. UUIDs are dynamically generated using client-side parameters and a timestamp, ensuring uniqueness across users and sessions.
### Enhancements:

- Data fetching from API/database (Axios, useFetch hook)
- Error handling (In the project only within the capabilities of the react)
- Accessibility (But need to tweak the styles a bit to make it more comfortable and nice looking)
- Testing (If it works, it works)
- Deployment
### Running the App:

`npm run compile:sass:` Compiles Sass files into CSS for styling.

`npm start`: Starts the React development server, allowing hot reloading and live updates.
