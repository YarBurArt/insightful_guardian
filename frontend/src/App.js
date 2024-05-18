import './App.css';
import PostForm from './components/PostForm';
import { BrowserRouter as Router, 
  Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/create_post" 
        element={<PostForm />}>
      </Route>
      {/* TODO: add routes react (index, posts, search...) */}
    </Routes>
  </Router>
  );
}

export default App;
