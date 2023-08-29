from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_user = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text="🛒 Sotib Olish", callback_data="user:buy")
        # ],
        # [
        #     InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="user:settings")
        # ],
        [
            InlineKeyboardButton(text="🆘 Yordam", callback_data="user:help"),
        ]
    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Tilni o'zgartirish",
                                 callback_data="user:change_language")
        ],
        [
            InlineKeyboardButton(text="👛 Hamyonni o'zgartirish", callback_data="user:change_wallet")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:back")
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ]
    ]
)


back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

isCorrect = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ To'g'ri", callback_data="user:isCorrect")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ]
    ]
)

latin_region_btn = InlineKeyboardMarkup(row_width=1)
latin_region_btn.add(InlineKeyboardButton(text="🇺🇿 Toshkent shahri", callback_data="region:tsh"),
                     InlineKeyboardButton(text="🇺🇿 Toshkent viloyati", callback_data="region:tv"),
                     InlineKeyboardButton(text="🇺🇿 Andijon viloyati", callback_data="region:av"),
                     InlineKeyboardButton(text="🇺🇿 Buxoro viloyati", callback_data="region:bv"),
                     InlineKeyboardButton(text="🇺🇿 Farg'ona viloyati", callback_data="region:fv"),
                     InlineKeyboardButton(text="🇺🇿 Jizzax viloyati", callback_data="region:jv"),
                     InlineKeyboardButton(text="🇺🇿 Namangan viloyati", callback_data="region:nv"),
                     InlineKeyboardButton(text="🇺🇿 Navoiy viloyati", callback_data="region:nav"),
                     InlineKeyboardButton(text="🇺🇿 Qashqadaryo viloyati",
                                          callback_data="region:qv"),
                     InlineKeyboardButton(text="🇺🇿 Samarqand viloyati", callback_data="region:sv"),
                     InlineKeyboardButton(text="🇺🇿 Sirdaryo viloyati", callback_data="region:sirv"),
                     InlineKeyboardButton(text="🇺🇿 Surxondaryo viloyati",
                                          callback_data="region:surv"),
                     InlineKeyboardButton(text="🇺🇿 Xorazm viloyati", callback_data="region:xv"),
                     InlineKeyboardButton(text="🇺🇿 Qoraqalpog'iston Respublikasi",
                                          callback_data="region:qorv")
                     )

uz_cyrillic_region_btn = InlineKeyboardMarkup(row_width=1)
uz_cyrillic_region_btn.add(InlineKeyboardButton(text="🇺🇿 Тошкент шаҳри", callback_data="region:tsh"),
                           InlineKeyboardButton(text="🇺🇿 Тошкент вилояти", callback_data="region:tv"),
                           InlineKeyboardButton(text="🇺🇿 Андижон вилояти", callback_data="region:av"),
                           InlineKeyboardButton(text="🇺🇿 Бухоро вилояти", callback_data="region:bv"),
                           InlineKeyboardButton(text="🇺🇿 Фарғона вилояти", callback_data="region:fv"),
                           InlineKeyboardButton(text="🇺🇿 Жиззах вилояти", callback_data="region:jv"),
                           InlineKeyboardButton(text="🇺🇿 Наманган вилояти", callback_data="region:nv"),
                           InlineKeyboardButton(text="🇺🇿 Навоий вилояти", callback_data="region:nav"),
                           InlineKeyboardButton(text="🇺🇿 Қашқадарё вилояти",
                                                callback_data="region:qv"),
                           InlineKeyboardButton(text="🇺🇿 Самарқанд вилояти", callback_data="region:sv"),
                           InlineKeyboardButton(text="🇺🇿 Сирдарё вилояти", callback_data="region:sirv"),
                           InlineKeyboardButton(text="🇺🇿 Сурхондарё вилояти",
                                                callback_data="region:surv"),
                           InlineKeyboardButton(text="🇺🇿 Хоразм вилояти", callback_data="region:xv"),
                           InlineKeyboardButton(text="🇺🇿 Қорақалпоғистон Республикаси",
                                                callback_data="region:qorv")
                           )
