from aiogram.types import CallbackQuery

from filters import IsSuperAdmin
from keyboards.inline.superAdminKeyboards import back
from loader import dp, db


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:stat", state="*")
async def show_stat(call: CallbackQuery):
    count_users = await db.count_users()
    count_free_webinar_users = len(await db.select_users_by_condition(selected_service='free_webinar'))
    count_paid_course_users = len(await db.select_users_by_condition(selected_service='online_course'))
    count_new_users = len(await db.select_daily_users())

    text = f"""
    📊 Statistika:
    👤 Umumiy foydalanuvchilar soni: {count_users} ta
    💵 Pullik kurs qatnashchilari soni: {count_paid_course_users} ta
    🆓 Bepul webinar qatnashchilari soni: {count_free_webinar_users} ta

    📆 Bugungi statistika:
    👤 Yangi foydalanuvchilar soni: {count_new_users} ta
    """
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=back)

