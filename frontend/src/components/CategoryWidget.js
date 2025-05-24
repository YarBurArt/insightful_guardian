import { useState, useEffect } from 'react';
import config from '../config';
import { notify } from './UserHelper';

const CategoryWidget = () => {
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    const fetchCategories = async () => {
      try{
        const response = await config.axios_b.get('/category');
        const data = response.data;
        console.log(data); // dev
        setCategories(data);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching categories:", error);
        notify("Error fetching categories");
      }
    };
    fetchCategories();
  }, []);
  if (!categories) {
    return null;
  }

  return (
    <div className="categoryWidget">
      <h2>Categories</h2>
      <hr></hr>
      {isLoading ? (
        <p> Loading... </p>
      ) : (
      <ul>
        {categories['cts'].map((category) => (
          <li key={category.id}>
            {/* it's works because within the {} - React expects a JS expression, not a plain string */}
            <a href={/category/ +  encodeURIComponent(category.name)}>{category.name}</a> 
          </li>
        ))}
      </ul> )}
    </div>
  );
};

export default CategoryWidget;
