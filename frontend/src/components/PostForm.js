import React, { useState } from 'react';
import config from '../config';
import axios from 'axios';
import { Navigate } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from "rehype-raw";
import Tabs from './Tabs';

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
    // TODO: generate ig_token access, save in DB and cookies
    try {
      const response = await config.axios_b.post('/posts/', {
        post_id, title, content, category, 
      });
      console.log('Post creation response:', response.data); // dev
      return <Navigate to={`/post/${post_id}`} />;
  
    } catch (error) {
      console.error('Error creating post:', error); // dev
      alert("Error creating post: " + error);
    }
  };
  // react fragments here only for readability
  return (
  <Tabs>
  <div className='PostForm'>
    <h1>Create Post</h1>
    <h3>Remember that your post will be public only after moderation by AI and signatures.</h3>
    <form onSubmit={handleSubmit}>
      <>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" value={title}
          onChange={(e) => setTitle(e.target.value)}
          required />
      </>
      <>
      {/* TODO: add content with url filter */}
        <label htmlFor="content">Content:</label>
        <textarea id="content" value={content}
          onChange={(e) => setContent(e.target.value)}
          required />
      </>
      <>
        <label htmlFor="category">Category:</label>
        <input type="text" id="category" value={category}
          onChange={(e) => setCategory(e.target.value)}
          required />
      </>
      <button type="submit">Public </button>
    </form></div>
    <div className='PostForm-preview'>
      <h1>Preview content (markdown support)</h1>
      <ReactMarkdown  rehypePlugins={[rehypeRaw]}>{content}</ReactMarkdown>
    </div>
    </Tabs>
  );
};

export default PostForm;
