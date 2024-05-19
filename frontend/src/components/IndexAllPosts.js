import React, { useState, useEffect } from "react";
import axios from "axios";

const IndexAllPosts = () => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchPosts = async () => {
            try { // TODO: remove hard url 
                const response = await axios.get("http://127.0.0.1:8000/api/blog/posts");
                setPosts(response.data);
            } catch (error) {
                console.error("Error fetching posts:", error);
            }
        };

        fetchPosts();
    }, []);

    return (
        <div>
            <h1>Posts</h1>
            <ul>
                {posts.map((post) => (
                    <li key={post.id}>{post.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default IndexAllPosts;
