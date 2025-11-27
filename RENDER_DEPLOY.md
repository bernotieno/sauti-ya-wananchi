# Render Deployment Guide

## Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create PostgreSQL Database

### 2.1 Create Database Service
1. Go to https://render.com/dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in database details:
   - **Name**: `sauti-db` (or your preferred name)
   - **Database**: `sauti_db`
   - **User**: `sauti_user`
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (recommended)
   - **Plan**: Free tier or Starter ($7/month)

### 2.2 Get Database Connection Details
After creation, Render provides:
- **Internal Database URL**: `postgresql://sauti_user:password@dpg-xxx-a/sauti_db`
- **External Database URL**: `postgresql://sauti_user:password@dpg-xxx-a.oregon-postgres.render.com/sauti_db`

**Important**: Copy the **Internal Database URL** - this is what your web service will use.

## Step 3: Create Web Service

### 3.1 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in service details:
   - **Name**: `sauti-ya-wananchi`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: Free tier or Starter ($7/month)

### 3.2 Configure Build Settings
- **Dockerfile Path**: `./Dockerfile`
- **Docker Context**: `.`
- **Auto-Deploy**: Yes

## Step 4: Environment Variables

### 4.1 Required Variables
In your web service settings, add these environment variables:

```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://sauti_user:password@dpg-xxx-a/sauti_db
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

### 4.2 Optional AI Variables (if using AI features)
```
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

### 4.3 How to Add Environment Variables
1. Go to your web service dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add each variable one by one
5. Click **"Save Changes"**

## Step 5: Connect Database to Web Service

### 5.1 Link Services (Automatic Method)
1. In your web service dashboard
2. Go to **"Environment"** tab
3. Click **"Add from Database"**
4. Select your PostgreSQL database
5. This automatically adds `DATABASE_URL`

### 5.2 Manual Method
1. Copy the **Internal Database URL** from your PostgreSQL service
2. Add it as `DATABASE_URL` environment variable in your web service
3. Format: `postgresql://username:password@host/database_name`

## Step 6: Deploy

### 6.1 Trigger Deployment
1. Save all environment variables
2. Render will automatically start building
3. Monitor build logs in the **"Logs"** tab
4. Build takes 5-10 minutes

### 6.2 Verify Deployment
1. Check build logs for errors
2. Once deployed, visit your app URL: `https://your-app-name.onrender.com`
3. You should see the landing page

## Step 7: Post-Deployment Setup

### 7.1 Create Superuser
1. Go to your web service dashboard
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Follow prompts to create admin user

### 7.2 Seed Sample Data (Optional)
```bash
python manage.py seed_data
```

### 7.3 Access Admin Panel
Visit: `https://your-app-name.onrender.com/admin`

## Troubleshooting

### Database Connection Issues
- Ensure `DATABASE_URL` uses **Internal** database URL
- Check database and web service are in same region
- Verify database credentials are correct

### Build Failures
- Check build logs for specific errors
- Ensure all required environment variables are set
- Verify Dockerfile syntax

### App Not Loading
- Check `ALLOWED_HOSTS` includes your Render domain
- Verify `CSRF_TRUSTED_ORIGINS` is set correctly
- Check application logs for errors

## Important Notes

- **Free Tier Limitations**: Services sleep after 15 minutes of inactivity
- **Database Backups**: Automatic on paid plans
- **SSL**: Automatically provided by Render
- **Custom Domain**: Available on paid plans
- **Scaling**: Upgrade to paid plans for better performance