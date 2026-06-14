from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

_FILTER_LABELS = {
    "video": "Video",
    "photo": "Foto",
    "audio": "Audio",
    "doc": "Dokumen",
}

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Unduh Tunggal", callback_data="menu_single"),
         InlineKeyboardButton("📦 Batch Download", callback_data="menu_batch")],
        [InlineKeyboardButton("⏩ Auto-Forward", callback_data="menu_auto")]
    ])

def get_caption_keyboard(message_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✂️ Hapus Baris Terakhir", callback_data=f"cap_rmlast_{message_id}"),
         InlineKeyboardButton("✅ Mulai", callback_data=f"cap_done_{message_id}")]
    ])

def get_filter_keyboard(selected_filters, message_id):
    filters = ["video", "photo", "audio", "doc"]

    if len(selected_filters) >= 4:
        selected_filters = []

    buttons = []
    for f in filters:
        label = _FILTER_LABELS[f]
        text = f"✅ {label}" if f in selected_filters else label
        buttons.append(InlineKeyboardButton(text, callback_data=f"filter_{f}_{message_id}"))

    if not selected_filters:
        bottom_button = InlineKeyboardButton("✅ Semua", callback_data=f"filter_all_{message_id}")
    else:
        bottom_button = InlineKeyboardButton("➡️ Lanjut", callback_data=f"filter_done_{message_id}")

    return InlineKeyboardMarkup([
        buttons[:2],
        buttons[2:],
        [bottom_button]
    ])

def get_destination_keyboard(msg_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Chat Bot", callback_data=f"batch_bot_{msg_id}"),
         InlineKeyboardButton("📢 Channel/Topik", callback_data=f"batch_chan_{msg_id}")]
    ])
