# 🤖 Instagram Automation System

A **fully automated Instagram posting system** that generates quotes, creates videos, and uploads to Instagram with zero manual intervention using AI.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-orange.svg)](/.github/workflows/daily_post.yml)

## 🎬 Quick Demo

```bash
# Clone and run demo
git clone https://github.com/WasiRaza895/automation_insta.git
cd automation_insta
pip install -r requirements.txt
python demo.py
```

## 🚀 Run It NOW (Manual Test)

Want to see it work immediately? Follow these steps:

### Step 1: Clone the repository
```bash
git clone https://github.com/WasiRaza895/automation_insta.git
cd automation_insta
```

### Step 2: Install dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install imagemagick ffmpeg

# On macOS:
brew install imagemagick ffmpeg

# Fix ImageMagick security policy (Ubuntu/Debian):
sudo sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml
```

### Step 3: Set up your credentials
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use any text editor (vim, code, etc.)
```

Make sure to fill in:
- `GOOGLE_API_KEY` - Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `INSTAGRAM_USERNAME` - Your Instagram username
- `INSTAGRAM_PASSWORD` - Your Instagram password
- `INSTAGRAM_2FA_SEED` - (Optional) Only if you have 2FA enabled

**💡 Pro Tip:** Run `python list_gemini_models.py` to see which Gemini models are available for your API key, then update `config.yaml` accordingly.

### Step 4: Run it!
```bash
python run_now.py
```

### Step 5: Watch the magic happen! 🎬

The script will:
1. 📝 Generate a stoic quote with Gemini
2. 🎬 Create a video prompt
3. 🎥 Generate a cinematic video (or placeholder if Veo unavailable)
4. ✨ Add quote overlay in **1080x1920 Reel format** (9:16 vertical)
5. 📱 Upload to Instagram as a **Reel** (not regular post)
6. ✅ Done! Check your Instagram account!

**Expected output:**
```
🚀 Starting manual Instagram post...
==================================================
📝 Step 1/6: Generating Content with Gemini
✓ Quote: The obstacle is the way.
✓ Video Prompt: A serene mountain landscape...
🎬 Step 2/6: Video Generation (Cinematic)
✓ Video ready: output/video_20240131_120000.mp4
✨ Step 3/6: Video Processing (1080x1920 Reel Format)
✓ Final video: output/video_20240131_120000.mp4
📱 Step 4/6: Uploading to Instagram as Reel
✓ Reel uploaded successfully!
✅ SUCCESS! Your Reel is now live!
🔗 View it: https://instagram.com/your_username/
==================================================
✅ Done! Check your Instagram account.
```

### Alternative: Manual Trigger from GitHub Actions

You can also run it directly from GitHub:

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select "Daily Instagram Post" workflow
4. Click **Run workflow** button
5. (Optional) Check "Run in test mode" to skip upload
6. Click green **Run workflow** button
7. Watch it run in real-time!

This is perfect for testing without having to set up anything locally.

## ✨ Features

- 🎯 **AI-Powered Content Generation** - Uses Google Gemini to generate:
  - Stoic/minimalist quotes
  - Cinematic video prompts
  - Engaging captions with emojis
  - 25+ relevant hashtags
  - First comment suggestions

- 🎥 **Video Creation** - Automated video generation:
  - Placeholder videos with text overlays (MoviePy + ImageMagick)
  - Google Veo 3.1 integration ready (when API available)
  - **Proper Instagram Reel format: 1080x1920 (9:16 vertical)**
  - Automatic resize/crop from any source video
  - H.264 codec with AAC audio
  - 30 FPS, optimized for Instagram
  - Dark minimalist aesthetic

- 📱 **Instagram Auto-Upload** - Smart posting system:
  - Automatic login with session persistence
  - **Uploads as Instagram Reel** using `clip_upload()` (not regular video post)
  - Reel upload with captions and hashtags
  - 2FA support
  - Rate limiting and safety features
  - Human-like delays

- ⏰ **GitHub Actions Automation** - Fully automated scheduling:
  - Posts twice daily (9 AM & 7 PM UTC)
  - Manual trigger option
  - Comprehensive error handling
  - Logs and artifacts on failure

## 📋 Requirements

- Python 3.10+
- Instagram account (Business/Creator recommended)
- Google AI API key (Gemini)
- GitHub repository with Actions enabled

## 🚀 Setup Instructions

### 1. Fork/Clone Repository

```bash
git clone https://github.com/WasiRaza895/automation_insta.git
cd automation_insta
```

### 2. Install Dependencies (Local Testing)

```bash
# Install system dependencies
sudo apt-get install imagemagick ffmpeg  # Ubuntu/Debian
# brew install imagemagick ffmpeg        # macOS

# Fix ImageMagick security policy (Ubuntu/Debian)
sudo sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml

# Install Python packages
pip install -r requirements.txt
```

**Note:** The ImageMagick policy fix is required to allow text rendering on videos. On GitHub Actions, this is handled automatically in the workflow.

### 3. Configure GitHub Secrets

Go to your repository **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `GOOGLE_API_KEY` or `GEMINI_API_KEY` | Google AI API key | ✅ Yes |
| `INSTAGRAM_USERNAME` | Your Instagram username | ✅ Yes |
| `INSTAGRAM_PASSWORD` | Your Instagram password | ✅ Yes |
| `INSTAGRAM_2FA_SEED` | 2FA seed (if enabled) | ⚠️ Optional |

#### Getting Google AI API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create/select a project
3. Generate API key
4. Copy and add to GitHub Secrets

#### Getting 2FA Seed (Optional):
If you have 2FA enabled on Instagram:
1. When setting up 2FA, save the seed/secret key
2. Add it to `INSTAGRAM_2FA_SEED` secret
3. Format: Base32 encoded string (e.g., `JBSWY3DPEHPK3PXP`)

### 4. Configure Settings

Edit `config.yaml` to customize:

```yaml
content:
  theme: "stoic"           # stoic, motivational, minimalist
  quote_style: "short"     # short, medium, long
  hashtag_count: 25

video:
  duration: 15             # seconds
  font_size: 60
  text_color: "white"

safety:
  min_delay_seconds: 30
  max_delay_seconds: 120
  max_posts_per_day: 2
```

### 5. Test Your Setup

**Option A: Run Validation Tests**
```bash
python test_setup.py
```
This checks all dependencies and configuration.

**Option B: Run Demo (No API Keys Needed)**
```bash
python demo.py
```
This demonstrates all components with fallback content.

**Option C: Test Full Automation Locally**
```bash
# Set environment variables
export GOOGLE_API_KEY="your-key-here"
export INSTAGRAM_USERNAME="your-username"
export INSTAGRAM_PASSWORD="your-password"

# Run automation
python main.py
```

**Note**: For local testing without Instagram upload, comment out the upload section in `main.py`.

### 6. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows if not already enabled
3. Workflow will run automatically at scheduled times (9 AM & 7 PM UTC)
4. You can also trigger manually using "Run workflow" button

## 📁 Project Structure

```
automation_insta/
├── src/
│   ├── content_generator.py    # Gemini content generation
│   ├── video_generator.py      # Veo video generation (placeholder)
│   ├── video_processor.py      # MoviePy video processing
│   ├── instagram_uploader.py   # Instagram upload logic
│   ├── session_manager.py      # Login session management
│   └── utils.py                # Helper functions
├── .github/
│   └── workflows/
│       └── daily_post.yml      # GitHub Actions workflow
├── assets/
│   └── fonts/                  # Custom fonts (optional)
├── output/                     # Generated videos (gitignored)
├── sessions/                   # Session storage (gitignored)
├── config.yaml                 # Configuration file
├── requirements.txt            # Python dependencies
├── main.py                     # Main orchestrator
└── README.md                   # This file
```

## 🔒 Safety & Best Practices

### Rate Limiting
- Maximum 2 posts per day (configurable)
- Random delays between actions (30-120 seconds)
- Session persistence to avoid frequent logins

### Account Safety
- Use Instagram Business/Creator account
- Don't use your main personal account
- Start with lower frequency and gradually increase
- Monitor for any Instagram warnings

### Session Management
- Sessions are stored in `sessions/` directory (gitignored)
- Sessions persist across runs to avoid re-login
- Sessions auto-refresh when expired

## 🛠️ Troubleshooting

### Gemini API Issues

**1. Model 404 Error (Model Not Found):**
```
Error generating content: 404 NOT_FOUND. 'models/gemini-1.5-flash is not found for API version v1beta'
```
**Root Cause:**
- The Gemini model specified in your config is not available for your API key
- This can happen when:
  - Model name is outdated or incorrect
  - Model is not enabled for your API key/region
  - Model requires different permissions or subscription tier
  - Model is in beta and not available to all users

**Solution:**

**Step 1: List your available models**
```bash
# Run the helper script to see what models are available for your API key
python list_gemini_models.py
```

This will show you all models you can use with your API key.

**Step 2: Update config.yaml**
```yaml
api:
  gemini_model: "gemini-1.5-flash"  # Use a model from the list above
```

**Step 3: Common working models to try:**
- `gemini-1.5-flash` (recommended - fast and efficient)
- `gemini-1.5-pro` (more capable, may be slower)
- `gemini-pro` (stable, older version)
- `gemini-1.0-pro` (legacy, but widely available)

**For GitHub Actions:**
1. Update `config.yaml` with an available model
2. Commit and push the changes
3. The next workflow run will use the updated model

**Note:** The system will now automatically detect available models at runtime and suggest alternatives if your configured model is not found. It will fall back to static content generation if no suitable model is available.

**2. API Key Invalid:**
```
403 PERMISSION_DENIED or invalid API key
```
**Solution:**
- Verify your API key is set correctly:
  ```bash
  echo $GOOGLE_API_KEY  # Should show your key
  ```
- Get a new API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- For GitHub Actions: Add/update the `GOOGLE_API_KEY` secret in repository settings

**3. API Quota Exceeded:**
```
429 RESOURCE_EXHAUSTED
```
**Solution:**
- You've exceeded the free tier quota
- Wait for quota to reset (usually daily)
- Check quota at [Google AI Studio](https://aistudio.google.com/)
- Consider upgrading to paid tier for higher limits

### Instagram Login Issues

**1. Missing Credentials Error:**
```
ERROR: Instagram username and password are required
```
**Solution:**
- Ensure environment variables are set:
  ```bash
  export INSTAGRAM_USERNAME="your_username"
  export INSTAGRAM_PASSWORD="your_password"
  ```
- For GitHub Actions:
  - Go to Settings → Secrets and variables → Actions
  - Add `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` secrets
  - Secret names are case-sensitive!
- Verify secrets don't contain only whitespace

**2. 2FA NoneType Error:**
```
ERROR: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```
**Solution:**
- This occurs when 2FA is configured incorrectly
- **If you DON'T have 2FA on Instagram:**
  - Remove or leave `INSTAGRAM_2FA_SEED` empty
  - The system will automatically skip 2FA
- **If you DO have 2FA on Instagram:**
  - Get your 2FA seed when setting up authenticator app
  - Format: Base32 encoded string (e.g., `JBSWY3DPEHPK3PXP`)
  - Add to environment: `export INSTAGRAM_2FA_SEED="YOUR_SEED"`
  - For GitHub Actions: Add as secret `INSTAGRAM_2FA_SEED`
- The system now validates 2FA seeds before use

**3. Challenge Required:**
```
Instagram is asking for verification
```
**Solution:**
- Login to Instagram manually from the same network/IP
- Complete any verification challenges (email, SMS, etc.)
- Wait 24 hours before retrying automation
- Use a Business/Creator account (more automation-friendly)

**4. Rate Limited:**
```
Instagram is rate limiting
```
**Solution:**
- Wait 6-24 hours before trying again
- Reduce posting frequency in `config.yaml`:
  ```yaml
  safety:
    max_posts_per_day: 1  # Reduce from 2
    min_delay_seconds: 60  # Increase delays
    max_delay_seconds: 180
  ```
- Don't run the automation too frequently during testing

**5. Account Checkpoint:**
```
Account checkpoint detected
```
**Solution:**
- Your account needs verification
- Open Instagram app or website
- Follow the security checkpoint prompts
- May need to verify identity with email/phone

**6. IP Address Blacklisted / Action Blocked:**
```
Instagram API error: ... change your IP address, because it is added to the blacklist
```
or
```
Action blocked - suspicious activity detected
```

**Root Cause:**
- Instagram has flagged your IP address as suspicious or bot-like
- This commonly happens when:
  - Running automation from GitHub Actions (cloud/datacenter IPs are often flagged)
  - Using VPS or cloud hosting services
  - Multiple failed login attempts from the same IP
  - Rapid, bot-like activity patterns
  - First-time automation from a new IP address

**Solutions:**

**Option 1: Run from a Trusted Local IP (Recommended)**
```bash
# 1. Clone the repository locally
git clone https://github.com/WasiRaza895/automation_insta.git
cd automation_insta

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
export INSTAGRAM_USERNAME='your_username'
export INSTAGRAM_PASSWORD='your_password'
export GOOGLE_API_KEY='your_api_key'

# 4. Run from your home/mobile network (NOT VPN or proxy)
python run_now.py
```

**Option 2: Recover Your Instagram Account**
1. Open Instagram app or website from a trusted device
2. Complete any security challenges or verifications
3. You may need to:
   - Verify via email or SMS
   - Reset your password
   - Confirm your identity
4. **Wait 24-48 hours** before attempting automation again
5. Do NOT keep retrying from the blocked IP

**Option 3: Prevent Future Blocks**
1. **Use Instagram Business/Creator account** (more tolerant of automation)
2. **Reduce posting frequency** in `config.yaml`:
   ```yaml
   safety:
     max_posts_per_day: 1  # Start with just 1 post per day
     min_delay_seconds: 120  # Increase delays significantly
     max_delay_seconds: 300
   ```
3. **Build account trust first:**
   - Post manually from Instagram mobile app for 3-7 days
   - Like, comment, and engage normally
   - Verify account with phone number and email
   - Avoid sudden automation from a new IP
4. **For GitHub Actions users:**
   - Consider running automation less frequently (once per day max)
   - Or switch to local execution from a residential IP
   - GitHub runner IPs are often pre-flagged by Instagram

**⚠️ CRITICAL WARNINGS:**
- **DO NOT** keep retrying from the same blocked IP (makes it worse)
- **DO NOT** use multiple accounts from the same blocked IP
- **DO NOT** ignore Instagram's security warnings
- **DO NOT** use aggressive retry logic
- Repeated violations may lead to **permanent account ban**

**Understanding IP Blocks:**
Instagram uses sophisticated bot detection that flags:
- Datacenter/cloud IP addresses (AWS, Azure, Google Cloud, GitHub)
- IPs with history of abuse or automation
- Sudden activity from unfamiliar locations
- Patterns that don't match normal human behavior

The best approach is to establish trust gradually:
1. Start with manual posts from your normal device/network
2. Gradually introduce automation from a residential IP
3. Keep frequency low and delays high
4. Monitor for any Instagram warnings

### GitHub Actions Workflow Failures

**Common Issues:**

1. **2FA Authentication Error:**
   ```
   ERROR: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
   ```
   **Solution:** 
   - If you don't have 2FA enabled on Instagram, leave `INSTAGRAM_2FA_SEED` secret empty or remove it
   - If you do have 2FA enabled, ensure the secret is set correctly with your base32-encoded 2FA seed
   - The workflow will now automatically handle missing/empty 2FA seeds

2. **Missing Secrets:**
   ```
   ERROR: Instagram username and password are required
   ```
   **Solution:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add all required secrets: `GOOGLE_API_KEY` (or `GEMINI_API_KEY`), `INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`
   - Verify secret names match exactly (case-sensitive)

3. **ImageMagick Policy Error:**
   ```
   attempt to perform an operation not allowed by the security policy
   ```
   **Solution:** This is automatically fixed in the workflow. If running locally, see the "Video Processing Issues" section below.

4. **Python Package Installation Failure:**
   - Check the "Install Python dependencies" step in workflow logs
   - Ensure `requirements.txt` is valid and all packages are available
   - The workflow installs Python 3.10 - some packages may have compatibility issues

5. **Video Upload Failure:**
   - Instagram may rate limit or challenge your account
   - Use a Business/Creator account (less restrictive)
   - Reduce posting frequency in `config.yaml`
   - Check if account requires manual verification

**Debugging Steps:**
1. Go to Actions tab and select the failed workflow run
2. Check "Run Instagram automation" step for detailed error logs
3. Review "Print environment info" step to verify dependencies
4. Download artifacts (logs and output files) if available
5. Test locally first: `python run_now.py` to reproduce the issue

### Environment Variable Debugging

The system now logs which environment variables are detected (without exposing values):

```
Environment variable status:
  INSTAGRAM_USERNAME: ✓ SET
  INSTAGRAM_PASSWORD: ✓ SET
  INSTAGRAM_2FA_SEED: ○ NOT SET (2FA disabled)
```

If you see `✗ NOT SET` for required variables, that's the issue.

### Login Issues

**Challenge Required:**
```
Instagram is asking for verification. Please verify your account manually.
```
- Login to Instagram manually from the same IP
- Complete any verification challenges
- Try again after 24 hours

**Rate Limited:**
```
Instagram is rate limiting. Please wait and try again later.
```
- Wait 6-24 hours before trying again
- Reduce posting frequency in config
- Increase delay ranges

### Video Processing Issues

**ImageMagick Policy Error:**
```
attempt to perform an operation not allowed by the security policy
```
Edit `/etc/ImageMagick-6/policy.xml` and modify:
```xml
<policy domain="path" rights="none" pattern="@*" />
```
to:
```xml
<policy domain="path" rights="read|write" pattern="@*" />
```

### API Issues

**Gemini API Error:**
- Check API key is valid
- Verify API quota hasn't been exceeded
- Check API is enabled in Google Cloud Console

## 📊 Monitoring

### Check Workflow Status
1. Go to **Actions** tab
2. View run history and logs
3. Download artifacts on failure

### View Logs
```bash
# In GitHub Actions logs
# Or locally when testing
tail -f *.log
```

## ⚠️ Disclaimer

This tool is for educational purposes. Use responsibly and in accordance with:
- [Instagram Terms of Service](https://help.instagram.com/581066165581870)
- [Instagram Community Guidelines](https://help.instagram.com/477434105621119)
- Automated behavior may violate Instagram's ToS
- Use at your own risk
- Author is not responsible for account bans or restrictions

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Credits

Built with:
- [Google Gemini AI](https://ai.google.dev/)
- [instagrapi](https://github.com/adw0rd/instagrapi)
- [MoviePy](https://github.com/Zulko/moviepy)
- [ImageMagick](https://imagemagick.org/)

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section above

---

**Made with ❤️ using AI**