import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from filters import IsSuperAdmin
from keyboards.inline.superAdminKeyboards import menu_super_admin, users_btn
from loader import dp, db


@dp.message_handler(IsSuperAdmin(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Salom Katta Admin, {message.from_user.full_name}!", reply_markup=menu_super_admin)


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:cancel", state="*")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("Bekor qilindi!", reply_markup=menu_super_admin)
    await state.finish()


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:users")
async def users(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Foydalanuvchilar", reply_markup=users_btn)


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:free_webinar_users", state="*")
async def free_webinar_users(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    users = await db.select_users_by_condition(selected_service='free_webinar')
    columns = ["ID", "F.I.O", "Tel Raqam", "Xizmat", "SUMMA", "Tolov", "Viloyat", "Vaqt"]
    data = [columns]
    for user in users:
        id = user['id']
        fullname = user['fullname']
        phone_number = user['phone_number']
        selected_service = user['selected_service']
        region = user['region']
        if selected_service == 'free_webinar':
            selected_service = 'Webinar'
            amount_paid = "-"
            method = "-"
        else:
            selected_service = 'Kurs'
            amount_paid = f"{user['amount_paid']}"
            if amount_paid == '0 so\'m':
                method = 'Naqd'
            else:
                method = 'Karta'
        created_at = user['created_at']
        created_at = datetime.datetime.strftime(created_at, "%Y-%m-%d %H:%M:%S")

        data.append([id, fullname, phone_number, selected_service, amount_paid, method, region, created_at])

    # Create the PDF document
    doc = SimpleDocTemplate("free_webinar_users.pdf", pagesize=A4)
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),  # Header row font style
        ('FONTSIZE', (0, 0), (-1, 0), 9),  # Header row font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 9),  # Header row bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data row background color
        ('FONTNAME', (0, 1), (-1, -1), 'Courier'),  # Data row font style
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Data row font size
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),  # Data row bottom padding
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Grid lines for all cells
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Border for all cells
    ]))
    doc.build([table])
    await call.message.answer_document(document=open("free_webinar_users.pdf", "rb"))


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:paid_course_users", state="*")
async def paid_course_users(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    users = await db.select_users_by_condition(selected_service='online_course')
    columns = ["ID", "F.I.O", "Tel Raqam", "Xizmat", "SUMMA", "Tolov", "Viloyat", "Vaqt"]
    data = [columns]
    for user in users:
        id = user['id']
        fullname = user['fullname']
        phone_number = user['phone_number']
        selected_service = user['selected_service']
        region = user['region']
        if selected_service == 'free_webinar':
            selected_service = 'Webinar'
            amount_paid = "-"
            method = "-"
        else:
            selected_service = 'Kurs'
            amount_paid = f"{user['amount_paid']}"
            if amount_paid == '0 so\'m':
                method = 'Naqd'
            else:
                method = 'Karta'
        created_at = user['created_at']
        created_at = datetime.datetime.strftime(created_at, "%Y-%m-%d %H:%M:%S")
        data.append([id, fullname, phone_number, selected_service, amount_paid, method, region, created_at])

    # Create the PDF document
    doc = SimpleDocTemplate("free_webinar_users.pdf", pagesize=A4)
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),  # Header row font style
        ('FONTSIZE', (0, 0), (-1, 0), 9),  # Header row font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 9),  # Header row bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data row background color
        ('FONTNAME', (0, 1), (-1, -1), 'Courier'),  # Data row font style
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Data row font size
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),  # Data row bottom padding
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Grid lines for all cells
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Border for all cells
    ]))
    doc.build([table])
    await call.message.answer_document(document=open("free_webinar_users.pdf", "rb"))
