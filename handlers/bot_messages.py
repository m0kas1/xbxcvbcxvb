from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from keyboards import main, ispravit
from aiogram.fsm.context import FSMContext
from utils import StepsForm
from keyboards import inline_kb, b
from lexicon import LEXICON_RU
import os
from word import add_word

from environs import Env

env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
channel_id = env('CHAT_ID')

bot = Bot(token=bot_token, parse_mode='HTML')

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != channel_id:
        await message.answer(f"Привет, {message.from_user.first_name}! Чтобы начать наше заполнять анкету, нажмите на кнопочку снизу/слева снизу кнопка 'Menu'", reply_markup=main)
    else:
        pass

@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(F.text)
async def get_start(message: Message, state: FSMContext):
    if (message.text.lower() == 'отправить проблему' or message.text.lower() == '/form') and message.chat.id != channel_id:
        await message.answer('На каком предприятии обнаружена проблема?', reply_markup=inline_kb.as_markup())
        await state.set_state(StepsForm.GET_CHEH)
@router.callback_query(F.data.startswith("«"))
async def get_CHEH(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(cheh=callback.data)
        await state.set_state(StepsForm.GET_FIO)
        await callback.message.answer('Введите ваше ФИО')
    except AttributeError:
        await bot.send_message(chat_id=callback.from_user.id, text=LEXICON_RU['no_echo'])
@router.message(F.text)
async def get_FIO(message: Message, state: FSMContext):
    try:
        if message.text.count(' ') == 2 and message.text.count(' ') != len(message.text):
            await state.update_data(fio=message.text)
            await state.set_state(StepsForm.GET_PODRASDELENIE)
            await message.answer('Введите ваше подразделение:')
        else:
            await message.answer('Введите нормально текст.\n\nПример: Имя Фамилия Отчество.')
    except AttributeError:
        await bot.send_message(chat_id=message.from_user.id, text=LEXICON_RU['no_g'])
@router.message(F.text)
async def get_PODRASDELENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text=LEXICON_RU['no_g'])
    else:
        await state.update_data(podraselenit=message.text)
        await state.set_state(StepsForm.GET_ULUCHENIE)
        await message.answer('Укажите область улучшения:', reply_markup=b.as_markup())

@router.callback_query(F.data)
async def get_ULUCHENIE(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(uluchenie=callback.data)
        await state.set_state(StepsForm.GET_PREDLOSHENIE)
        await callback.message.answer('Напишите название предложения:')
    except AttributeError:
        await bot.send_message(chat_id=callback.from_user.id, text=LEXICON_RU['no_echo'])
@router.message(F.text)
async def get_PREDLOSHENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text=LEXICON_RU['no_g'])
    else:
        await state.update_data(predloshenie=message.text)
        await state.set_state(StepsForm.GET_PROBLEMA)
        await message.answer('Опишите вашу проблему')

@router.message(F.in_(['text', 'photo']))
async def get_PROBLEMA(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text=LEXICON_RU['no_g'])
    else:
        await state.update_data(problema=message.text)
        await state.set_state(StepsForm.GET_PHOTO_1)
        await message.answer('Отправьте фото. ЕСЛИ ФОТО НЕТ - ВВЕДИТЕ ЛЮБОЙ ТЕКСТ')
@router.message(F.text)
async def get_PHOTO_1(message: Message, state: FSMContext, bot: Bot):
    c = 0
    while c != 1:
        if message.photo:
            await state.update_data(photo_1=message.photo[-1].file_id)
            await state.set_state(StepsForm.GET_PHOTO_1)
            await bot.download(
                message.photo[-1],
                destination=f"img/{message.photo[-1].file_id}.jpg"
            )
            await state.set_state(StepsForm.GET_RESHENIE)
            await message.answer('Опишите ваше решение проблемы:')
            c = 1
        else:
            await state.set_state(StepsForm.GET_RESHENIE)
            await message.answer('Опишите ваше решение проблемы:')
            break

@router.message()
async def get_RESHENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text=LEXICON_RU['no_g'])
    else:
        await state.update_data(reshenie=message.text)
        await state.set_state(StepsForm.GET_PHOTO_2)
        await message.answer('Отправьте фото. ЕСЛИ ФОТО НЕТ - ВВЕДИТЕ ЛЮБОЙ ТЕКСТ')

@router.message()
async def get_PHOTO_2(message: Message, state: FSMContext, bot: Bot):
    global data_user, PHOTO_1, TEG, PHOTO_2, CHEH
    c = 0
    while c != 1:
        if message.photo:
            await state.update_data(photo_2=message.photo[-1].file_id)
            await state.set_state(StepsForm.GET_PHOTO_2)
            await bot.download(
                message.photo[-1],
                destination=f"img/{message.photo[-1].file_id}.jpg"
            )
            c = 1
        else:
            break

    content_data = await state.get_data()
    TEG = f'@{message.from_user.username}'
    d = dict(content_data)
    # print(content_data.__dict__)
    d['TEG'] = TEG
    print(f'Данные отправителя {d}')

    FIO = content_data.get('fio')
    CHEH = content_data.get('cheh')
    PODRASDELENIE = content_data.get('podraselenit')
    ULUCHENIE = content_data.get('uluchenie')
    PREDLOSHENIE = content_data.get('predloshenie')
    RESHENIE = content_data.get('reshenie')
    PROBLEMA = content_data.get('problema')
    PHOTO_1 = content_data.get('photo_1')
    PHOTO_2 = content_data.get('photo_2')
    data_user = f'Данные пользователя:\r\n\n' \
                f'ФИО: {FIO}\n' \
                f'Место работы: {CHEH}\n' \
                f'Подразделение: {PODRASDELENIE}\n' \
                f'Область улучшения: {ULUCHENIE}\n' \
                f'Предложение: {PREDLOSHENIE}\n' \
                f'Проблема: {PROBLEMA}\n' \
                f'Решение: {RESHENIE}\n' \
                f'Тег: {TEG}'

    if PHOTO_1 is None and PHOTO_2 is None:
        await message.answer(data_user)
        await message.answer('Всё верно? Нажмите на кнопку снизу.', reply_markup=ispravit)
    else:
        if PHOTO_1 is None:
            g_2 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_2}.jpg'), caption=data_user)
            media = [g_2]
            await message.answer_media_group(media)
            await message.answer('Всё верно? Нажмите на кнопку снизу.', reply_markup=ispravit)

        else:
            if PHOTO_2 is None:
                g_1 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_1}.jpg'), caption=data_user)
                media = [g_1]
                await message.answer_media_group(media)
                await message.answer('Всё верно? Нажмите на кнопку снизу.', reply_markup=ispravit)
            else:
                g_1 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_1}.jpg'))
                g_2 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_2}.jpg'), caption=data_user)
                media = [g_1, g_2]
                await message.answer_media_group(media)
                await message.answer('Всё верно? Нажмите на кнопку снизу.', reply_markup=ispravit)
    await state.update_data(gey=message.text)
    await state.set_state(StepsForm.GET_vibor)
@router.message()
async def get_VIBER(message: Message, state: FSMContext):
    if message.text.lower() == 'исправить':
        await state.clear()
        if os.path.isfile(f'img/{PHOTO_1}.jpg') or os.path.isfile(f'img/{PHOTO_2}.jpg'):
            os.remove(f'img/{PHOTO_1}.jpg')
            os.remove(f'img/{PHOTO_2}.jpg')


        # if os.path.isfile(f'txt/{TEG}.txt'):
        #     os.remove(f'txt/{TEG}.txt')
        #
        # if os.path.isfile(f'zip/{CHEH}.zip'):
        #     os.remove(f'zip/{CHEH}.zip')

        await message.answer(f"Давай ещё раз, только будь аккуратнее! Незабудь нажать на кнопку ниже 👇", reply_markup=main)

    if message.text.lower() == 'отправить':
        await state.clear()
        add_word(PHOTO_1, PHOTO_2, data_user, CHEH, TEG)
        # my_file = open(f"txt/{TEG}.txt", "w+", encoding='utf-8')
        # my_file.write(data_user)
        # my_file.close()
        #
        # file_zip = zipfile.ZipFile(f'zip/{CHEH}.zip', 'w')
        # file_zip.close()
        #
        # file_zip = zipfile.ZipFile(f'zip/{CHEH}.zip', 'a')
        # file_zip.write(f'txt/{TEG}.txt')
        #
        # if PHOTO_1 is None and PHOTO_2 is None:
        #     pass
        #
        # else:
        #     if PHOTO_1 is None:
        #         file_zip.write(f'img/{PHOTO_2}.jpg')
        #     elif PHOTO_2 is None:
        #         file_zip.write(f'img/{PHOTO_1}.jpg')
        #     else:
        #         file_zip.write(f'img/{PHOTO_1}.jpg')
        #         file_zip.write(f'img/{PHOTO_2}.jpg')
        # file_zip.close()
        #
        # documnet = FSInputFile(path=f'zip/{CHEH}.zip')
        documnet = FSInputFile(path=f'word/{CHEH + TEG}.docx')
        await message.answer('Файл отправлен!!!', reply_markup=main)
        await bot.send_document(chat_id=channel_id, document=documnet)
        os.remove(f'word/{CHEH + TEG}.docx')

        if PHOTO_1 is None and PHOTO_2 is None:
            pass
        else:
            if PHOTO_1 is None:
                os.remove(f'img/{PHOTO_2}.jpg')
            elif PHOTO_2 is None:
                os.remove(f'img/{PHOTO_1}.jpg')
            else:
                os.remove(f'img/{PHOTO_1}.jpg')
                os.remove(f'img/{PHOTO_2}.jpg')

@router.message()
async def cmd_start(message: Message):
    await message.answer('Пиши нормально осёл')