# 🎵 J TOK - TikTok Username Finder

A powerful Python tool to discover and check the availability of 2-4 character TikTok usernames automatically.

## Features ✨

- 🔍 **Automated Username Generation** - Generates all possible 2-4 character combinations
- ⚡ **Multi-threaded Search** - 15 parallel threads for faster checking
- 📊 **Real-time Progress** - Live progress bar with statistics
- 💾 **Auto Save Results** - Saves found usernames to a timestamped file
- 🎨 **Beautiful UI** - Colorful terminal interface with detailed feedback
- 🚀 **Easy to Use** - Simple one-command execution

## Installation 📦

```bash
git clone https://github.com/j3had/JE.TOK.git
cd JE.TOK
pip install colorama requests
```

## Usage 🚀

```bash
python tiktok_guesser.py
```

The tool will:
1. Generate 2-4 character usernames automatically
2. Check availability on TikTok in parallel
3. Display available usernames in real-time
4. Save results to a file when complete

## Output Example 📋

```
✓ FOUND! [1] @ab is available! 🎉
✓ FOUND! [2] @xyz is available! 🎉
✓ FOUND! [3] @j3 is available! 🎉
```

Results are saved as: `J_TOK_usernames_YYYYMMDD_HHMMSS.txt`

## Requirements 📋

- Python 3.6+
- `requests` - HTTP library
- `colorama` - Terminal colors

## How It Works 🔧

1. **Username Generation** - Creates all combinations of lowercase letters and digits
2. **Availability Check** - Sends requests to TikTok for each username
3. **Content Verification** - Analyzes response to confirm user exists
4. **Parallel Processing** - Uses threading for faster results
5. **Results Storage** - Saves found usernames locally

## Performance ⚡

- Generates ~45,000 usernames (2-4 chars)
- Checks multiple usernames simultaneously
- Average time: 30-60 minutes depending on connection
- Can be interrupted with `Ctrl+C`

## Notes ⚠️

- Respects rate limits and delays
- Use responsibly and ethically
- Some short usernames may already be taken
- Results depend on TikTok's API availability

## License 📄

MIT License - Feel free to use and modify

## Author 👨‍💻

**J3HAD**

---

⭐ If you find this useful, please star the repository!

🔗 [GitHub Repository](https://github.com/j3had/JE.TOK.git)
