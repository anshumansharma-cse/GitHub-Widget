***

# _GitHub Commit History Widget_

## Purpose
- Nothing fuels motivation quite like seeing your own GitHub commit history.
- While GitHub offers a homescreen widget for mobile devices (Android & iOS), there is no native equivalent for desktop environments.
- This project is an attempt to create an 'ever-present', interactive GitHub commit history desktop widget for developers.

## Features
- **Always Visible:** Floats natively on your desktop environment.
- **Resilient Engine:** Built with TCP connection pooling, exponential backoff, and graceful degradation to handle network drops without crashing.
- **Private Repo Support:** Securely track both public and private repository contributions.

## Scope
- The initial releases are exclusively built and optimized for macOS.
- Windows and Linux (for specific desktop environments) versions are on the roadmap.

---

## Requirements & Setup (macOS)

### 1. Install Core Dependencies
If you do not have Homebrew installed, open your terminal and run:
```bash
# Install Xcode command line tools
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

# Add Homebrew to your PATH (Run these exactly as they appear in your terminal output)
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify your installation by running `brew doctor`.

Next, install Git and the `uv` Python package manager:
```bash
brew install git
brew install uv
```

### 2. Clone the Repository
```bash
git clone https://github.com/anshumansharma-cse/GitHub-Widget.git
cd GitHub-Widget
```

### 3. Configuration & Authentication
Before running the widget, you must configure it to track your specific account.

**Public Repositories Only:**
1. Open `Commit_History_Widget/main.py`.
2. Locate the Configuration block at the top and change `GITHUB_USERNAME` to your actual GitHub handle.

**🔐 Private Repositories (Optional but Recommended):**
If you want the widget to track your private code, you must provide a Personal Access Token (PAT).
1. Create a hidden file at the project root level:
   ```bash
   touch .env
   ```
2. Generate a classic PAT in your GitHub Developer Settings with `repo` scopes.
3. Inside the `.env` file, paste your token exactly like this (sample):
   ```text
   GITHUB_PAT=ghp_YourSecretTokenHere
   ```

### 4. Build the Environment
Use `uv` to instantly build an isolated, pristine Python 3.12 environment and install the required dependencies:
```bash
# Fetch Python 3.12 and build the environment
uv venv --python 3.12

# Activate the environment
source .venv/bin/activate

# Install project requirements
uv pip install -r requirements.txt
```

### 5. Launch the Widget
Move into the application directory and start the engine:
```bash
cd Commit_History_Widget
uv run main.py