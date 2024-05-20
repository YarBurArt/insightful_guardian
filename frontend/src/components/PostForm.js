import React, { useState } from 'react';

const PostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: gen uuid for post id and send form to serv 
    console.log('Send data to srv:', { title, content, category });
    // clean all
    setTitle('');
    setContent('');
    setCategory('');
  };

  return (
  <div className='PostForm'>
    <h1>Create Post</h1>
    <h3>Remember that your post will be public only after moderation by AI and signatures.</h3>
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="title">Title:</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="content">Content:</label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required></textarea>
      </div>
      <div>
        <label htmlFor="category">Category:</label>
        <input
          type="text"
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
        />
      </div>
      <button type="submit">Public </button>
    </form></div>
  );
};

export default PostForm;
