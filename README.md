# 🚀 X1 EcoChain BOT


## 🎯 Overview

X1 EcoChain BOT is an automated tool designed to streamline onchain operations across multiple accounts. It provides seamless integration with X1 EcoChain network and offers robust proxy support for enhanced security and reliability.

**🔗 Get Started:** [Register on X1 EcoChain](https://testnet.x1ecochain.com/)

> **Important:** Connect new evm wallet.

## ✨ Features

- 🔄 **Automated Account Management** - Retrieve account information automatically
- 🌐 **Flexible Proxy Support** - Run with or without proxy configuration
- 🔀 **Smart Proxy Rotation** - Automatic rotation of invalid proxies
- 🚰 **Claim Test Token** - Automated claim daily XIT Faucet
- ⏰ **Daily Check-In** – Automated perform daily check-in
- 📜 **Quests Completion** – Automated complete available quests
- 👥 **Multi-Account Support** - Manage multiple accounts simultaneously

## 📋 Requirements

- **Python:** Version 3.9 or higher
- **pip:** Latest version recommended
- **Compatible libraries:** eth-account and eth-utils(see requirements.txt)

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dopezayn/X1-Ecochain-BOT.git
cd X1-Ecochain-BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
# or for Python 3 specifically
pip3 install -r requirements.txt
```

### 3. Library Version Management

> ⚠️ **Important:** Ensure library versions match those specified in `requirements.txt`

**Check installed library version:**
```bash
pip show library_name
```

**Uninstall conflicting library:**
```bash
pip uninstall library_name
```

**Install specific library version:**
```bash
pip install library_name==version
```

## ⚙️ Configuration

### Account Setup

Create or edit `accounts.txt` in the project directory:

```
your_private_key_1
your_private_key_2
your_private_key_3
```

### Proxy Configuration (Optional)

Create or edit `proxy.txt` in the project directory:

```
# Simple format (HTTP protocol by default)
192.168.1.1:8080

# With protocol specification
http://192.168.1.1:8080
https://192.168.1.1:8080

# With authentication
http://username:password@192.168.1.1:8080
```

## 🚀 Usage

Run the bot using one of the following commands:

```bash
python bot.py
# or for Python 3 specifically
python3 bot.py
```

### Runtime Options

When starting the bot, you'll be prompted to choose:

1. **Proxy Mode Selection:**
   - Option `1`: Run with proxy
   - Option `2`: Run without proxy

2. **Auto-Rotation:** 
   - `y`: Enable automatic invalid proxy rotation
   - `n`: Disable auto-rotation

## 💖 Support the Project

If this project has been helpful to you, consider supporting its development:


## 📞 Contact & Support

- **Developer:** AkHii


---

<div align="center">

**Made with ❤️ by [Akhii](https://github.com/dopezayn)**

*Thank you for using X1 EcoChain BOT! Don't forget to ⭐ star this repository.*

</div>
