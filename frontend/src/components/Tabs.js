import React, { useState } from 'react';

const Tabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabClick = (index) => {
    setActiveTab(index);
  };
  const handlePrevClick = () => {
    setActiveTab((prevActiveTab) => (prevActiveTab === 0 ? React.Children.count(children) - 1 : prevActiveTab - 1));
  };

  const handleNextClick = () => {
    setActiveTab((prevActiveTab) => (prevActiveTab === React.Children.count(children) - 1 ? 0 : prevActiveTab + 1));
  };

  return (
    <div>
      <div className="tabs">
        {React.Children.map(children, (child, index) => (
          <div
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            onClick={() => handleTabClick(index)}
          >
            {child.props.label}
          </div>
        ))}
      </div>
      <div className="tab-content">
        {React.Children.map(children, (child, index) =>
          activeTab === index ? child : null
        )}
      </div>
      <div className="tab-controls"> {/* TODO: fix this loop */}
        <button onClick={handlePrevClick}>Previous (edit)</button>
        <button onClick={handleNextClick}>Next (preview)</button>
      </div>
    </div>
  );
};

export default Tabs;