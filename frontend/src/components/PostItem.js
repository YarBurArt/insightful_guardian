import React from 'react';
import { Link } from 'react-router-dom';

const PostItem = ({ post }) => {
    return (
        <li className="post"> 
            <Link to={`/post/${post.post_id}`} className='link_post'>
                {post.title}
            </Link> <br/>
            | {post.content.slice(0, 500)} 
            {post.content.length > 500 && ' ...'}  <br/># {post.category}
        </li>
    );
};

export default PostItem;
