import React, { useState, useEffect } from "react";
import config from '../config';
import Pagination from './Pagination';
import PostList from './PostList';
import loadingGif from '../ayanami_loading.gif';
import CategoryWidget from "./CategoryWidget";
import SearchInput from './SearchInput';
import { fetchSearchResults } from "./UserHelper";

const IndexAllPosts = () => {
    const [posts, setPosts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [isLoading, setIsLoading] = useState(true);

    const [query, setQuery] = useState('');
    
    useEffect(() => {
        const fetchPosts = async () => {
            try { 
                const response = await config.axios_b.get(`/posts/${currentPage}/10`);
                setPosts(response.data.posts);
                setIsLoading(false);
                setTotalPages(Math.ceil(response.data.total / 10)); // n per page
                document.scrollingElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } catch (error) {
                console.error("Error fetching posts:", error);
            }
        };
        fetchPosts();
    }, [currentPage]); // [] listen for changes in currentPage
    
    const handlePageChange = (page) => {
        setCurrentPage(page);
    };
    const handleSearch = async (query) => {
        try {
            const results = await fetchSearchResults(query);
            setPosts(results); // TODO: rewrite on redirect to sq page
            setIsLoading(false);
            setTotalPages(1);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    };

    return (
        <><div className="container-n IndexPage">
        <CategoryWidget />
        <div className="IndexAllPosts">
            <h1>Posts.</h1>
            {isLoading ? (
                <>
                <img src={loadingGif} alt="Loading..." />
                <h3>Loading . . . </h3>
                </>
            ) : (
                <PostList posts={posts} />
            )}
            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
            />
        </div>
        {/* TODO: rewrite, fix get request */}
        <SearchInput query={query} setQuery={setQuery} onSearch={handleSearch} />
        </div>
        </>
    );
};
export default IndexAllPosts;
