from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_super_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍💻 Adminlar", callback_data="superadmin:admins"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="superadmin:stat"),
        ],
        [
            InlineKeyboardButton(text="👤 Foydalanuvchilar", callback_data="superadmin:users")
        ],
        [
            InlineKeyboardButton(text="📝 Reklama yuborish", callback_data="superadmin:send_ads"),
        ]
    ]
)

users_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Bepul Webinar Qatnashchilari", callback_data="superadmin:free_webinar_users")
        ],
        [
            InlineKeyboardButton(text="👤 Pullik Kurs Qatnashchilari", callback_data="superadmin:paid_course_users")
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="superadmin:cancel")
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:cancel")
        ]
    ]
)
