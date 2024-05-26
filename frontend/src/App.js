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
      <Link className='link' to="/sq">Search Post</Link>
    <Routes>
      <Route path="/"
        element={<IndexAllPosts />}/> 
      <Route path="/create_post" 
        element={<PostForm />}/> {/* TODO: selenium tests */}
      <Route path="/sq" 
        element={<IndexAllPosts />}/>
        {/* TODO: view post by name */}
    </Routes>
    <Footer />
  </Router>
  );
}

export default App;
