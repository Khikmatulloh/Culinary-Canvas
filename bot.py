import logging
import os
import asyncio
import django
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category

User = get_user_model()


API_TOKEN = "7300404549:AAHNwPph6Zse8wyXhxHjFQ88C8HYe_J7yvA"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class RecipeForm(StatesGroup):
    title = State()
    description = State()
    ingredients = State()
    instructions = State()
    category = State()
    confirm = State()



@sync_to_async
def get_user_by_email(email: str):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


@sync_to_async
def save_telegram_id(user, telegram_id: str):
    user.telegram_id = telegram_id
    user.save()
    return user


@sync_to_async
def get_user_by_tg(telegram_id: str):
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def create_recipe(data, author):
    category = None
    if data.get("category"):
        category, _ = Category.objects.get_or_create(name=data["category"])

    recipe = Recipe.objects.create(
        author=author,
        title=data["title"],
        description=data["description"],
        ingredients=data["ingredients"],
        instructions=data["instructions"],
        category=category,
    )
    return recipe



@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("👋 Culinary Canvas botiga xush kelibsiz!\n\nIltimos, emailingizni kiriting:")


@router.message(lambda msg: "@" in msg.text)
async def handle_email(message: Message):
    email = message.text.strip()
    user = await get_user_by_email(email)
    if user:
        await save_telegram_id(user, str(message.from_user.id))
        await message.answer("✅ Muvaffaqiyatli login! Endi /recipes orqali retseptlaringizni ko‘rishingiz yoki /newrecipe orqali yangi retsept qo‘shishingiz mumkin.")
    else:
        await message.answer("❌ Bu email ro‘yxatdan o‘tmagan. Avval sayt orqali ro‘yxatdan o‘ting.")



@router.message(Command("recipes"))
async def list_recipes(message: Message):
    user = await get_user_by_tg(str(message.from_user.id))
    if not user:
        await message.answer("❌ Siz login qilmagansiz. Avval emailingizni yozing.")
        return

    recipes = await sync_to_async(list)(Recipe.objects.filter(author=user))
    if recipes:
        reply = "\n".join(f"{r.id}. {r.title}" for r in recipes)
    else:
        reply = "📭 Sizda retseptlar yo‘q."
    await message.answer(reply)



@router.message(Command("newrecipe"))
async def new_recipe(message: Message, state: FSMContext):
    user = await get_user_by_tg(str(message.from_user.id))
    if not user:
        await message.answer("❌ Avval login qilishingiz kerak. Emailingizni yozing.")
        return

    await state.set_state(RecipeForm.title)
    await message.answer("🍴 Yangi retsept nomini kiriting:")


@router.message(RecipeForm.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(RecipeForm.description)
    await message.answer("📖 Retsept tavsifini yozing:")


@router.message(RecipeForm.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(RecipeForm.ingredients)
    await message.answer("🥕 Ingredientlarni yozing (vergul bilan):")


@router.message(RecipeForm.ingredients)
async def process_ingredients(message: Message, state: FSMContext):
    await state.update_data(ingredients=message.text)
    await state.set_state(RecipeForm.instructions)
    await message.answer("👨‍🍳 Tayyorlash usullarini yozing:")


@router.message(RecipeForm.instructions)
async def process_instructions(message: Message, state: FSMContext):
    await state.update_data(instructions=message.text)
    await state.set_state(RecipeForm.category)
    await message.answer("📂 Kategoriya nomini yozing (yoki ❌ yuboring):")


@router.message(RecipeForm.category)
async def process_category(message: Message, state: FSMContext):
    if message.text != "❌":
        await state.update_data(category=message.text)
    data = await state.get_data()

    text = (
        f"✅ Retsept tayyor!\n\n"
        f"🍴 Nomi: {data['title']}\n"
        f"📖 Tavsif: {data['description']}\n"
        f"🥕 Ingredientlar: {data['ingredients']}\n"
        f"👨‍🍳 Tayyorlash: {data['instructions']}\n"
        f"📂 Kategoriya: {data.get('category', 'Yo‘q')}\n\n"
        f"Tasdiqlaysizmi? (ha/yo‘q)"
    )
    await state.set_state(RecipeForm.confirm)
    await message.answer(text)


@router.message(RecipeForm.confirm)
async def process_confirm(message: Message, state: FSMContext):
    user = await get_user_by_tg(str(message.from_user.id))
    if not user:
        await message.answer("❌ Avval login qilishingiz kerak.")
        await state.clear()
        return

    if message.text.lower() == "ha":
        data = await state.get_data()
        recipe = await create_recipe(data, user)
        await message.answer(f"🎉 Retsept saqlandi: {recipe.title}")
    else:
        await message.answer("❌ Bekor qilindi.")
    await state.clear()



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
