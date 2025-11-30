# Swiggy Vendor Chatbot - Frontend

The frontend for the Swiggy Vendor Chatbot, built with React, Vite, and Tailwind CSS.

## Setup

### Local Development

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The app will be available at `http://localhost:5173`.

    **Note**: The frontend connects to the backend at `http://localhost:8000`. Ensure the backend is running.

### Docker Deployment

The frontend is containerized using Nginx for production.

```bash
docker build -t chatbot-frontend .
docker run -p 80:80 chatbot-frontend
```

Refer to the root [README.md](../README.md) for full stack deployment using Docker Compose.

## Technologies

- **React 19**: UI Library
- **Vite 5**: Build tool and dev server
- **Tailwind CSS v3**: Utility-first CSS framework
- **PostCSS**: CSS processing
