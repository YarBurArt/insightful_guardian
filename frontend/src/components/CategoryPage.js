import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import config from "../config";
import { notify } from "./UserHelper";
import loadingGif from "../ayanami_loading.gif";
import CategoryWidget from "./CategoryWidget";
import { Link } from "react-router-dom";
import { ToastContainer } from 'react-toastify';

const CategoryPage = () => {
    const { category } = useParams();
    const [posts, setPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);  

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                var category_c = encodeURIComponent(category);
                const response = await config.axios_b.get(
                    `/category/posts/?name=${category_c}`);
                setPosts(response.data);
                setIsLoading(false);
            } catch (error) {
                console.error("Error fetching posts:", error);
                notify("Error fetching posts");
            }
        };
        fetchPosts();
    }, [category]
);
    return (
        <div className="container-n IndexPage">
        <CategoryWidget />
        <div className="IndexAllPosts">
            <h1>Posts in {category}.</h1>
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
        </div>
        <ToastContainer/>
        </div>
    );
};
export default CategoryPage;
