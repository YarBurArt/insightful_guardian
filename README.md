# Insightful guardian
<!-- ![](https://images.unsplash.com/photo-1486944936280-f152c82ac151?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D) -->
![](docs/scr1.jpeg)
This is a repository created for learning goals, I'm actually trying to create an analog of telegra.ph, but with a different content moderation and search. I see the problem and try to fix it, but there is no docker image or anything else that can be deployed on a production server. Where I know how to do more efficiently I write, otherwise I ask generative AI. 
There's fullstack development on `FastAPI`, `React`, `MongoDB`.

[docs/architecture.md](docs/architecture.md)

[docs/contribution.md](docs/contribution.md)

## Requirements
### Backend 
- what = "version" -- why
- poetry ---- to install all
- python = "^3.10" -------- minimal python version 
- fastapi = "^0.111.0" ---------- async API backend 
- fastapi-cors = "^0.0.6" ---------- http operations
- motor = "^3.4.0" ---------------- async mongodb
- faker = "^25.2.0" ------------- generate test data
- nltk = "^3.8.1" ------------ data for moderations
- pandas = "^2.2.2" - load and process signatures
- better-profanity = "^0.7.0" --- moderate by lib 
### Frontend
- npm ---- to install all
- "axios": "^1.6.8", ------------ aio http requests
- "react": "^18.3.1", -------- base front framework
- "react-dom": "^18.3.1", ---------- render DOM api
- "react-router-dom": "^6.23.1", -- front endpoints
- "react-scripts": "^5.0.1", -------- project tools
- "snyk": "^1.1291.0" ---------- test security code

## Install and use
### Backend
clone repo
```bash
git clone https://github.com/YarBurArt/insightful_guardian.git
```
```bash
cd insightful_guardian
```
install poetry for py3 dependencies
```bash
pip install poetry 
```
install python dependencies
```bash
poetry install  
```
run backend through uvicorn in poetry shell 
```bash
poetry shell 
```
```bash
py backend/main.py
```
### Frontend
```bash
cd frontend
```
install react/js dependencies
```bash
npm install
```
compile styles from sass to css
```bash
npm run compile:sass
```
run react front (as a separate server)
```bash
npm start
```

Closing is better to start with the frontend, then the backend, then the environments.
I write tasks directly in the code via TODO: for convenience and clarity. Just relax, I know it's not the best code, but it works well enough
