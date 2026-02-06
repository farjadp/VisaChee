# How to Use VisaChee Bot 📖

This guide will help you set up, run, and interact with the VisaChee Immigration Assessment Bot.

## 1. Prerequisites

-   Python 3.9 or higher installed on your system.
-   A Telegram account.
-   A Bot Token from [@BotFather](https://t.me/BotFather).

## 2. Configuration

1.  Open `main.py`.
2.  Locate the `TOKEN` variable inside the `main()` function.
3.  Ensure your valid Telegram Bot Token is pasted there:
    ```python
    TOKEN = "YOUR_API_TOKEN_HERE"
    ```
    *(Note: In the current version, the token is already pre-configured).*

## 3. Running the Bot

Open your terminal or command prompt, navigate to the project directory, and run:

```bash
python main.py
```

You should see the message: `Bot is polling...` indicating it is active.

## 4. Interacting with the Bot

1.  Open Telegram and search for your bot's username (e.g., `@visachee_bot`).
2.  Tap on **Start**.
3.  **Choose Your Path**:
    -   **⚡️ Quick Scan**: Select this for a fast check. You will be asked 5 binary questions.
    -   **🎮 Deep Dive**: Select this for a detailed assessment. You will progress through 4 levels of questions regarding your age, education, capital, and business strategy.
4.  **View Results**: At the end of either path, you will receive a scorecard showing your eligibility for the 5 target destinations.
5.  **Restart**: Click "🔄 Restart" to try again with different answers.

## 5. Troubleshooting

-   **Bot not responding?**
    -   Check your terminal to ensure the script is still running.
    -   Ensure your internet connection is stable.
    -   Restart the script (`Ctrl+C` to stop, then run `python main.py` again).
