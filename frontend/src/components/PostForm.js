import React, { useState } from 'react';
import axios from 'axios';

const PostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    //const postId = generateUniquePostId(); // Replace with your chosen library
    const postId = 1;
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/blog/posts/', {
        title,
        content,
        category,
        id: postId, 
      });
  
      console.log('Post creation response:', response.data);
      setTitle('');
      setContent('');
      setCategory('');
      // TODO: redirect or success handling logic
  
    } catch (error) {
      console.error('Error creating post:', error);

    }
  };

  return (
  <div className='PostForm'>
    <h1>Create Post</h1>
    <h3>Remember that your post will be public only after moderation by AI and signatures.</h3>
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" value={title}
          onChange={(e) => setTitle(e.target.value)}
          required />
      </div>
      <div>
        <label htmlFor="content">Content:</label>
        <textarea id="content" value={content}
          onChange={(e) => setContent(e.target.value)}
          required />
      </div>
      <div>
        <label htmlFor="category">Category:</label>
        <input type="text" id="category" value={category}
          onChange={(e) => setCategory(e.target.value)}
          required />
      </div>
      <button type="submit">Public </button>
    </form></div>
  );
};

export default PostForm;
