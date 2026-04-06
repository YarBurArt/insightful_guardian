import axios from 'axios';

const axios_b = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/blog',
  });

const config = {
    axios_b,
    DEFAULT_PAGE_SIZE: 10,
};
  
export default config;