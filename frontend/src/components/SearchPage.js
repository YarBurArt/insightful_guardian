import React, { useState } from 'react';
import { Alert } from 'react-native';
import toast, { Toaster } from 'react-hot-toast';
import config from '../config';
import SearchInput from './SearchInput';
import SearchResults from './SearchResults';


const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [posts, setPosts] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await config.axios_b.get(`/search?query=${query}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching search results:', error);  // dev
      toast.error("Posts not found, try another query");
      Alert.alert(error)
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
