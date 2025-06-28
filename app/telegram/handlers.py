from aiogram import Router, types, F
from app.db import get_session
from app.models import User, Client
from sqlmodel import select
from aiogram.filters import Command
from app.ai import generate_reply, generate_offer

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот, который помогает продавать услуги.\n\n"
        "👉 Если ты предприниматель и хочешь продавать через меня — используй команду /become_a_lead\n"
        "💬 Если ты хочешь узнать о продукте — просто напиши мне сообщение"
    )


@router.message(Command("become_a_lead"))
async def register_user(message: types.Message):
    session = get_session()
    tg_id = message.from_user.id
    username = message.from_user.username
    user = session.exec(select(User).where(User.telegram_id == tg_id)).first()
    if not user:
        user = User(telegram_id=tg_id, username=username)
        session.add(user)
        session.commit()
        await message.answer("Вы зарегистрированы как лидер.")
    else:
        await message.answer("Вы уже зарегистрированы.")

@router.message(Command("add_client"))
async def add_client(message: types.Message):
    session = get_session()
    tg_id = message.from_user.id
    user = session.exec(select(User).where(User.telegram_id == tg_id)).first()
    if not user:
        await message.answer("Сначала используйте /start для регистрации.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Используйте: /add_client @username")
        return
    client_username = args[1].lstrip("@")
    client = Client(telegram_username=client_username, user_id=user.id)
    session.add(client)
    session.commit()
    await message.answer(f"Клиент @{client_username} добавлен.")

@router.message(Command("make_offer"))
async def make_offer(message: types.Message):
    session = get_session()
    tg_id = message.from_user.id
    user = session.exec(select(User).where(User.telegram_id == tg_id)).first()

    if not user:
        await message.answer("Сначала зарегистрируйтесь через /start.")
        return

    services_description = message.text.removeprefix("/make_offer").strip()
    if not services_description:
        await message.answer("Пожалуйста, введите описание ваших услуг после команды:\nПример: /make_offer Услуга по продвижению бизнеса за 7 дней")
        return
    
    # offer = await generate_offer(services_description) УТП от гпт
    offer = services_description

    user.offer = offer
    session.add(user)
    session.commit()
    await message.answer("УТП сохранено.")

@router.message()
async def handle_client_message(message: types.Message):

    print("Got message:", message.text)

    session = get_session()
    sender_username = message.from_user.username

    client = session.exec(select(Client).where(Client.telegram_username==sender_username)).first()
    if not client:
        await message.answer("Вы не являетесь клиентом ни одного продавца. Попросите своего продавца зарегистрировать вас как его клиента.")
        return
    
    user = session.get(User, client.user_id)
    if not user:
        await message.answer("Вы не являетесь клиентом ни одного продавца. Попросите своего продавца зарегистрировать вас как его клиента.")
        return
    
    if not client.offer_sent:
        if user.offer:
            await message.answer(user.offer)
            client.offer_sent=True
        
        else:
            await message.answer("Ваш продавец пока не добавил УТП.")
        
        session.add(client)
        session.commit()
        return
    
    else:
        gpt_reply = await generate_reply(
            client_message=message.text,
            leader_username=user.username,
            offer=user.offer
        )
        await message.answer(gpt_reply)

