import React, { useState, useEffect } from 'react';

const Tabs = ({ children, tab_name }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [showAll, setShowAll] = useState(false);
  const [isWideScreen, setIsWideScreen] = useState(window.innerWidth > 700)

  // Split children into an array
  const tabContents = React.Children.toArray(children);

  const handleTabClick = (index) => {
    setActiveTab(index);
    setShowAll(false);
  };

  const handleShowAll = () => {
    setShowAll((prev) => !prev);
  };

  const handleResize = () => {
    setIsWideScreen(window.innerWidth > 700);
    if (window.innerWidth <= 700) {
      setShowAll(false);
    }
  };

  useEffect(() => {
    // to tabs if on phone
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <>
      <div className="tabs">
        {tabContents.map((child, index) => (
          <div
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            onClick={() => handleTabClick(index)}>
            {child.props.label}
          </div>
        ))}
      </div>
      <div className="tab-content" style={{ 
        display: showAll ? 'flex' : 'block' }}>
        {showAll ? (
          tabContents.map((content, index) => (
            <div key={index} className="tab-pane" style={{ 
              flex: 1, justifyContent: 'center', alignItems: 'center', 
            }}>
              {content}
            </div>
          ))
        ) : (
          <div className="tab-pane">{tabContents[activeTab]}</div>
        )}
      </div>
      <div className="tab-controls">
        {tabContents.map((_, index) => (
          <button key={index} onClick={() => setActiveTab(index)}>
            {tab_name[index]}
          </button>
        ))}
        {isWideScreen && (
          <button onClick={handleShowAll}>
            {showAll ? 'Hide All' : 'Show All'}
          </button>
        )}
      </div>
    </>
  );
};

export default Tabs;
