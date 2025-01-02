import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { fetchSearchResults } from './UserHelper';
import SearchInput from './SearchInput';
import SearchResults from './SearchResults';


const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [posts, setPosts] = useState([]);

  const handleSearch = async () => {
    try {
      const posts = await fetchSearchResults(query);
      setPosts(posts);
    } catch (error) {
      console.debug('Error fetching search results:', error);
    }
  };
  return (
    <>
    <SearchInput query={query} setQuery={setQuery} handleSearch={handleSearch} />
    <SearchResults posts={posts} />
    <Toaster />
    </>
  );
};

export default SearchPage;
