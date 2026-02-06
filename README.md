# VisaChee Immigration Assessment Bot 🌍

A value-driven, interactive Telegram Bot designed to assess immigration eligibility for entrepreneurs and skilled professionals.

## 🚀 Features

-   **Dual-Track Assessment**:
    -   ⚡️ **Quick Scan**: Tinder-style, fast binary choices for immediate feedback.
    -   🎮 **Deep Dive**: Gamified 4-level assessment (Profile, Capital, Strategy, History).
-   **Smart Scoring**: Weighted algorithms for 5 target destinations:
    -   🇳🇱 Netherlands
    -   🇫🇮 Finland
    -   🇩🇰 Denmark
    -   🇦🇪 UAE (Golden Visa)
    -   🇨🇦 Canada (Startup/PNP)
-   **Modularity**: Separation of content (`questions.py`), logic (`logic.py`), and bot handling (`main.py`).

## 🛠 Tech Stack

-   **Python 3.9+**
-   **python-telegram-bot** (v20+ Async)
-   **Persistence**: In-memory (State Machine)

## 📂 Project Structure

```
VisaChee/
├── main.py        # Entry point: Bot handlers & conversation states
├── logic.py       # Business logic: Scoring & constraints
├── questions.py   # Content: Questions, text strings, & configurations
├── README.md      # Project overview
├── CHANGELOG.md   # Version history
└── HOW_TO_USE.md  # User guide
```

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/farjadp/VisaChee.git
    cd VisaChee
    ```

2.  **Install Dependencies**:
    ```bash
    pip install python-telegram-bot
    ```

3.  **Run the Bot**:
    ```bash
    python main.py
    ```

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
