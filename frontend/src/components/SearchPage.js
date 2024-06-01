import React, { useState } from 'react';
import { Link } from "react-router-dom";
import axios from 'axios';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [posts, setPosts] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/blog/search?query=${query}`);
      setPosts(response.data);
    } catch (error) {
      alert("Posts not found, try another query");
      console.error('Error fetching search results:', error);  // dev
    }
  };

  return (
    <div className="IndexAllPosts"> {/* TODO: search style */}
      <h1>Search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query"/>
      <button onClick={handleSearch}>Search</button>
      
      {posts.length > 0 && (
        <div>
          <h2>Search Results</h2>
          <ul>
                {posts.map((post) => (
                    <li key={post._id}> {/* TODO: link style */}
                        <Link key={post.post_id} to={`/post/${post.post_id}`} className='link_post'>
                            {post.title}
                        </Link> <br/>
                    | {post.content} <br/># {post.category}
                    </li>
        ))}</ul></div>)}
    </div>
  );
};

export default SearchPage;
