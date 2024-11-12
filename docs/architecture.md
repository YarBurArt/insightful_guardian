# Architecture Overview

## Project Structure

```
/insightful_guardian
├── docs            # mini project documentation in general 
│   ├── architecture.md  # you are here 
│   └── contribution.md  # how to contribute and support
├── backend          # python fastapi server-side
│   ├── api          # REST API routes as an interface 
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   ├── main.py      # fastapi app initialization
│   ├── repositories # as the repository pattern in java 
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   └── postgres.py
│   ├── services    # route services and basic logic
│   │   ├── __init__.py
│   │   ├── lib_profanity  # C-based optimization crutch
│   │   │   ├── main_linux.c
│   │   │   ├── main_win10.c
│   │   │   └── statprofilter.so
│   │   ├── moderation_service.py  # most interesting part of logic 
│   │   ├── moderation_service_test.py
│   │   ├── post_service.py
│   │   ├── post_service_test.py
│   │   └── profanity_en.csv
│   └── utils       # helper scripts for services  
│       ├── exceptions.py
│       ├── gen_fkdata.py
│       ├── __init__.py
│       ├── sec_analyzer.py    # analysis through ML models
│       └── testai.py
├── frontend        # client side on react and JS
│   ├── package.json
│   ├── package-lock.json
│   ├── public      # to run React in some versions
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── README.md
│   ├── server  # front from a separate server, is used by the crutch for learning 
│   │   ├── db.js
│   │   ├── index.js
│   │   └── routes
│   │       └── posts.js
│   ├── src         # frontend source code
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── ayanami_loading.gif
│   │   ├── components # to divide responsibilities into components
│   │   │   ├── CategoryPage.js
│   │   │   ├── CategoryWidget.js
│   │   │   ├── Footer.js
│   │   │   ├── IndexAllPosts.js  # for the basic homepage
│   │   │   ├── Pagination.js
│   │   │   ├── PostForm.js     # writing and editing new posts
│   │   │   ├── PostInput.js
│   │   │   ├── PostItem.js
│   │   │   ├── PostList.js
│   │   │   ├── PostPage.js     # specific post 
│   │   │   ├── SearchInput.js
│   │   │   ├── SearchPage.js   # separate search by name and tags
│   │   │   ├── SearchResults.js
│   │   │   ├── Tabs.js
│   │   │   ├── useIframeValidation.js
│   │   │   └── UserHelper.js
│   │   ├── config.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── setupTests.js
│   │   ├── styles # appearance of objects of various categories
│   │   │   ├── base
│   │   │   │   └── _reset.scss
│   │   │   ├── components
│   │   │   │   ├── _link.scss
│   │   │   │   ├── _loading.scss
│   │   │   │   └── _pagination.scss
│   │   │   ├── layout
│   │   │   │   ├── _category.scss
│   │   │   │   ├── _footer.scss
│   │   │   │   └── _header.scss
│   │   │   ├── main.scss
│   │   │   ├── pages
│   │   │   │   ├── _index.scss
│   │   │   │   ├── _post-form.scss
│   │   │   │   ├── _postpage.scss
│   │   │   │   └── _searchpage.scss
│   │   │   └── utils
│   │   │       ├── _mixins.scss
│   │   │       └── _variables.scss
│   │   ├── styles.css      # styles after building 
│   │   ├── styles.css.map
│   │   └── tests    # critical functionality tests 
│   │       ├── IndexAllPosts.test.js
│   │       ├── PostForm.test.js
│   │       └── tests_se    # more general tests on selenium 
│   │           ├── Dockerfile
│   │           ├── main.py
│   │           └── requirements.txt
│   └── tests
├── LICENSE
├── package-lock.json
├── poetry.lock
├── pyproject.toml
└── README.md
```
---
> BELOW IS JUST A SKETCH 
---
## Technology Stack

- **Backend**: FastAPI
- **Frontend**: React
- **Database**: PostgreSQL, MongoDB
- **Authentication**: there's no need, just an idea like the telegra . ph
- **Deployment**: Docker, KVM debian 

## Communication Between Frontend and Backend

- The frontend communicates with the backend via RESTful APIs.
- API endpoints are defined in the FastAPI application and can be accessed at `/api/v1/...`.

## Data Flow

1. **User Interaction**: Users interact with the React frontend.
2. **API Requests**: The frontend makes API requests to the FastAPI backend.
3. **Data Processing**: The backend processes the requests, interacts with the database, and returns responses.
4. **Rendering**: The frontend receives the data and updates the UI accordingly.

## Deployment Architecture

- **Frontend**: Deployed on ...
- **Backend**: Deployed on ...
- **Database**: Hosted on ...

## Scalability Considerations

- Use of load balancers to distribute traffic.
- Caching strategies to reduce database load.
- Microservices architecture for independent scaling of components.

## Conclusion

This document provides a high-level overview of the architecture for the FastAPI + React application. For more detailed information, please refer to the individual components' documentation.
