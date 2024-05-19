import './App.css';
import PostForm from './components/PostForm';
import IndexAllPosts from './components/IndexAllPosts';
import { BrowserRouter as Router, 
  Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/"
        element={<IndexAllPosts />}/> 
      <Route path="/create_post" 
        element={<PostForm />}>
      </Route>
      {/* TODO: add routes react ... */}
    </Routes>
  </Router>
  );
}

export default App;
