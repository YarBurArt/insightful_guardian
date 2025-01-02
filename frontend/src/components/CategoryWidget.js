import React from 'react';
//import config from '../config';
import loadingGif from '../ayanami_loading.gif';

const CategoryWidget = () => {
  // const [categories, setCategories] = useState([]);
  // const [isLoading, setIsLoading] = useState(true);
  // useEffect(() => {
  //   const fetchCategories = async () => {
  //     const response = await config.axios_b.get('/category');
  //     const data = response.data;
  //     console.log(data); // dev
  //     setCategories(data);
  //     setIsLoading(false);
  //   };
  //   fetchCategories();
  // }, []);
  // if (!categories) {
  //   return null;
  // }
  let isLoading = false;

  const categories = [
    { id: 1, name: 'Web Dev / backend' },
    { id: 2, name: 'Web3.0 / Blockchain' }, { id: 3, name: 'I know nothing' },
    { id: 4, name: 'Pentest web' }, { id: 5, name: 'DevSecOps' },
    { id: 6, name: 'ML tech.' }, { id: 7, name: 'Linux adm.' },
    { id: 8, name: 'Mobile pentest' }
  ];
  
  return (
    <div className="categoryWidget">
      <h2>Categories</h2>
      <hr></hr>
      {isLoading ? (
        <img src={loadingGif} alt="Loading..." />
      ) : (
      <ul>
        {categories.map((category) => (
          <li key={category.id}>
            {/* it's works because within the {} - React expects a JS expression, not a plain string */}
            <a href={/category/ + category.name}>{category.name}</a> 
          </li>
        ))}
      </ul> )}
    </div>
  );
};

export default CategoryWidget;
