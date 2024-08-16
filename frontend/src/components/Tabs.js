import React, { useState } from 'react';

const Tabs = ({ tab1, tab2 }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabClick = (index) => {
    setActiveTab(index);
  };

  return (
    <div>
      <div className="tabs">
        <div
          className={`tab ${activeTab === 0 ? 'active' : ''}`}
          onClick={() => handleTabClick(0)} >
          {tab1.label}
        </div>
        <div
          className={`tab ${activeTab === 1 ? 'active' : ''}`}
          onClick={() => handleTabClick(1)} >
          {tab2.label}
        </div>
      </div>
      <div className="tab-content">
        {activeTab === 0 ? tab1.content : tab2.content}
      </div>
      <div className="tab-controls">
        <button onClick={() => setActiveTab(0)}>Tab 1</button>
        <button onClick={() => setActiveTab(1)}>Tab 2</button>
      </div>
    </div>
  );
};

export default Tabs;