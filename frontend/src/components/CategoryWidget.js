import React from 'react';

const categories = [
  { id: 1, name: 'Code' },
  { id: 2, name: 'Design' },
  { id: 3, name: 'Business' },
  { id: 4, name: 'Marketing' },
]; // TODO: get from backend

const CategoryWidget = () => {
  return (
    <div className="categoryWidget">
      <h2>Categories</h2>
      <hr></hr>
      <ul>
        {categories.map((category) => (
          <li key={category.id}>
            <a href="#">{category.name}</a> {/* TODO: add link */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CategoryWidget;
