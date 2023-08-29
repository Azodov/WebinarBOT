from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes

from data.config import ADMINS
from filters import IsGuest
from keyboards.inline.userKeyboards import latin_region_btn, uz_cyrillic_region_btn
from loader import dp, db, bot


@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    else:
        lang_btn = InlineKeyboardMarkup(row_width=1)
        lang_btn.add(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz_latin"),
                     InlineKeyboardButton(text="🇺🇿 Ўзбекча", callback_data="lang:uz_cyrillic"),
                     )

        await message.answer(f"👋Assalomu alaykum Bot tilini tanlang...\n"
                             f"👋Ассалому алайкум Бот тилини танланг...", reply_markup=lang_btn)
        await state.set_state("get_lang")


@dp.callback_query_handler(IsGuest(), text_contains="lang:", state="get_lang")
async def get_lang(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    lang = call.data.split(":")[-1]
    await state.update_data(lang=lang)
    if lang == "uz_latin":
        await call.message.edit_text("😊 Juda soz endi viloyatingizni tanlang...", reply_markup=latin_region_btn)
        await state.set_state("get_region")
    elif lang == "uz_cyrillic":
        await call.message.edit_text("😊 Жуда соз энди вилоятингизни танланг...", reply_markup=uz_cyrillic_region_btn)
    await state.set_state("get_region")


@dp.callback_query_handler(IsGuest(), text_contains="region:", state="get_region")
async def get_region(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    await call.answer(cache_time=1)
    region = call.data.split(":")[-1]
    if region == "tsh":
        region = "Toshkent shahri"
    elif region == "tv":
        region = "Toshkent viloyati"
    elif region == "av":
        region = "Andijon viloyati"
    elif region == "bv":
        region = "Buxoro viloyati"
    elif region == "fv":
        region = "Farg'ona viloyati"
    elif region == "jv":
        region = "Jizzax viloyati"
    elif region == "nv":
        region = "Namangan viloyati"
    elif region == "nav":
        region = "Navoiy viloyati"
    elif region == "qv":
        region = "Qashqadaryo viloyati"
    elif region == "sv":
        region = "Samarqand viloyati"
    elif region == "sirv":
        region = "Sirdaryo viloyati"
    elif region == "surv":
        region = "Surxondaryo viloyati"
    elif region == "xv":
        region = "Xorazm viloyati"
    elif region == "qorv":
        region = "Qoraqalpog'iston Respublikasi"
    await state.update_data(region=region)
    if lang == "uz_latin":
        await call.message.edit_text("✍️ Iltimos to'liq ismingizni kiriting...")
    elif lang == "uz_cyrillic":
        await call.message.edit_text("✍️ Илтимос тўлиқ исмингизни киритинг...")

    await state.set_state("get_fullname")


@dp.message_handler(IsGuest(), state="get_fullname")
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    data = await state.get_data()
    lang = data["lang"]
    if lang == "uz_latin":
        await message.answer("📞 Iltimos telefon raqamingizni kiriting...")
    elif lang == "uz_cyrillic":
        await message.answer("📞 Илтимос телефон рақамингизни киритинг...")
    await state.set_state("get_phone_number")


@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.CONTACT)
@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
    else:
        await state.update_data(phone_number=message.text)
    data = await state.get_data()
    lang = data["lang"]
    if lang == "uz_latin":
        service_btn = InlineKeyboardMarkup(row_width=1)
        service_btn.add(
            InlineKeyboardButton(text="🆓 Bepul Webinarga ro'yxatdan o'tish", callback_data="service:free_webinar"),
            InlineKeyboardButton(text="🆙 Online 20 kunlik Kurs uchun ro'yxatdan o'tish",
                                 callback_data="service:online_course"),
        )

        await message.answer("🔀 Xizmat turini tanlang...", reply_markup=service_btn)
    elif lang == "uz_cyrillic":
        service_btn = InlineKeyboardMarkup(row_width=1)
        service_btn.add(
            InlineKeyboardButton(text="🆓 Бепул Вебинарга рўйхатдан ўтиш", callback_data="service:free_webinar"),
            InlineKeyboardButton(text="🆙 Онлайн 20 кунлик Курс учун рўйхатдан ўтиш",
                                 callback_data="service:online_course"),
        )
        await message.answer("🔀 Xизмат турини танланг...", reply_markup=service_btn)
    await state.set_state("get_service")


@dp.callback_query_handler(IsGuest(), text_contains="service:", state="get_service")
async def get_service(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    service = call.data.split(":")[-1]
    await state.update_data(service=service)
    lang = data["lang"]
    region = data["region"]
    fullname = data["fullname"]
    phone_number = data["phone_number"]
    if service == "free_webinar":
        await db.add_user(telegram_id=int(call.from_user.id), language=lang, region=region, fullname=fullname,
                          phone_number=phone_number, selected_service=service, amount_paid="0")
        if lang == "uz_latin":
            await call.message.edit_text("✅ Sizning so'rovingiz qab☺ul qilindi. Tez orada siz bilan bog'lanamiz...")
        elif lang == "uz_cyrillic":
            await call.message.edit_text("✅ Сизнинг сўровингиз қабул қилинди. Тез орада сиз билан боғланамиз...")
        text_for_admin = (f"👤 Foydalanuvchi: {fullname}\n"
                          f"📞 Telefon raqami: {phone_number}\n"
                          f"📍 Viloyati: {region}\n"
                          f"📝 Xizmat turi: Bepul Webinar\n"
                          f"📅 Vaqt: {call.message.date}\n"
                          f"🇺🇿 Til: O'zbek Tili\n")
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=text_for_admin)
    elif service == "online_course":
        if lang == "uz_latin":
            payment_methods_btn = InlineKeyboardMarkup(row_width=1)
            payment_methods_btn.add(
                InlineKeyboardButton(text="💳 Karta orqali to'lash", callback_data="payment_method:card"),
                InlineKeyboardButton(text="💵 Naqd pul orqali to'lash", callback_data="payment_method:cash"),
            )
            text = "😊 To'lov turini tanlang...\n"
            await call.message.edit_text(text, reply_markup=payment_methods_btn)

        elif lang == "uz_cyrillic":
            payment_methods_btn = InlineKeyboardMarkup(row_width=1)
            payment_methods_btn.add(
                InlineKeyboardButton(text="💳 Карта орқали тўлаш", callback_data="payment_method:card"),
                InlineKeyboardButton(text="💵 Нақд пул орқали тўлаш", callback_data="payment_method:cash"),
            )
            text = "😊 Тўлов турини танланг...\n"
            await call.message.edit_text(text, reply_markup=payment_methods_btn)
        await state.set_state("get_payment_method")


@dp.callback_query_handler(IsGuest(), text_contains="payment_method:", state="get_payment_method")
async def get_payment_method(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    payment_method = call.data.split(":")[-1]
    lang = data["lang"]
    phone_number = data["phone_number"]
    region = data["region"]
    fullname = data["fullname"]
    service = data["service"]
    if payment_method == "card":
        await state.update_data(payment_method="card")
        if lang == "uz_latin":
            summ_btn = InlineKeyboardMarkup(row_width=1)
            summ_btn.add(
                InlineKeyboardButton(text="💵 200.000 so'm (Boshlang'ich summa)", callback_data="amount_paid:200000"),
                InlineKeyboardButton(text="💵 600.000 so'm", callback_data="amount_paid:600000"),
                InlineKeyboardButton(text="💵 900.000 so'm", callback_data="amount_paid:900000"),
                InlineKeyboardButton(text="💵 1.500.000 so'm", callback_data="amount_paid:1500000"),
                InlineKeyboardButton(text="💵 2.000.000 so'm(To'liq)", callback_data="amount_paid:2000000"),
            )
            await call.message.edit_text("😊 To'lov summasini tanlang...\n"
                                         "Eng kam boshlang'ich summa 200.000 so'm", reply_markup=summ_btn)
            await state.set_state("get_amount_paid")
        elif lang == "uz_cyrillic":
            summ_btn = InlineKeyboardMarkup(row_width=1)
            summ_btn.add(
                InlineKeyboardButton(text="💵 200.000 сўм (Бошланғич сумма)", callback_data="amount_paid:200000"),
                InlineKeyboardButton(text="💵 600.000 сўм", callback_data="amount_paid:600000"),
                InlineKeyboardButton(text="💵 900.000 сўм", callback_data="amount_paid:900000"),
                InlineKeyboardButton(text="💵 1.500.000 сўм", callback_data="amount_paid:1500000"),
                InlineKeyboardButton(text="💵 2.000.000 сўм(Тўлиқ)", callback_data="amount_paid:2000000"),
            )
            await call.message.edit_text("😊 Тўлов суммасини танланг...\n"
                                         "Энг кам бошланғич сумма 200.000 сўм", reply_markup=summ_btn)
            await state.set_state("get_amount_paid")
    elif payment_method == "cash":
        await db.add_user(telegram_id=int(call.from_user.id), language=lang, region=region, fullname=fullname,
                          phone_number=phone_number, selected_service=service, amount_paid="0")
        if lang == "uz_latin":
            await call.message.edit_text("👋Sizning so'rovingiz qabul qilindi. Tez orada siz bilan bog'lanamiz...")
        elif lang == "uz_cyrillic":
            await call.message.edit_text("👋Сизнинг сўровингиз қабул қилинди. Тез орада сиз билан боғланамиз...")
        text_for_admin = (f"👤 Foydalanuvchi: {fullname}\n"
                          f"📞 Telefon raqami: {phone_number}\n"
                          f"📍 Viloyati: {region}\n"
                          f"📝 Xizmat turi: Online 20 kunlik Kurs\n"
                          f"💵 To'lov summasi: 0 so'm\n"
                          f"📅 Vaqt: {call.message.date}\n"
                          f"🇺🇿 Til: O'zbek Tili\n")
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=text_for_admin)


@dp.callback_query_handler(IsGuest(), text_contains="amount_paid:", state="get_amount_paid")
async def get_amount_paid(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    amount_paid = call.data.split(":")[-1]
    await state.update_data(amount_paid=amount_paid)
    lang = data["lang"]
    if lang == "uz_latin":
        text = ("♦️ Quydagi kartaga to'lov amalga oshiriladi 👇🏻\n\n"
                "Ma'lumotlar:\n"
                "🏦 Bank: <b>Aloqa bank</b>\n"
                "💳 Karta: <b><code>9860 1901 0240 3648</code></b>\n"
                "👤 Ism: <b>Shokhruz Lutfullayev</b>\n"
                f"💵 Summa: <b><code>{amount_paid}</code> so'm</b>\n"
                "To'lov amalga oshirilgandan so'ng <b>📸 Chek rasmini</b> yuboring"
                )
        await call.message.edit_text(text, parse_mode="HTML")
    elif lang == "uz_cyrillic":
        text = ("♦️ Қуйдаги картага тўлов амалга оширилади 👇🏻\n\n"
                "Маълумотлар:\n"
                "🏦 Банк: <b>Aloqa bank</b>\n"
                "💳 Карта: <b><code>9860 1901 0240 3648</code></b>\n"
                "👤 Исм: <b>Шохруз Лутфуллаев</b>\n"
                f"💵 Сумма: <b><code>{amount_paid}</code> сўм</b>\n"
                "Тўлов амалга оширилгандан сўнг <b>📸 Чек расмини</b> юборинг"
                )
        await call.message.edit_text(text, parse_mode="HTML")

    await state.set_state("get_cheque")


@dp.message_handler(IsGuest(), state="get_cheque", content_types=ContentTypes.PHOTO)
async def get_cheque(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    region = data["region"]
    fullname = data["fullname"]
    phone_number = data["phone_number"]
    service = data["service"]
    amount_paid = data["amount_paid"]
    await db.add_user(telegram_id=int(message.from_user.id), language=lang, region=region, fullname=fullname,
                      phone_number=phone_number, selected_service=service, amount_paid=amount_paid,
                      cheques=message.photo[-1].file_id)
    text_for_admin = (f"👤 Foydalanuvchi: {fullname}\n"
                      f"📞 Telefon raqami: {phone_number}\n"
                      f"📍 Viloyati: {region}\n"
                      f"📝 Xizmat turi: Online 20 kunlik Kurs\n"
                      f"💵 To'lov summasi: {amount_paid}\n"
                      f"📅 Vaqt: {message.date}\n"
                      f"🇺🇿 Til: O'zbek Tili\n")
    for admin in ADMINS:
        await bot.send_photo(chat_id=admin, photo=message.photo[-1].file_id, caption=text_for_admin)

    if lang == "uz_latin":
        await message.answer("👋Sizning so'rovingiz qabul qilindi. Tez orada siz bilan bog'lanamiz...")
    elif lang == "uz_cyrillic":
        await message.answer("👋Сизнинг сўровингиз қабул қилинди. Тез орада сиз билан боғланамиз...")
    await state.finish()
    await state.reset_data()
