from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.datacollect import Data, FillGoogleFormState
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from loader import dp, bot, ADMIN_TELEGRAM_ID
from aiogram.utils.exceptions import ChatNotFound
from keyboards.default.mainbutton import confirm_data_button, mainbutton
from aiogram.types import ReplyKeyboardRemove
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openpyxl


# Cancel command
@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Jarayon bekor qilindi.", reply_markup=mainbutton)

@dp.message_handler(Text(equals="🔍 Hodim kerak", ignore_case=True), state=None)


# states
# @dp.message_handler(state=None)
async def bot_start(message: types.Message):
    
    # await message.answer(f"Salom, {message.from_user.full_name}!")
# Start command
    await Data.tech.set()
    await message.reply("📌 Ish turi(masalan: Backendchi, O'qituvchi Integration)ni kiriting:", reply_markup=ReplyKeyboardRemove())

# Technology input
@dp.message_handler(state=Data.tech)
async def process_tech(message: types.Message, state: FSMContext):
    await state.update_data(tech=message.text)
    await Data.telegram.set()
    await message.reply("📨 Telegram userini kiriting (masalan: @username):")

# Telegram input
@dp.message_handler(state=Data.telegram)
async def process_telegram(message: types.Message, state: FSMContext):
    await state.update_data(telegram=message.text)
    await Data.contact.set()
    await message.reply("📞 Aloqa uchun ma'lumotni kiriting:(masalan: telfon raqam...)")

# Contact input
@dp.message_handler(state=Data.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Data.region.set()
    await message.reply("🌐 Hududni kiriting:(masalan: Toshkent)")

# Region input
@dp.message_handler(state=Data.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await Data.responsible.set()
    await message.reply("✍️ Mas'ul shaxsning ismini kiriting:(masalan:HR)")

# Responsible input
@dp.message_handler(state=Data.responsible)
async def process_responsible(message: types.Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await Data.work_time.set()
    await message.reply("⌚ Ish vaqtini kiriting:(masalan: 09:00-18:00)")

# Work time input
@dp.message_handler(state=Data.work_time)
async def process_work_time(message: types.Message, state: FSMContext):
    await state.update_data(work_time=message.text)
    await Data.salary.set()
    await message.reply("💰 Maoshni kiriting:")

# Salary input
@dp.message_handler(state=Data.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    summary = (
        f"*Xodim kerak:*\n"
        f"📌 *Ish turi*: {data['tech']}\n"
        f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
    )
    await Data.confirm.set()
    await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# Confirmation input
@dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=Data.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        admin_id = ADMIN_TELEGRAM_ID  
        summary2 = (
            f"*Xodim kerak:*\n"
            f"📌 *Ish turi*: {data['tech']}\n"
            f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        )
        
        for admin_id in admin_id:
            try:
                await bot.send_message(chat_id=admin_id, text=summary2, parse_mode="Markdown")
            # except ChatNotFound:
            #     print(f"Admin with ID {admin_id} not found or unable to send message.")
            except Exception as e:
                texterror = (f"Failed to send message to {admin_id}: {e}")
                await bot.send_message(chat_id=admin_id,text=texterror )
        
        
        # await bot.send_message(chat_id=admin_id, text=summary)
        await message.reply("Ma'lumotlaringiz adminga yuborildi!", reply_markup=mainbutton)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.", reply_markup=mainbutton)
    await state.finish()

# # Cancel command
# @dp.message_handler(commands="cancel", state="*")
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply("Jarayon bekor qilindi.", reply_markup=mainbutton)








#states 2


@dp.message_handler(Text(equals="🏢 Ish joy kerak", ignore_case=True), state=None)

async def bot_start(message: types.Message):
    await Data.tech.set()
    await message.reply("📌 Kasbingiz (masalan: O'qituvchi)ni kiriting:", reply_markup=ReplyKeyboardRemove())

# kasb input
@dp.message_handler(state=Data.tech)
async def process_tech(message: types.Message, state: FSMContext):
    await state.update_data(tech=message.text)
    await Data.telegram.set()
    await message.reply("📨 Telegram userini kiriting (masalan: @username):")

# Telegram input
@dp.message_handler(state=Data.telegram)
async def process_telegram(message: types.Message, state: FSMContext):
    await state.update_data(telegram=message.text)
    await Data.contact.set()
    await message.reply("📞 Aloqa uchun ma'lumotni kiriting:")

# Contact input
@dp.message_handler(state=Data.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Data.region.set()
    await message.reply("🌐 Hududni kiriting:")

# Region input
@dp.message_handler(state=Data.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await Data.responsible.set()
    await message.reply("✍️ Tajribangizni kiriting:")

# Responsible input
@dp.message_handler(state=Data.responsible)
async def process_responsible(message: types.Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await Data.work_time.set()
    await message.reply("⌚ Ish vaqtini kiriting:")

# Work time input
@dp.message_handler(state=Data.work_time)
async def process_work_time(message: types.Message, state: FSMContext):
    await state.update_data(work_time=message.text)
    await Data.salary.set()
    await message.reply("💰 Maoshni kiriting:")

# Salary input
@dp.message_handler(state=Data.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()

    summary = (
        f"*🏢 Ish joy kerak:*\n"
        f"📌 *Kasbi*: {data['tech']}\n"
        f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Tajriba*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
    )
    await Data.confirm.set()
    await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# Confirmation input
@dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=Data.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        admin_id = ADMIN_TELEGRAM_ID  
        summary2 = (
            f"*🏢 Ish joy kerak:*\n"
            f"📌 *Texnologiya *: {data['tech']}\n"
            f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        )
        
        for admin_id in admin_id:
            try:
                await bot.send_message(chat_id=admin_id, text=summary2, parse_mode="Markdown")
            # except ChatNotFound:
            #     print(f"Admin with ID {admin_id} not found or unable to send message.")
            except Exception as e:
                texterror = (f"Failed to send message to {admin_id}: {e}")
                await bot.send_message(chat_id=admin_id, text=texterror )
        
        
        # await bot.send_message(chat_id=admin_id, text=summary)
        await message.reply("Ma'lumotlaringiz adminga yuborildi!", reply_markup=mainbutton)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.", reply_markup=mainbutton)
    await state.finish()

# Cancel command
@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Jarayon bekor qilindi.", reply_markup=mainbutton)
    









   
@dp.message_handler(Text(equals="🤝 Sherik kerak", ignore_case=True), state=None)
async def bot_start(message: types.Message):
    await Data.tech.set()
    await message.reply("📌Ish(masalan:Pythonda dastur yozishga)ni kiriting:", reply_markup=ReplyKeyboardRemove())

# Technology input
@dp.message_handler(state=Data.tech)
async def process_tech(message: types.Message, state: FSMContext):
    await state.update_data(tech=message.text)
    await Data.telegram.set()
    await message.reply("📨 Telegram userini kiriting (masalan: @username):")

# Telegram input
@dp.message_handler(state=Data.telegram)
async def process_telegram(message: types.Message, state: FSMContext):
    await state.update_data(telegram=message.text)
    await Data.contact.set()
    await message.reply("📞 Aloqa uchun ma'lumotni kiriting:")

# Contact input
@dp.message_handler(state=Data.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Data.region.set()
    await message.reply("🌐 Hududni kiriting:")

# Region input
@dp.message_handler(state=Data.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await Data.responsible.set()
    await message.reply("✍️ ismingizni kiriting:")

# Responsible input
@dp.message_handler(state=Data.responsible)
async def process_responsible(message: types.Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await Data.work_time.set()
    await message.reply("⌚ Ish vaqtini kiriting:")

# Work time input
@dp.message_handler(state=Data.work_time)
async def process_work_time(message: types.Message, state: FSMContext):
    await state.update_data(work_time=message.text)
    await Data.salary.set()
    await message.reply("💰 Maoshni kiriting:")

# Salary input
@dp.message_handler(state=Data.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()

    summary = (
        f"*🤝 Sherik kerak* /n"
        f"📌 *Ish*: {data['tech']}\n"
        f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
    )
    await Data.confirm.set()
    await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# Confirmation input
@dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=Data.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        admin_id = ADMIN_TELEGRAM_ID  
        summary2 = (
            f"*🤝 Sherik kerak* /n"
            f"📌 *Ish*: {data['tech']}\n"
            f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        )
        
        for admin_id in admin_id:
            try:
                await bot.send_message(chat_id=admin_id, text=summary2, parse_mode="Markdown")
            except Exception as e:
                texterror = (f"Failed to send message to {admin_id}: {e}")
                await bot.send_message(chat_id=admin_id,text=texterror )
        
        
        # await bot.send_message(chat_id=admin_id, text=summary)
        await message.reply("Ma'lumotlaringiz adminga yuborildi!", reply_markup=mainbutton)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.")
    await state.finish()

# # Cancel command
# @dp.message_handler(commands="cancel", state="*")
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply("Jarayon bekor qilindi.", reply_markup=mainbutton)
    
    
    
    





@dp.message_handler(Text(equals="🧑🏻‍🏫👩🏻‍🏫 Ustoz kerak", ignore_case=True), state=None)
async def bot_start(message: types.Message):
    await Data.tech.set()
    await message.reply("📌 Yo'nalishi: (masalan: Python o'qitish)ni kiriting:", reply_markup=ReplyKeyboardRemove())

# Technology input
@dp.message_handler(state=Data.tech)
async def process_tech(message: types.Message, state: FSMContext):
    await state.update_data(tech=message.text)
    await Data.telegram.set()
    await message.reply("📨 Telegram userizni kiriting (masalan: @username):")

# Telegram input
@dp.message_handler(state=Data.telegram)
async def process_telegram(message: types.Message, state: FSMContext):
    await state.update_data(telegram=message.text)
    await Data.contact.set()
    await message.reply("📞 Aloqa uchun ma'lumotni kiriting:")

# Contact input
@dp.message_handler(state=Data.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Data.region.set()
    await message.reply("🌐 Hududni kiriting:")

# Region input
@dp.message_handler(state=Data.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await Data.responsible.set()
    await message.reply("✍️ Talablarizni kiriting:")

# Responsible input
@dp.message_handler(state=Data.responsible)
async def process_responsible(message: types.Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await Data.work_time.set()
    await message.reply("⌚ o'rganish vaqtini kiriting:")

# Work time input
@dp.message_handler(state=Data.work_time)
async def process_work_time(message: types.Message, state: FSMContext):
    await state.update_data(work_time=message.text)
    await Data.salary.set()
    await message.reply("💰 Maoshni kiriting:")

# Salary input
@dp.message_handler(state=Data.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()

    summary = (
        f"*🧑🏻‍🏫👩🏻‍🏫 Ustoz kerak: *"
        f"📌 *Yo'nalish*: {data['tech']}\n"
        f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Talablar*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
    )
    await Data.confirm.set()
    await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# Confirmation input
@dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=Data.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        admin_id = ADMIN_TELEGRAM_ID  
        summary2 = (
            f"*🧑🏻‍🏫👩🏻‍🏫 Ustoz kerak : *\n"
            f"📌 *Yo'nalish*: {data['tech']}\n"
            f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Talab*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        )
        
        for admin_id in admin_id:
            try:
                await bot.send_message(chat_id=admin_id, text=summary2, parse_mode="Markdown")
            except Exception as e:
                texterror = (f"Failed to send message to {admin_id}: {e}")
                await bot.send_message(chat_id=admin_id,text=texterror )
        
        
        # await bot.send_message(chat_id=admin_id, text=summary)
        await message.reply("Ma'lumotlaringiz adminga yuborildi!", reply_markup=mainbutton)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.")
    await state.finish()

# # Cancel command
# @dp.message_handler(commands="cancel", state="*")
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply("Jarayon bekor qilindi.", reply_markup=mainbutton)
    
    
    
    
    
    
    
    
    
    
    
    

    
# @dp.message_handler(Text(equals="👩🏻‍🎓👨🏻‍🎓 Shogird kerak none", ignore_case=True), state=None)
# async def bot_start(message: types.Message):
#     await Data.tech.set()
#     await message.reply("📌 Yo'nalish:(masalan:Python, Django, Bot)ni kiriting:", reply_markup=ReplyKeyboardRemove())

# # Technology input
# @dp.message_handler(state=Data.tech)
# async def process_tech(message: types.Message, state: FSMContext):
#     await state.update_data(tech=message.text)
#     await Data.telegram.set()
#     await message.reply("📨 Telegram userini kiriting (masalan: @username):")

# # Telegram input
# @dp.message_handler(state=Data.telegram)
# async def process_telegram(message: types.Message, state: FSMContext):
#     await state.update_data(telegram=message.text)
#     await Data.contact.set()
#     await message.reply("📞 Aloqa uchun ma'lumotni kiriting:")

# # Contact input
# @dp.message_handler(state=Data.contact)
# async def process_contact(message: types.Message, state: FSMContext):
#     await state.update_data(contact=message.text)
#     await Data.region.set()
#     await message.reply("🌐 Hududni kiriting:")

# # Region input
# @dp.message_handler(state=Data.region)
# async def process_region(message: types.Message, state: FSMContext):
#     await state.update_data(region=message.text)
#     await Data.responsible.set()
#     await message.reply("✍️ Mas'ul shaxsning ismini kiriting:")

# # Responsible input
# @dp.message_handler(state=Data.responsible)
# async def process_responsible(message: types.Message, state: FSMContext):
#     await state.update_data(responsible=message.text)
#     await Data.work_time.set()
#     await message.reply("⌚ Ish vaqtini kiriting:")

# # Work time input
# @dp.message_handler(state=Data.work_time)
# async def process_work_time(message: types.Message, state: FSMContext):
#     await state.update_data(work_time=message.text)
#     await Data.salary.set()
#     await message.reply("💰 Maoshni kiriting:")

# # Salary input
# @dp.message_handler(state=Data.salary)
# async def process_salary(message: types.Message, state: FSMContext):
#     await state.update_data(salary=message.text)
#     data = await state.get_data()

#     summary = (
#         f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
#         f"📌 *Yo'nalish*: {data['tech']}\n"
#         f"📨 *Telegram*: {data['telegram']}\n"
#             f"📞 *Aloqa*: {data['contact']}\n"
#             f"🌐 *Hudud*: {data['region']}\n"
#             f"✍️ *Mas'ul*: {data['responsible']}\n"
#             f"⌚ *Ish vaqti*: {data['work_time']}\n"
#             f"*💰 Maosh*: {data['salary']}\n"
#         f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
#     )
#     await Data.confirm.set()
#     await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# # Confirmation input
# @dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=Data.confirm)
# async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        admin_id = ADMIN_TELEGRAM_ID  
        summary2 = (
            f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
            f"📌 *Yo'nalish*: {data['tech']}\n"
            f"📨 *Telegram*: {data['telegram']}\n"
            f"📞 *Aloqa*: {data['contact']}\n"
            f"🌐 *Hudud*: {data['region']}\n"
            f"✍️ *Mas'ul*: {data['responsible']}\n"
            f"⌚ *Ish vaqti*: {data['work_time']}\n"
            f"*💰 Maosh*: {data['salary']}\n"
        )
        
        for admin_id in admin_id:
            try:
                await bot.send_message(chat_id=admin_id, text=summary2, parse_mode="Markdown")
            # except ChatNotFound:
            #     print(f"Admin with ID {admin_id} not found or unable to send message.")
            except Exception as e:
                texterror = (f"Failed to send message to {admin_id}: {e}")
                await bot.send_message(chat_id=admin_id,text=texterror)
        
        
        # await bot.send_message(chat_id=admin_id, text=summary)
        await message.reply("Ma'lumotlaringiz adminga yuborildi!", reply_markup=mainbutton)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.")
    await state.finish()






# #Form cheacking aprt

# SCOPE = ["https://docs.google.com/spreadsheets/d/1jDILIHV7dCfRBZK6h8tUFtbfVUZ2GWcgddqw8Sq-bEs/edit?usp=sharing"]
# CREDS_FILE = "C:/Users/Victus/Desktop/mukammal-bot-paid-master/mukammal-bot-paid-master/botform.xlsx"  # Replace with your JSON key file path
# SPREADSHEET_NAME = "botform"  # Replace with your Google Sheet name

# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
# client = gspread.authorize(credentials)
# sheet = client.open(SPREADSHEET_NAME).sheet1  # Open the first sheet

# @dp.message_handler(Text(equals="👩🏻‍🎓👨🏻‍🎓 Shogird kerak", ignore_case=True), state=None)
# async def bot_start(message: types.Message):
#     await FillGoogleFormState.salary.set()
#     await message.reply("📌 qancha maosh xohlaysiz:", reply_markup=ReplyKeyboardRemove())






# # STates 
# @dp.message_handler(state=FillGoogleFormState.salary)
# async def process_salary(message: types.Message, state: FSMContext):
#     await state.update_data(salary=message.text)
#     await FillGoogleFormState.name.set()
#     await message.reply("📨ismizni kiriting:")
    
# @dp.message_handler(state=FillGoogleFormState.name)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await FillGoogleFormState.age.set()
#     await message.reply("yoshizni kiriting:")
    
# @dp.message_handler(state=FillGoogleFormState.age)
# async def process_age(message: types.Message, state:FSMContext):
#     await state.update_data(age=message.text)
#     await FillGoogleFormState.region.set()
#     await message.reply("viloyatingizni kiriting: ")
    
# @dp.message_handler(state=FillGoogleFormState.region)
# async def process_region(message: types.Message, state: FSMContext):
#     await state.update_data(region=message.text)
#     data = await state.get_data()

#     summary = (
#         f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
#         f"📌 *maosh*: {data['salary']}\n"
#          f"📞 *Ism*: {data['name']}\n"
#         f"📨 *yosh*: {data['age']}\n"
#         f"📞 *Viloyat*: {data['region']}\n"
#         f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
#     )
#     await FillGoogleFormState.confirm.set()
#     await message.reply(summary, parse_mode="Markdown", reply_markup=confirm_data_button)

# # Confirmation input
# @dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=FillGoogleFormState.confirm)
# async def process_confirm(message: types.Message, state: FSMContext):
#     if message.text.lower() == 'ha':
#         data = await state.get_data()

#         # Data to write into Google Sheet
#         row = [data['salary'], data['name'], data['age'], data['region']]

#         try:
#             # Append the row to the Google Sheet
#             sheet.append_row(row)
#             await message.reply("Ma'lumotlaringiz Google Sheetga yozildi va adminga yuborildi!", reply_markup=mainbutton)
#         except Exception as e:
#             await message.reply(f"Google Sheetga yozishda xatolik: {e}")
        
#         admin_id = ADMIN_TELEGRAM_ID  # Add admin IDs here
#         summary2 = (
#             f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
#             f"📌 *maosh*: {data['salary']}\n"
#             f"📞 *Ism*: {data['name']}\n"
#             f"📨 *yosh*: {data['age']}\n"
#             f"📞 *Viloyat*: {data['region']}\n"
#         )
        
#         for admin in admin_id:
#             try:
#                 await bot.send_message(chat_id=admin, text=summary2, parse_mode="Markdown")
#             except Exception as e:
#                 texterror = f"Admin uchun habar jo'natishda xatolik: {e}"
#                 await bot.send_message(chat_id=admin, text=texterror)
#     else:
#         await message.reply("Ma'lumotlarni qayta kiritishni boshlang.")
    
#     await state.finish()


EXCEL_FILE = r"C:\Users\Victus\Desktop\mukammal-bot-paid-master\mukammal-bot-paid-master\botform.xlsx"

# Function to write data to Excel
def write_to_excel(row):
    try:
        # Load the workbook
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active

        # Append the row
        sheet.append(row)

        # Save the workbook
        workbook.save(EXCEL_FILE)
        return True
    except Exception as e:
        print(f"Error writing to Excel: {e}")
        return False

# Handlers
@dp.message_handler(Text(equals="👩🏻‍🎓👨🏻‍🎓 Shogird kerak", ignore_case=True), state=None)
async def bot_start(message: types.Message):
    await FillGoogleFormState.salary.set()
    await message.reply("📌 qancha maosh xohlaysiz:", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=FillGoogleFormState.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await FillGoogleFormState.name.set()
    await message.reply("📨 Ismingizni kiriting:")

@dp.message_handler(state=FillGoogleFormState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await FillGoogleFormState.age.set()
    await message.reply("Yoshingizni kiriting:")

@dp.message_handler(state=FillGoogleFormState.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await FillGoogleFormState.region.set()
    await message.reply("Viloyatingizni kiriting:")

@dp.message_handler(state=FillGoogleFormState.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    data = await state.get_data()

    summary = (
        f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
        f"📌 *Maosh*: {data['salary']}\n"
        f"📞 *Ism*: {data['name']}\n"
        f"📨 *Yosh*: {data['age']}\n"
        f"📞 *Viloyat*: {data['region']}\n"
        f"Barcha ma'lumotlar to'g'rimi? *(ha/yo'q)*"
    )
    await FillGoogleFormState.confirm.set()
    await message.reply(summary, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text.lower() in ['ha', 'yo\'q'], state=FillGoogleFormState.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()

        # Data to write into Excel
        row = [data['salary'], data['name'], data['age'], data['region']]

        if write_to_excel(row):
            await message.reply("Ma'lumotlaringiz Excel fayliga yozildi!", reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply("Excel fayliga yozishda xatolik yuz berdi!")

        admin_id = ADMIN_TELEGRAM_ID  # Add admin IDs here
        summary2 = (
            f"*👩🏻‍🎓👨🏻‍🎓 Shogird kerak*\n"
            f"📌 *Maosh*: {data['salary']}\n"
            f"📞 *Ism*: {data['name']}\n"
            f"📨 *Yosh*: {data['age']}\n"
            f"📞 *Viloyat*: {data['region']}\n"
        )

        for admin in admin_id:
            try:
                await bot.send_message(chat_id=admin, text=summary2, parse_mode="Markdown")
            except Exception as e:
                texterror = f"Admin uchun habar jo'natishda xatolik: {e}"
                await bot.send_message(chat_id=admin, text=texterror)
    else:
        await message.reply("Ma'lumotlarni qayta kiritishni boshlang.")

    await state.finish()







