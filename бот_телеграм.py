import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import re

TOKEN = "8654456305:AAHN8-QHfYK49gKHpRzM6zcPVCx7_-8TFQU"  

bot = Bot(token=TOKEN)
dp = Dispatcher()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ========== Хранилище методички ответов ==========
FAQ = {}  # ключевое слово: ответ

# ========== Списки цензуры ==========
BANNED_WORDS = [
    # === Самые распространенные (мат) ===
    "хуй", "хуя", "хуё", "хуе", "хуи", "хую", "хули", "хуле", 
    "пизда", "пиздец", "пизды", "пизду", "пиздой", "пизде", "пиздюк",
    "ебать", "ебал", "ебёт", "ебу", "еби", "ёб", "еблан", "ёбаный", "ебанный",
    "блядь", "блять", "бля", "блядина", "блядство", "блядский",
    "сука", "суки", "суку", "сукой", "сучка", "сучонок", "сучара",
    "мудак", "мудила", "мудень", "мудачина", "мудашва",
    "гандон", "гондон", "гандон штопаный",
    "залупа", "залупу", "залупой", "залупень",
    "хер", "хера", "херу", "хернёй", "херня",

    # === Оскорбления личности ===
    "пидор", "пидорас", "пидрила", "пидр", "пидар", "петух",
    "сволочь", "сволота", "сволочной",
    "урод", "уродина", "уродство", "уродливый",
    "дебил", "дебилы", "дебилоид", "дебс",
    "идиот", "идиоты", "идиотина", "идиотка",
    "козёл", "козлы", "козлина", "козлиный",
    "тварь", "твари", "тварюга",
    "лох", "лошара", "лохушка", "лохопет",
    "чмо", "чмошник", "чмырь", "чмо болотное",
    "придурок", "придурки", "придурочный",
    "кретин", "кретины", "кретинка",
    "ублюдок", "ублюдки", "ублюдочный",
    "мразь", "мрази", "мразота",
    "падла", "падлы", "падлюка",
    "гнида", "гниды", "гнилой",
    "скотина", "скоты", "скотский",
    "сучка", "сучонок",
    "гнида", "гниды",
    "сволочь", "сволота",
    "стерва", "стервы", "стервозный",
    "шваль", "швальё",
    "шлюха", "шлюхи", "шлюшка",
    "проститутка", "профура",
    "дура", "дурак", "дурында", "дурачина",
    "тупица", "тупой", "тупорылый",
    "осёл", "ослы", "ослиный",
    "баран", "бараны", "бараний",
    "свинья", "свиньи", "свинский",
    "крыса", "крысы", "крысёныш",
    "шавка", "шавки",
    "пёс", "псы", "псина", "пёс смердячий",
    "быдло", "быдлан", "быдловатый",
    "хам", "хамло", "хамьё",
    "жлоб", "жлобы", "жлобский",
    "алкаш", "алкаши", "алкоголик",
    "наркоман", "наркоша", "нарик",
    "отморозок", "отморозки",
    "подонок", "подонки",
    "негодяй", "негодяи",
    "мерзавец", "мерзавцы",
    "гад", "гады", "гадёныш",
    "злыдень", "злыдни",
    "выродок", "выродки",
    "недоносок", "недоноски",
    "убогий", "убогие",
    "ничтожество", "ничтожества",
    "пустышка", "пустышки",
    "тряпка", "тряпки",
    "размазня",
    "слабак", "слабаки",
    "трус", "трусы", "трусливый",
    "предатель", "предатели",
    "стукач", "стукачи",
    "шестёрка", "шестёрки",
    "холуй", "холуи",
    "прихвостень", "прихвостни",
    "подхалим", "подхалимы",
    "лизоблюд", "лизоблюды",
    "дармоед", "дармоеды",
    "тунеядец", "тунеядцы",
    "нахлебник", "нахлебники",
    "паразит", "паразиты",
    "вонючка", "вонючки",
    "грязнуля", "грязнули",
    
    # === Националистические и расовые оскорбления ===
    "черножопый", "черножопые",
    "чурка", "чурки", "чурбан", "чурбаны",
    "хач", "хачи", "хачик", "хачики",
    "жид", "жиды", "жидовский", "жидёнок",
    "хохол", "хохлы", "хохлушка",
    "москаль", "москали",
    "кацап", "кацапы",
    "бульбаш", "бульбаши",
    "ниггер", "ниггеры",
    "азер", "азеры",
    "армяшка", "армяшки",
]

BANNED_PATTERNS = [
    r"ху[йяёеиюлр]",
    r"пизд[аеёуцчшщ]",
    r"еб[ауёнилртс]",
    r"бля[дт]",
    r"пид[оа]р",
    r"г[оа]нд[оа]н",
    r"м[уа]д[аи]к",
    r"ч[мю]о",
    r"свол[оа]ч",
    r"у[рй]од",
    r"д[еи]бил",
    r"иди[о]т",
    r"к[оа]з[её]л",
    r"твар[ьи]",
    r"ло[хш]",
    r"быдл[оа]",
    r"ха[чм]",
    r"шлю[хш]",
]

# ========== Функции ==========

def censor_text(text: str) -> str:
    """Фильтрует мат и оскорбления"""
    for word in BANNED_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("***", text)
    
    for pattern in BANNED_PATTERNS:
        text = re.sub(pattern, "***", text, flags=re.IGNORECASE)
    
    return text

def load_faq(file_path: str) -> int:
    """Загружает методичку ответов из файла"""
    FAQ.clear()
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                FAQ[key.strip().lower()] = value.strip()
                count += 1
    return count

def load_banned_words(file_path: str) -> int:
    """Загружает список запрещённых слов из файла"""
    global BANNED_WORDS
    with open(file_path, 'r', encoding='utf-8') as f:
        BANNED_WORDS = [line.strip() for line in f if line.strip()]
    return len(BANNED_WORDS)

def find_answer(user_text: str) -> str | None:
    """Ищет ответ в методичке по ключевым словам"""
    text_lower = user_text.lower()
    for key, value in FAQ.items():
        if key in text_lower:
            return value
    return None

# ========== Обработчики ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот с цензурой и приемом файлов.\n\n"
        "📎 Отправь мне файл с методичкой (название должно содержать 'faq' или 'методичка')\n"
        "🚫 Отправь файл со списком запрещённых слов (название должно содержать 'bad_words' или 'цензур')\n"
        "💬 Или просто напиши текст — я проверю на цензуру и найду ответ в методичке\n\n"
        "Команды:\n"
        "/start — это сообщение\n"
        "/help — справка\n"
        "/faq — показать загруженные ответы\n"
        "/words — показать количество запрещённых слов"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Как загрузить методичку ответов:\n"
        "1. Создайте txt-файл с ответами в формате:\n"
        "   ключевое слово: ответ\n"
        "   привет: Здравствуйте!\n"
        "   оплата: Оплата картой\n\n"
        "2. Назовите файл так, чтобы в имени было 'faq' или 'методичка'\n"
        "3. Отправьте файл боту\n\n"
        "Как обновить список цензуры:\n"
        "1. Создайте txt-файл со словами (по одному на строку)\n"
        "2. В имени файла должно быть 'bad_words' или 'цензур'\n"
        "3. Отправьте файл боту"
    )

@dp.message(Command("faq"))
async def cmd_faq(message: types.Message):
    if not FAQ:
        await message.answer("📭 Методичка не загружена. Отправьте файл с ответами.")
    else:
        faq_text = "📋 Загруженные ответы:\n\n"
        for key, value in FAQ.items():
            faq_text += f"• {key}: {value[:50]}...\n" if len(value) > 50 else f"• {key}: {value}\n"
        await message.answer(faq_text)

@dp.message(Command("words"))
async def cmd_words(message: types.Message):
    await message.answer(f"🚫 Запрещено слов: {len(BANNED_WORDS)}\n"
                         f"🔍 Паттернов: {len(BANNED_PATTERNS)}")

@dp.message(F.document)
async def handle_document(message: types.Message):
    """Обработка полученных файлов"""
    document = message.document
    file_name = document.file_name or "file"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # Скачиваем файл
    file_id = document.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, file_path)
    
    file_name_lower = file_name.lower()
    
    # Проверяем, методичка ли это
    if "faq" in file_name_lower or "методичка" in file_name_lower:
        try:
            count = load_faq(file_path)
            await message.answer(f"✅ Методичка '{file_name}' загружена! Выучено {count} ответов.")
        except Exception as e:
            await message.answer(f"⚠️ Ошибка загрузки методички: {e}")
        return
    
    # Проверяем, список ли это цензуры
    if "bad_words" in file_name_lower or "цензур" in file_name_lower:
        try:
            count = load_banned_words(file_path)
            await message.answer(f"✅ Список цензуры '{file_name}' обновлён! Запрещено {count} слов.")
        except Exception as e:
            await message.answer(f"⚠️ Ошибка загрузки списка цензуры: {e}")
        return
    
    # Обычный файл — сохраняем и проверяем на цензуру
    await message.answer(f"✅ Файл '{file_name}' сохранен!")
    
    if file_name.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            censored = censor_text(content)
            
            await message.answer(
                "📝 Проверил содержимое на цензуру:\n\n" + 
                censored[:1000] + ("..." if len(censored) > 1000 else "")
            )
        except Exception as e:
            await message.answer(f"⚠️ Не удалось прочитать файл: {e}")

@dp.message(F.text)
async def handle_text(message: types.Message):
    """Обработка текстовых сообщений с цензурой и поиском ответа"""
    user_text = message.text
    
    # 1. Сначала проверяем цензуру
    censored = censor_text(user_text)
    
    # 2. Ищем ответ в методичке
    answer = find_answer(user_text)
    
    # 3. Формируем ответ
    response = ""
    
    if user_text != censored:
        response += f"⚠️ Текст отфильтрован от нецензурной лексики.\n"
    
    if answer:
        response += f"📝 Нашёл ответ в методичке:\n{answer}"
    elif FAQ:
        response += "🤔 Не нашёл подходящего ответа в методичке. Уточните вопрос."
    else:
        response += "📭 Методичка не загружена. Загрузите файл с ответами командой /help"
    
    await message.answer(response)

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("📸 Фото получил, но работаю только с текстом и документами")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
