# Deployment Guide

## Option 1: Heroku (Recommended - Free & Easy)

### Backend Deployment to Heroku

1. **Install Heroku CLI** (if not already installed):
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Navigate to backend directory**:
   ```bash
   cd chess-web/backend
   ```

4. **Create Heroku app**:
   ```bash
   heroku create your-chess-app-name
   ```

5. **Deploy to Heroku**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Get your backend URL**:
   ```bash
   heroku info
   ```
   Note the URL (e.g., `https://your-chess-app-name.herokuapp.com`)

### Frontend Deployment to Netlify

1. **Update API URL** in `chess-web/frontend/src/components/ChessBoard.js`:
   ```javascript
   // Change this line:
   const API_BASE = 'http://localhost:5000/api';
   // To your Heroku URL:
   const API_BASE = 'https://your-chess-app-name.herokuapp.com/api';
   ```

2. **Build the React app**:
   ```bash
   cd chess-web/frontend
   npm run build
   ```

3. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Sign up/login
   - Drag and drop the `build` folder from `chess-web/frontend/build`
   - Your site will be live at a URL like `https://random-name.netlify.app`

## Option 2: Vercel (Alternative)

### Frontend Deployment to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy from frontend directory**:
   ```bash
   cd chess-web/frontend
   vercel
   ```

3. **Follow the prompts** and your app will be live

## Option 3: PythonAnywhere (Backend Alternative)

### Backend Deployment to PythonAnywhere

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)

2. **Upload your backend files**:
   - Go to Files tab
   - Upload all files from `chess-web/backend/`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure WSGI file**:
   - Go to Web tab
   - Edit the WSGI file to point to your app.py

5. **Reload your web app**

## Option 4: GitHub Pages (Frontend Alternative)

### Frontend Deployment to GitHub Pages

1. **Create a GitHub repository**

2. **Push your frontend code**:
   ```bash
   cd chess-web/frontend
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/chess-app.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to Pages section
   - Select source branch (main)
   - Your site will be at `https://yourusername.github.io/chess-app`

## Environment Variables

For production, you might want to use environment variables:

### Backend (.env file):
```
FLASK_ENV=production
FLASK_APP=app.py
```

### Frontend (.env.production file):
```
REACT_APP_API_URL=https://your-backend-url.com
```

## Custom Domain

1. **Buy a domain** (e.g., from Namecheap, GoDaddy)
2. **Point DNS** to your hosting provider
3. **Configure SSL certificates** (usually automatic with modern hosting)

## Testing Your Deployment

1. **Test backend API**:
   ```bash
   curl https://your-backend-url.com/api/board
   ```

2. **Test frontend**:
   - Open your frontend URL
   - Try making a chess move
   - Check browser console for any errors

## Troubleshooting

### Common Issues:

1. **CORS errors**: Make sure your backend allows your frontend domain
2. **API URL issues**: Double-check the API URL in your frontend code
3. **Build errors**: Make sure all dependencies are installed
4. **Port issues**: Heroku assigns its own port, don't hardcode 5000

### Debug Commands:

```bash
# Check Heroku logs
heroku logs --tail

# Check if backend is running
curl https://your-backend-url.com/api/board

# Test local development
cd chess-web/backend && python app.py
cd ../frontend && npm start
```

## Cost Breakdown

- **Heroku**: Free tier available (sleeps after 30 min inactivity)
- **Netlify**: Free tier available
- **Vercel**: Free tier available
- **PythonAnywhere**: Free tier available
- **GitHub Pages**: Free

## Recommended Setup

For a professional deployment, I recommend:
- **Backend**: Heroku (easy, reliable, free tier)
- **Frontend**: Netlify (fast, reliable, free tier)
- **Domain**: Custom domain for branding 