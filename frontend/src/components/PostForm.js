import React, { useState } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

async function getIP() {
  try { // ipify crunch
    const response = await axios.get('https://api.ipify.org?format=json');
    return response.data.ip;
  } catch (error) {
    console.error('Error getting IP address:', error);
    return '127.0.0.1'; // default IP 
  }
}
async function generateUniquePostId() {
  const ip = await getIP();
  const timestamp = Date.now();
  const randomValue = Math.random().toString(36).substring(2, 12); // Generate a random value
  const combinedString = `${ip}-${timestamp}-${randomValue}`;
  return uuidv4(combinedString);
}                                                  
const PostForm =  () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const post_id = await generateUniquePostId(); 
    //const postId = 1;
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/blog/posts/', {
        post_id, title, content, category, 
      });
      console.log('Post creation response:', response.data);
      setTitle('');
      setContent('');
      setCategory('');
      // TODO: redirect or success handling logic
      alert("Post created successfully!");
  
    } catch (error) {
      console.error('Error creating post:', error);
      alert("Error creating post: " + error);
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
