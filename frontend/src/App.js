import './styles.css';
import PostForm from './components/PostForm';
import IndexAllPosts from './components/IndexAllPosts';
import Footer from './components/Footer'; 
import { BrowserRouter as Router, 
  Route, Routes, 
  Link} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Link className='link' to="/create_post">Create Post</Link>
      <Link className='link' to="/">Index All Posts</Link>
    <Routes>
      <Route path="/"
        element={<IndexAllPosts />}/> 
      <Route path="/create_post" 
        element={<PostForm />}>
      </Route>
      {/* TODO: add routes react ... */}
    </Routes>
    <Footer />
  </Router>
  );
}

export default App;
