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
  - 9:16 aspect ratio for Instagram Reels
  - Dark minimalist aesthetic

- 📱 **Instagram Auto-Upload** - Smart posting system:
  - Automatic login with session persistence
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