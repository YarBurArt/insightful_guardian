import React, { useState } from 'react';
import { Link } from "react-router-dom";
import config from '../config';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [posts, setPosts] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await config.axios_b.get(`/search?query=${query}`);
      setPosts(response.data);
    } catch (error) {
      alert("Posts not found, try another query");
      console.error('Error fetching search results:', error);  // dev
    }
  };

  return (
    <div>
    <div className="IndexAllPosts search-container"> 
      <input
        className="search-input"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query"/>
      <button className='search-button' onClick={handleSearch}>Search</button>
    </div><div className="IndexAllPosts">
      {posts.length > 0 && (
        <div>
          <h2>Search Results</h2>
          <ul>
            {posts.map((post) => (
                <li key={post._id}> 
                    <Link key={post.post_id} to={`/post/${post.post_id}`} className='link_post'>
                        {post.title}
                    </Link> <br/>
                | {post.content} <br/># {post.category}
                </li>
        ))}</ul></div>)}
    </div>
    </div>
  );
};

export default SearchPage;
