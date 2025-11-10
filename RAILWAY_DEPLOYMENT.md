# Deploying Deplacity to Railway

This guide will help you deploy the Deplacity Flask application to Railway.

## Prerequisites

- GitHub account with your project repository
- Railway account (can sign up with GitHub)
- All changes committed and pushed to GitHub

## Why Railway?

- ✅ Easy deployment from GitHub
- ✅ Free tier with $5/month credit
- ✅ Automatic PostgreSQL database provisioning
- ✅ Auto-deploy on git push
- ✅ Built-in environment variable management
- ✅ Fast deployment (usually under 2 minutes)

## Deployment Steps

### 1. Prepare Your Repository

Make sure all the following files are committed to your GitHub repository:

- ✅ `Procfile` - Tells Railway how to start your app
- ✅ `railway.json` - Railway configuration (optional but recommended)
- ✅ `requirements.txt` - Python dependencies with gunicorn and psycopg2-binary
- ✅ `wsgi.py` - WSGI entry point
- ✅ `.gitignore` - Excludes sensitive files

### 2. Create a Railway Account

1. Go to [Railway.app](https://railway.app/)
2. Click **"Login"** and sign in with your GitHub account
3. Authorize Railway to access your repositories

### 3. Create a New Project

1. Click **"New Project"** on Railway dashboard
2. Select **"Deploy from GitHub repo"**
3. Choose your `deplacity` repository
4. Railway will automatically detect it's a Python app

### 4. Add PostgreSQL Database

1. In your project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Generate a `DATABASE_URL` environment variable
   - Link it to your web service

### 5. Configure Environment Variables

Click on your web service, then go to the **"Variables"** tab:

**Required Environment Variables:**

```
ADMIN_USERNAME=Deplacity
ADMIN_PASSWORD=G19DeplacityUcl
SECRET_KEY=your-secret-key-here-change-this
FLASK_ENV=production
```

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

**To add variables:**
1. Click **"+ New Variable"**
2. Enter the name and value
3. Click **"Add"**
4. Repeat for all variables

### 6. Deploy

Railway will automatically deploy your application:

1. It detects Python from `requirements.txt`
2. Installs dependencies
3. Uses `Procfile` to start the app with Gunicorn
4. Your app goes live in 1-2 minutes! 🚀

### 7. Get Your Application URL

1. Go to your web service in Railway dashboard
2. Click on **"Settings"** tab
3. Scroll to **"Domains"** section
4. Click **"Generate Domain"**
5. Your app will be available at: `https://deplacity-production-xxxx.up.railway.app`

## Project Structure for Railway

```
deplacity/
├── Procfile              # ✅ Railway start command
├── railway.json          # ✅ Railway config (optional)
├── requirements.txt      # ✅ With gunicorn & psycopg2-binary
├── wsgi.py              # ✅ WSGI entry point
├── __init__.py          # ✅ Configured for DATABASE_URL
└── utils/db.py          # ✅ Supports PostgreSQL
```

## Railway Environment Variables

| Variable | Value | Auto-Generated |
|----------|-------|----------------|
| `DATABASE_URL` | postgres://... | ✅ Yes (from PostgreSQL service) |
| `PORT` | 8080 | ✅ Yes (Railway sets this) |
| `ADMIN_USERNAME` | Deplacity | ❌ You set this |
| `ADMIN_PASSWORD` | G19DeplacityUcl | ❌ You set this |
| `SECRET_KEY` | random-secret | ❌ You set this |
| `FLASK_ENV` | production | ❌ You set this |

## Monitoring & Management

### View Logs

1. Click on your web service
2. Click on **"Deployments"** tab
3. Click on the latest deployment
4. View real-time logs

### Database Management

**Using Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Connect to PostgreSQL
railway connect postgres
```

**Using PostgreSQL Client:**
1. Go to PostgreSQL service in Railway
2. Click **"Connect"** tab
3. Copy connection details
4. Use any PostgreSQL client (pgAdmin, DBeaver, etc.)

### Automatic Deployments

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update app"
git push origin main
```

Railway detects the push and redeploys automatically! ✨

## Cost & Free Tier

**Railway Free Trial:**
- $5 credit per month
- No credit card required to start
- Enough for small projects (hobby projects, testing, learning)

**Usage tips to stay within free tier:**
- Monitor your usage in the dashboard
- Stop services when not in use (development/testing)
- Upgrade to paid plan for production apps

**Typical monthly costs (after free credit):**
- Web Service: ~$2-5/month
- PostgreSQL: ~$2-5/month
- Total: ~$4-10/month for always-on service

## Troubleshooting

### Build Fails

**Check Python version:**
```json
// In railway.json (already configured)
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

**Verify dependencies:**
- Ensure `gunicorn` is in `requirements.txt`
- Ensure `psycopg2-binary` is in `requirements.txt`

### Database Connection Errors

1. Check PostgreSQL service is running
2. Verify `DATABASE_URL` is set
3. Check logs for connection errors
4. Ensure `psycopg2-binary` is installed

### Application Won't Start

1. Check `Procfile` syntax
2. Verify `wsgi.py` exists and is correct
3. Check logs for Python errors
4. Ensure `PORT` environment variable is used

### Static Files Not Loading

Flask serves static files automatically. If issues occur:
1. Check static files are committed to git
2. Verify `static/` folder structure
3. Check Flask static configuration in `__init__.py`

## Security Best Practices

⚠️ **Before Production:**

1. **Change credentials:**
   ```
   ADMIN_USERNAME=your-secure-username
   ADMIN_PASSWORD=strong-password-here
   SECRET_KEY=generate-a-random-secret-key
   ```

2. **Generate a strong SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Enable environment isolation:**
   - Use different credentials for production vs development
   - Never commit `.env` files to git

4. **Database backups:**
   - Railway doesn't provide automatic backups on free tier
   - Set up manual backups for important data
   - Consider upgrading for automatic backups

## Useful Railway Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands in Railway environment
railway run python manage.py migrate

# Open service in browser
railway open
```

## Comparison: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| Free Tier | $5/month credit | 750 hours/month |
| Setup | Easier | Slightly more config |
| Deploy Speed | Faster (~1-2 min) | Slower (~3-5 min) |
| Dashboard | Modern UI | Clean UI |
| Auto-redeploy | ✅ Yes | ✅ Yes |
| Database | PostgreSQL | PostgreSQL |
| CLI Tool | Excellent | Good |

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Railway Python Guide](https://docs.railway.app/guides/python)
- [Railway PostgreSQL](https://docs.railway.app/databases/postgresql)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Railway Discord Community](https://discord.gg/railway)

## Quick Start Summary

1. ✅ Files are ready (Procfile, railway.json, requirements.txt)
2. 🚀 Go to [railway.app](https://railway.app/) and login with GitHub
3. 📦 Create new project from your GitHub repo
4. 🗄️ Add PostgreSQL database
5. 🔧 Set environment variables (ADMIN_USERNAME, ADMIN_PASSWORD, SECRET_KEY)
6. ⚡ Generate domain
7. 🎉 Your app is live!

**Total time: ~5 minutes** ⏱️
