import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const PostPage = () => {
  const { post_id } = useParams(); // get the post ID from the URL
  const [postData, setPostData] = useState(null);

  useEffect(() => {
    const fetchData = async () => { // TODO: add real url 
      const response = await axios.get(`/api/posts/${post_id}`); // fetch post data by ID
      const data = response.data;
      setPostData(data);
    };
    fetchData();
  }, [post_id]);
  // TODO: loading gif
  if (!postData) return <div>Loading...</div>;

  return (
    <div>
      <h1>{postData.title}</h1>
      <p>{postData.content}</p>
    </div>
  );
};

export default PostPage;
