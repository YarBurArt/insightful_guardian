import React, { useState, useEffect, useRef } from 'react';
import config from '../config';
import { Navigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from "rehype-raw";
import Tabs from './Tabs';
import { generateUniquePostId, extractIFrameSrc } from './UserHelper';

// const iframeSrc = extractIFrameSrc(content); 
const PostForm =  () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');
  const [isChecking, setIsChecking] = useState(false);
  const timeoutRef = useRef(null) 
  const allowedDomains = ['youtube.com', 'sketchfab.com', 'google.com'];

  useEffect(() => {
    const validateIframeSrc = () => {
      const iframeSrc = extractIFrameSrc(content);
      if (iframeSrc) {
        const hostname = new URL(iframeSrc).hostname;
        if (!allowedDomains.includes(hostname)) {
          console.warn(`Iframe src not allowed: ${hostname}`);
        }
      }
      setIsChecking(false);
    };

    if (isChecking) {
      timeoutRef.current = setTimeout(validateIframeSrc, 3000);
    }

    return () => clearTimeout(timeoutRef.current); 
  }, [content, allowedDomains, isChecking]);

  const handleInputChange = (event) => {
    setContent(event.target.value);
    setIsChecking(true); 
  };

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
          required  />
      </>
      <>
        <label htmlFor="content">Content:</label>
        <textarea id="content" value={content}
          onChange={(e) => handleInputChange(e)} 
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
