from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

mainbutton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔍 Hodim kerak') ,
            KeyboardButton(text='🏢 Ish joy kerak') ,  
              
        ],
        [
            KeyboardButton(text='🤝 Sherik kerak') ,
            KeyboardButton(text='🧑🏻‍🏫👩🏻‍🏫 Ustoz kerak') ,   
              
        ],
        [
            KeyboardButton(text='👩🏻‍🎓👨🏻‍🎓 Shogird kerak') ,  
              
        ],
    ],
    resize_keyboard = True
)

confirm_data_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ha') ,
            KeyboardButton(text='Yo\'q') ,  
              
        ],
    ],
    resize_keyboard = True
)