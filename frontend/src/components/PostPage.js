import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import config from '../config';
import loadingGif from '../ayanami_loading.gif';

const PostPage = () => {
  const { post_id } = useParams(); // get the post ID from the URL
  const [postData, setPostData] = useState(null);

  useEffect(() => {
    const fetchData = async () => { // TODO: add real url 
      const response = await config.axios_b.get(`/posts/${post_id}`); // fetch post data by ID
      const data = response.data;
      setPostData(data);
    };
    fetchData();
  }, [post_id]);
  // <> </> is React Fragment, for fast rendering page
  if (!postData) return ( 
    <> <img src={loadingGif} alt="Loading..." />
       <p>Loading...</p> </> 
  );
  // TODO: markdown support, with custom styles
  return (
    <div className="PostPage">
      <h1>{postData.title}</h1>
      <p>{postData.content}</p>
    </div>
  );
};

export default PostPage;
