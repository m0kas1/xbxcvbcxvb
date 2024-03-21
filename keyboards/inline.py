from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='«ЮМЭК»', callback_data='«ЮМЭК»')
inline_kb.button(text='«МЗВА-ЧЭМЗ»', callback_data='«МЗВА-ЧЭМЗ»')
inline_kb.button(text='«ИНСТА»', callback_data='«ИНСТА»')
inline_kb.button(text='«Энерготрансизолятор»', callback_data='«Энерготрансизолятор»')
inline_kb.button(text='«ВОЛЬТА»', callback_data='«ВОЛЬТА»')
inline_kb.button(text='«ФОРЭНЕРГО-ИНЖИНИРИНГ»', callback_data='«ФОРЭНЕРГО-ИНЖИНИРИНГ»')
inline_kb.button(text='«ЮЗРК ГРУПП»', callback_data='«ЮЗРК ГРУПП»')
inline_kb.adjust(2)

b = InlineKeyboardBuilder()
b.button(text='Безопастность', callback_data='Безопастность')
b.button(text='Качество', callback_data='Качество')
b.button(text='Производительность', callback_data='Производительность')
b.button(text='Эргономика', callback_data='Эргономика')
b.adjust(2)

# inline_kb_2 = InlineKeyboardBuilder()
# inline_kb.button(text='Безопастность', callback_data='«ЮМЭК»')
# inline_kb.button(text='Качество', callback_data='«МЗВА-ЧЭМЗ»')
# inline_kb.button(text='Производительность', callback_data='«ИНСТА»')
# inline_kb.button(text='Эргономика', callback_data='«Энерготрансизолятор»')
# inline_kb.adjust(2)

