# Castaways Ice Cream Shop - Deployment Guide

## 🚀 Quick Deploy to Heroku

### Prerequisites
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a [Heroku account](https://signup.heroku.com/)

### Deployment Steps

1. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Castaways Ice Cream Shop"
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-ice-cream-shop-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-super-secure-secret-key-here"
   heroku config:set ADMIN_USERNAME="admin"
   heroku config:set ADMIN_PASSWORD="your-secure-admin-password"
   heroku config:set FLASK_ENV="production"
   heroku config:set FLASK_DEBUG="False"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Initialize Database** (if needed)
   ```bash
   heroku run python -c "from views import init_db; init_db()"
   ```

## 🔧 Alternative Deployment Options

### Deploy to Railway
1. Connect your GitHub repository to [Railway](https://railway.app)
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Deploy to Render
1. Connect your GitHub repository to [Render](https://render.com)
2. Set environment variables in Render dashboard
3. Choose Python web service

### Deploy to DigitalOcean App Platform
1. Connect your GitHub repository
2. Set environment variables
3. Configure build and run commands

## ⚠️ CRITICAL: Before Going Live

### 1. Security Checklist
- [ ] Change default admin password
- [ ] Set secure SECRET_KEY
- [ ] Disable debug mode
- [ ] Remove debug routes
- [ ] Set up HTTPS/SSL

### 2. Database Setup
- [ ] Consider upgrading from SQLite to PostgreSQL
- [ ] Set up database backups
- [ ] Initialize production database

### 3. Domain & DNS
- [ ] Purchase domain name
- [ ] Configure DNS settings
- [ ] Set up SSL certificate

### 4. Monitoring
- [ ] Set up application monitoring
- [ ] Configure error tracking
- [ ] Set up uptime monitoring

## 📊 Expected Costs

- **Heroku**: Free tier available, paid plans start at $7/month
- **Railway**: Free tier with usage limits, paid plans start at $5/month  
- **Render**: Free tier available, paid plans start at $7/month
- **Domain**: $10-15/year
- **SSL Certificate**: Free with Let's Encrypt

## 🆘 Need Help?

If you encounter issues during deployment:
1. Check Heroku logs: `heroku logs --tail`
2. Verify environment variables: `heroku config`
3. Test locally first with production settings
4. Consult platform-specific documentation