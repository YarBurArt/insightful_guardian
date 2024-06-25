import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import config from '../config';
import Pagination from './Pagination';
import loadingGif from '../ayanami_loading.gif';
import CategoryWidget from "./CategoryWidget";

const IndexAllPosts = () => {
    const [posts, setPosts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchPosts = async () => {
            try { 
                const response = await config.axios_b.get(`/posts/${currentPage}/10`);
                setPosts(response.data.posts);
                setIsLoading(false);
                setTotalPages(Math.ceil(response.data.total / 10)); // n per page
                document.scrollingElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                console.log(response.data); // TODO: remove after debug
            } catch (error) {
                console.error("Error fetching posts:", error);
            }
        };
        fetchPosts();
    }, [currentPage]); // [] listen for changes in currentPage
    const handlePageChange = (page) => {
        setCurrentPage(page);
      };
    // TODO: optimize rendering posts lists on view
    return (
        <div className="container-n IndexPage">
        <CategoryWidget />
        <div className="IndexAllPosts">
            <h1>Posts.</h1>
            {isLoading ? (
                <img src={loadingGif} alt="Loading..." />
            ) : (
            <ul className="posts">
                {posts.map((post) => (
                    <li key={post._id} className="post"> 
                        <Link key={post.post_id} to={`/post/${post.post_id}`} className='link_post'>
                            {post.title}
                        </Link> <br/>
                    | {post.content.slice(0, 500)} 
                    {post.content.length > 500 && ' ...'}  <br/># {post.category}
                    </li>
                ))}
            </ul>  )}
            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
            />
        </div></div>
    );
};
export default IndexAllPosts;
