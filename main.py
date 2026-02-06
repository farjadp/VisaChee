import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from questions import BotText
from logic import calculate_score, format_results

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- STATES ---
(
    CHOOSING_PATH,
    QUICK_Q1, QUICK_Q2, QUICK_Q3, QUICK_Q4, QUICK_Q5,
    DEEP_LEVEL_1, DEEP_LEVEL_2, DEEP_LEVEL_3, DEEP_LEVEL_4
) = range(10)

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point: /start command"""
    # Reset user data
    context.user_data.clear()
    
    keyboard = [
        [InlineKeyboardButton(BotText.CHOOSE_PATH_BUTTONS["A"], callback_data="path_a")],
        [InlineKeyboardButton(BotText.CHOOSE_PATH_BUTTONS["B"], callback_data="path_b")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(BotText.WELCOME, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        # If triggered via restart/callback
        await update.callback_query.message.edit_text(BotText.WELCOME, reply_markup=reply_markup, parse_mode="Markdown")
        
    return CHOOSING_PATH

async def choose_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "path_a":
        context.user_data['path'] = 'A'
        return await ask_quick_question(update, context, 0)
    elif choice == "path_b":
        context.user_data['path'] = 'B'
        context.user_data['deep_q_idx'] = 0 # Track question index within levels
        context.user_data['level_idx'] = 1  # Track current level
        return await start_deep_level(update, context, 1)

# --- PATH A: QUICK SCAN HANDLERS ---

async def ask_quick_question(update: Update, context: ContextTypes.DEFAULT_TYPE, q_index):
    """Asks a question from the Quick Scan list based on index."""
    if q_index >= len(BotText.QUICK_QUESTIONS):
        return await show_quick_results(update, context)

    q_data = BotText.QUICK_QUESTIONS[q_index]
    context.user_data['current_q_idx'] = q_index
    
    keyboard = []
    for label, value in q_data['options']:
        keyboard.append([InlineKeyboardButton(label, callback_data=value)])
    
    text = f"⚡️ *Question {q_index + 1}/{len(BotText.QUICK_QUESTIONS)}*\n\n{q_data['text']}"
    
    await update.callback_query.message.edit_text(
        text, 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )
    
    # Return the state corresponding to the NEXT interaction
    # For simplicity in this demo, sharing one state handler or using specific states
    # We will use specific states for clarity in flow
    return QUICK_Q1 + q_index 

async def handle_quick_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    q_idx = context.user_data.get('current_q_idx', 0)
    answer = query.data
    
    # Store Answer
    q_id = BotText.QUICK_QUESTIONS[q_idx]['id']
    context.user_data[q_id] = answer
    
    # Move to next
    return await ask_quick_question(update, context, q_idx + 1)

async def show_quick_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Calculate scores and get the archetype message
    scores, messages = calculate_score(context.user_data)
    
    # The first message in the list is the main archetype result
    main_message = messages[0]
        
    # Format the full result utilizing the helper, although format_results now just expects the same structure
    result_details = format_results(scores, messages)
    
    keyboard = [[InlineKeyboardButton(BotText.CONTACT_ADMIN, callback_data="contact_info")]]
    # Add Deep Dive Button
    keyboard.append([InlineKeyboardButton(BotText.BUTTON_DEEP_DIVE, callback_data="start_deep_dive")])
    keyboard.append([InlineKeyboardButton(BotText.RESTART, callback_data="restart")])
    
    await update.callback_query.message.edit_text(
        result_details, 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def start_deep_from_quick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transition from Quick Scan Result to Deep Dive."""
    query = update.callback_query
    await query.answer()
    
    # Initialize Deep Dive settings
    context.user_data['path'] = 'B'
    context.user_data['level_idx'] = 1
    context.user_data['deep_q_idx'] = 0
    
    # Start Level 1
    return await start_deep_level(update, context, 1)

# --- PATH B: DEEP DIVE HANDLERS ---

def get_level_questions(level_str):
    return BotText.LEVELS[level_str]["questions"]

async def start_deep_level(update: Update, context: ContextTypes.DEFAULT_TYPE, level_num):
    """Initialize a level or ask first question of level."""
    context.user_data['level_idx'] = level_num
    context.user_data['deep_q_idx'] = 0
    level_str = str(level_num)
    
    # Intro to Level
    level_name = BotText.LEVELS[level_str]["name"]
    await update.callback_query.message.edit_text(f"🚀 Entering *{level_name}*...", parse_mode="Markdown")
    
    # Ask first question of this level
    return await ask_deep_question(update, context)

async def ask_deep_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level_num = context.user_data['level_idx']
    q_idx = context.user_data['deep_q_idx']
    level_str = str(level_num)
    
    questions = get_level_questions(level_str)
    
    # Check if level finished
    if q_idx >= len(questions):
        # Move to next level
        if level_num < 4:
            return await start_deep_level(update, context, level_num + 1)
        else:
            return await show_deep_results(update, context)

    q_data = questions[q_idx]
    
    keyboard = []
    for label, value in q_data['options']:
        keyboard.append([InlineKeyboardButton(label, callback_data=value)])
    
    progress = f"(Level {level_num}/4 • Q{q_idx+1})"
    text = f"{progress}\n{q_data['text']}"
    
    await update.callback_query.message.edit_text(
        text, 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )
    
    # Map level to state
    # Level 1 -> DEEP_LEVEL_1, etc.
    return DEEP_LEVEL_1 + (level_num - 1)

async def handle_deep_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    level_num = context.user_data['level_idx']
    q_idx = context.user_data['deep_q_idx']
    level_str = str(level_num)
    
    questions = get_level_questions(level_str)
    q_id = questions[q_idx]['id']
    answer = query.data
    
    # Store
    context.user_data[q_id] = answer
    
    # increment
    context.user_data['deep_q_idx'] += 1
    
    return await ask_deep_question(update, context)

async def show_deep_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scores, messages = calculate_score(context.user_data)
    result_text = format_results(scores, messages)
    
    keyboard = [[InlineKeyboardButton(BotText.CONTACT_ADMIN, callback_data="contact_info")]]
    keyboard.append([InlineKeyboardButton(BotText.RESTART, callback_data="restart")])

    await update.callback_query.message.edit_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def contact_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows contact details."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton(BotText.RESTART, callback_data="restart")]]
    
    await query.message.edit_text(
        BotText.CONTACT_DETAILS,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    return ConversationHandler.END

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart conversation loop"""
    query = update.callback_query
    await query.answer()
    return await start(update, context)

# --- MAIN SETUP ---

def main():
    # PLACEHOLDER: Get token from env or user
    TOKEN = "8231330084:AAEpJ-NzjaPLedEUs7IPLqcEBYDaXRyLgqA" 
    
    application = ApplicationBuilder().token(TOKEN).build()

    # Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(restart, pattern="^restart$"),
            CallbackQueryHandler(contact_info_handler, pattern="^contact_info$"),
            CallbackQueryHandler(start_deep_from_quick, pattern="^start_deep_dive$")
        ],
        states={
            CHOOSING_PATH: [
                CallbackQueryHandler(choose_path, pattern="^path_")
            ],
            # Path A States
            QUICK_Q1: [CallbackQueryHandler(handle_quick_answer)],
            QUICK_Q2: [CallbackQueryHandler(handle_quick_answer)],
            QUICK_Q3: [CallbackQueryHandler(handle_quick_answer)],
            QUICK_Q4: [CallbackQueryHandler(handle_quick_answer)],
            QUICK_Q5: [CallbackQueryHandler(handle_quick_answer)],
            
            # Path B States
            DEEP_LEVEL_1: [CallbackQueryHandler(handle_deep_answer)],
            DEEP_LEVEL_2: [CallbackQueryHandler(handle_deep_answer)],
            DEEP_LEVEL_3: [CallbackQueryHandler(handle_deep_answer)],
            DEEP_LEVEL_4: [CallbackQueryHandler(handle_deep_answer)],
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(restart, pattern="^restart$")
        ]
    )

    application.add_handler(conv_handler)
    
    print("Bot is polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
