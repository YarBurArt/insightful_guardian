# Insightful guardian
![](https://images.unsplash.com/photo-1486944936280-f152c82ac151?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)
This is a repository created for learning goals, I'm actually trying to create an analog of telegra.ph, but with a different content moderation and search. I see the problem and try to fix it, but there is no docker image or anything else that can be deployed on a production server. Where I know how to do more efficiently I write, otherwise I ask generative AI. 
There's fullstack development on `FastAPI`, `React`, `MongoDB`.

## Requirements
### Backend 
- what = "version" -- why
- python = "^3.10" -------- minimal python version 
- fastapi = "^0.111.0" ---------- async API backend 
- fastapi-cors = "^0.0.6" ---------- http operations
- motor = "^3.4.0" ---------------- async mongodb
- faker = "^25.2.0" ------------- generate test data
- nltk = "^3.8.1" ------------ data for moderations
- pandas = "^2.2.2" - load and process signatures
- better-profanity = "^0.7.0" --- moderate by lib 
### Frontend
- "axios": "^1.6.8", ------------ aio http requests
- "react": "^18.3.1", -------- base front framework
- "react-dom": "^18.3.1", ---------- render DOM api
- "react-router-dom": "^6.23.1", -- front endpoints
- "react-scripts": "^5.0.1", -------- project tools
- "snyk": "^1.1291.0" ---------- test security code
