import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Pagination from './Pagination';

const IndexAllPosts = () => {
    const [posts, setPosts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const fetchPosts = async () => {
            try { // TODO: remove hard url 
                const response = await axios.get(
                    `http://127.0.0.1:8000/api/blog/posts/${currentPage}/10`);
                setPosts(response.data.posts);
                setTotalPages(Math.ceil(response.data.total / 10)); // 10 per page
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
    return (
        <div className="IndexAllPosts">
            <h1>Posts.</h1>
            <ul>
                {posts.map((post) => (
                    <li key={post._id}> {/* TODO: link style */}
                        <Link key={post.post_id} to={`/post/${post.post_id}`} className='link_post'>
                            {post.title}
                        </Link> <br/>
                    | {post.content} <br/># {post.category}
                    </li>
                ))}
            </ul>
            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
            />
        </div>
    );
};
export default IndexAllPosts;
