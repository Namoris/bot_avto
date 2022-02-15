# -*- coding: utf-8 -*-
import os
import sqlite3
import string

from datetime import date, timedelta, datetime
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor


BOT_TOKEN = ''
PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:13317'



count_clcht = 2
n_clcht = 0

clchtid = [1086192049, 1029425997, 109425997, 1019880252 ]
clchtidrez = []


pathtopdf = r'..'
zayavkastr = 'Ваш запрос обрабатывается. Время генерации отчета 5-30 минут. Ожидайте.'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

admins = [157460875, 369935862]
m_pswd = ['1']

m_comm = ['reg_cl', 'del_cl', 'show_cl', 'mass_mail', 'ch_acc', 'send_msg', 'show_cl_id', 'set_bonus', 'add_in_activ_cl', 'del_activ_cl', 'show_comm', 'set_count_clcht', 'show_name_db']
m_db = ['nm', 'id', 'date_end', 'acc', 'date_bgn', 'date_reg', 'cnt_request', 'f_name', 'l_name', 'ref', 'cnt_bonus']

mNN = {}
count_request_today = 0
_today = date.today()

conn = sqlite3.connect('DB_clients.db')
cursor = conn.cursor()



#cursor.execute('''CREATE TABLE clients (nm text, id text, date_end text, acc text) ''')
#cursor.execute('''CREATE TABLE nm_id (nm text, id text) ''')
#nm text, id text, date_end text, acc text, date_bgn text, date_reg text, cnt_request text, f_name text, l_name text, ref text, cnt_bonus text


prices = [
    types.LabeledPrice(label='Working Time Machine', amount=5750),
    types.LabeledPrice(label='Gift wrapping', amount=500),
]

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")

@dp.callback_query_handler(lambda c: c.data == 'oferta')
async def process_callback_button(callback_query: types.CallbackQuery):
    ff = open('oferta.docx', 'rb')
    await bot.send_document(callback_query.from_user.id, ff)
    ff.close()
    #await bot.answer_callback_query(callback_query.id)
    #print(callback_query)    

@dp.callback_query_handler(lambda c: c.data == 'ref')
async def process_callback_button(callback_query: types.CallbackQuery):
    ff = open('referal.docx', 'rb')
    await bot.send_document(callback_query.from_user.id, ff)
    ff.close()


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    print(message)
    await bot.send_message(message.chat.id,
                           'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                           ' as fast as possible! Stay in touch.'
                           '\n\nUse /buy again to get a Time Machine for your friend!'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')

@dp.message_handler(commands=['bonus'])
async def cmd_buy(message: types.Message):
    mci = message.chat.id
    sql = "SELECT * FROM clients WHERE id=?"
    cursor.execute(sql, [(mci)])
    cl = cursor.fetchone()
    if cl is None:
        await bot.send_message(mci, 'Номер Вашего телефона не зарегистрирован')
        await bot.send_message(mci,
                               '⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
        await bot.send_message(mci,
                               '⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
    else:
        inline_btn1 = types.InlineKeyboardButton('Добавить все дни к подписке', callback_data='use_all_bonus')
        inline_btn2 = types.InlineKeyboardButton('Добавить 10 дней к подписке', callback_data='use_10_bonus')
        inline_btn3 = types.InlineKeyboardButton('Вывести бонусы', callback_data='bonus_in_money')
        inline_btn4 = types.InlineKeyboardButton('Реферальная система бонусов', callback_data='ref')
        inline_kb = types.InlineKeyboardMarkup().add(inline_btn1)
        inline_kb.add(inline_btn2)
        inline_kb.add(inline_btn3)
        inline_kb.add(inline_btn4)
        s = 'Количество бонусных дней:\n%s\nВы можете:' % cl[10]
        await bot.send_message(mci, s, reply_markup=inline_kb)



@dp.callback_query_handler(lambda c: c.data == 'use_all_bonus')
async def process_callback_button(callback_query: types.CallbackQuery):
    mci = callback_query.from_user.id
    sql = "SELECT * FROM clients WHERE id=?"
    cursor.execute(sql, [(mci)])
    cl = cursor.fetchone()
    if cl is None:
        await bot.send_message(mci, 'Номер Вашего телефона не зарегистрирован')
        await bot.send_message(mci,
                               '⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
        await bot.send_message(mci,
                               '⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
    else:
        if cl[10] != '0':
            sql = 'UPDATE clients SET cnt_bonus = ?, date_end = ?  WHERE id = ?'
            d_e = datetime.strptime(cl[2], '%Y-%m-%d').date()
            d_e = d_e + timedelta(days=(int(cl[10])))
            cursor.execute(sql, (0, d_e, mci))
            s = 'BotinfoCar 🚗, [%s]\n💳 Подписка на BotinfoCar оплачена до %s. Спасибо!' % (date.today(), d_e)
            await bot.send_message(mci, s)
            conn.commit()
        else:
            await bot.send_message(mci, 'К сожалению, у Вас не осталось бонусных дней.\nПриглашайте друзей и получайте бонусы вместе!')

@dp.callback_query_handler(lambda c: c.data == 'use_10_bonus')
async def process_callback_button(callback_query: types.CallbackQuery):
    mci = callback_query.from_user.id
    sql = "SELECT * FROM clients WHERE id=?"
    cursor.execute(sql, [(mci)])
    cl = cursor.fetchone()
    if cl is None:
        await bot.send_message(mci, 'Номер Вашего телефона не зарегистрирован')
        await bot.send_message(mci,
                               '⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
        await bot.send_message(mci,
                               '⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
    else:
        if cl[10] != '0' and int(cl[10]) > 9:
            sql = 'UPDATE clients SET cnt_bonus = ?, date_end = ?  WHERE id = ?'
            d_e = datetime.strptime(cl[2], '%Y-%m-%d').date()
            d_e = d_e + timedelta(days=(10))
            cursor.execute(sql, (int(cl[10]) - 10, d_e, mci))
            s = 'BotinfoCar 🚗, [%s]\n💳 Подписка на BotinfoCar оплачена до %s. Спасибо!' % (date.today(), d_e)
            await bot.send_message(mci, s)
            conn.commit()
        else:
            await bot.send_message(mci, 'К сожалению, у Вас недостаточно бонусных дней.\nПриглашайте друзей и получайте бонусы вместе!')


@dp.callback_query_handler(lambda c: c.data == 'bonus_in_money')
async def process_callback_button(callback_query: types.CallbackQuery):
    mci = callback_query.from_user.id
    sql = "SELECT * FROM clients WHERE id=?"
    cursor.execute(sql, [(mci)])
    cl = cursor.fetchone()
    if cl is None:
        await bot.send_message(mci, 'Номер Вашего телефона не зарегистрирован')
        await bot.send_message(mci,
                               '⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
        await bot.send_message(mci,
                               '⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
    else:
        if cl[10] != '0' and int(cl[10]) > 60:
            await bot.send_message(admins[0], cl[0] + ' ' + cl[1] + ' хочет вывести бонусы\nКоличество бонусов:%s' % cl[10])
            await bot.send_message(admins[1], cl[0] + ' ' + cl[1] + ' хочет вывести бонусы\nКоличество бонусов:%s' % cl[10])

            s = 'Ваша заявка будет рассмотренна в ближайшее время, после чего с Вами свяжется один из администраторов!\nСпасибо за ожидание!'
            await bot.send_message(mci, s)
        else:
            await bot.send_message(mci, 'К сожалению, у Вас недостаточно бонусных дней.\nПриглашайте друзей и получайте бонусы вместе!')


@dp.message_handler(commands=['start'])
async def cmd_buy(message: types.Message):
    print(1)
    await bot.send_message(message.chat.id, '⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
    await bot.send_message(message.chat.id,'⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
    await bot.send_message(message.chat.id, 'По возникшим вопросам обращайтесь по телефону: 89997188148 \nИли на нашу почту: \nBotinfocar@gmail.com')


    '''await bot.send_invoice(message.chat.id, title='Working Time Machine',
                           description='Want to visit your great-great-great-grandparents?'
                                       ' Make a fortune at the races?'
                                       ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
                                       ' Order our Working Time Machine today!',
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='RUB',
                           #photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='time-machine-example',
                           payload='123456789')
    '''

@dp.message_handler(commands = [ 'help' ])
async def handle_start_help(message):
    await bot.send_message(message.chat.id,'По возникшим вопросам обращайтесь по телефону: 89997188148 \nИли на нашу почту: \nBotinfocar@gmail.com')


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    global n_clcht
    global count_clcht
    global _today
    global count_request_today
    mci = message.chat.id
    print(mci)
    if mci not in clchtid:
        if message.text.split()[0].lower() in m_comm:
            if mci in admins:
                if message.text.split()[1] in m_pswd:
                    print(message.text.split()[1])
                    if message.text.split()[0].lower() == 'reg_cl':
                        tel = message.text.split()[3][-10:]
                        count_mnth = int(message.text.split()[2])
                        sql = "SELECT * FROM clients WHERE nm=?"
                        cursor.execute(sql, [(tel)])
                        cl = cursor.fetchone()
                        if cl is None:
                            await bot.send_message(message.chat.id, 'Номера нет в базе')
                        else:
                            print(cl)
                            sql = 'UPDATE clients SET date_end = ?, acc = ? WHERE id = ?'
                            if cl[2] == '':
                                
                                d_e = date.today() + timedelta(days=(count_mnth * 10))
                                cursor.execute(sql, (d_e, 1, cl[1]))
                                sql = 'UPDATE clients SET date_bgn = ?, cnt_request = ? WHERE id = ?'
                                cursor.execute(sql, (date.today(), 0, cl[1]))
                            else:
                                d_e = datetime.strptime(cl[2], '%Y-%m-%d').date()
                                if d_e < date.today():
                                    sql = 'UPDATE clients SET date_bgn = ?, cnt_request = ? WHERE id = ?'
                                    cursor.execute(sql, (date.today(), 0, cl[1]))
                                    sql = 'UPDATE clients SET date_end = ?, acc = ? WHERE id = ?'
                                    d_e = date.today() + timedelta(days=(count_mnth * 10))
                                else:
                                    d_e = d_e + timedelta(days=(count_mnth * 10))
                                cursor.execute(sql, (d_e, 1, cl[1]))
                            conn.commit()
                            print(d_e)
                            if cl[9] != '':
                                sql = "SELECT * FROM clients WHERE nm=? and acc = '1'"
                                cursor.execute(sql, [(cl[9])])
                                ref = cursor.fetchone()
                                if ref is not None:
                                    sql = 'UPDATE clients SET cnt_bonus = ? WHERE id = ?'
                                    cursor.execute(sql, (int(ref[10]) + 4, ref[1]))
                                    await bot.send_message(ref[1], '⭐️ Поздравляем, Ваш друг оплатил доступ в BotinfoCar и к вашей подписке добавленно 4 бонусных дня!')
                                    sql = 'UPDATE clients SET cnt_bonus = ? WHERE id = ?'
                                    cursor.execute(sql, (int(cl[10]) + 2, cl[1]))
                                    inline_btn2 = types.InlineKeyboardButton('Реферальная система бонусов', callback_data='ref')
                                    inline_kb = types.InlineKeyboardMarkup().add(inline_btn2)
                                    nmes = '⭐️ Вам добавлено 2 бонусных дня к основному тарифу по реферальной системе бонусов!Ознакомиться с ней Вы можете, нажав кнопку ниже:'
                                    await bot.send_message(cl[1], nmes, reply_markup = inline_kb)
                                    if ref[9] != '':
                                        sql = "SELECT * FROM clients WHERE nm=? and acc = '1'"
                                        cursor.execute(sql, [(ref[9])])
                                        ref1 = cursor.fetchone()
                                        if ref1 is not None:
                                            sql = 'UPDATE clients SET cnt_bonus = ? WHERE id = ?'
                                            cursor.execute(sql, (int(ref1[10]) + 1, ref1[1]))
                                            await bot.send_message(ref1[1], '⭐️ Поздравляем, Ваш друг пригласил друга и он оплатил доступ в BotinfoCar! К вашей подписке добавлен 1 бонусный день!')
                                    conn.commit()
                            sql = "SELECT * FROM clients WHERE ref=? and acc = '1'"
                            cursor.execute(sql, [(tel)])
                            refs = cursor.fetchall()
                            for r in refs:
                                sql = 'UPDATE clients SET cnt_bonus = ? WHERE id = ?'
                                cursor.execute(sql, (int(r[10]) + 2, r[1]))
                                await bot.send_message(r[1], '⭐️ Вам добавлено 2 бонусных дня к основному тарифу по реферальной системе бонусов!')

                            print(d_e)
                            conn.commit()
                            await bot.send_message(message.chat.id, 'ok')
                            s = 'BotinfoCar 🚗, [%s]\n💳 Подписка на BotinfoCar оплачена до %s. Спасибо!' % (date.today(), d_e)
                            await bot.send_message(cl[1], s)
                        sql = "SELECT * FROM clients"
                        cursor.execute(sql)
                        res = cursor.fetchall()
                        print(res)

                    elif message.text.split()[0].lower() == 'del_cl':
                        tel = message.text.split()[2][-10:]
                        sql = "SELECT * FROM clients WHERE nm=?"
                        cursor.execute(sql, [(tel)])
                        cl = cursor.fetchone()
                        if cl is None:
                            await bot.send_message(message.chat.id, 'Номера нет в базе')
                        else:
                            sql = "delete from clients where id = ?"
                            cursor.execute(sql, (cl[1],))
                            conn.commit()
                            await bot.send_message(message.chat.id, 'ok')

                    elif message.text.split()[0].lower() == 'send_msg':
                        id = message.text.split()[2]
                        sql = "SELECT * FROM clients WHERE id=?"
                        cursor.execute(sql, [(id)])
                        cl = cursor.fetchone()
                        if cl is None:
                            await bot.send_message(message.chat.id, 'Нет в базе')
                        else:
                            await bot.send_message(id, message.text[message.text.find(message.text.split()[3]):])
                            await bot.send_message(message.chat.id, 'ok')

                    elif message.text.split()[0].lower() == 'set_count_clcht':
                        global count_clcht
                        count_clcht = int(message.text.split()[2])
                        await bot.send_message(message.chat.id, 'ok')

                    elif message.text.split()[0].lower() == 'ch_acc':
                        tel = message.text.split()[2][-10:]
                        sql = "SELECT * FROM clients WHERE nm=?"
                        cursor.execute(sql, [(tel)])
                        cl = cursor.fetchone()
                        if cl is None:
                            await bot.send_message(message.chat.id, 'Номера нет в базе')
                        else:
                            sql = "UPDATE clients SET acc = ? WHERE nm = ?"
                            acc = int(cl[3]) ^ 1
                            cursor.execute(sql, (acc, tel))
                            print(1111)
                            conn.commit()
                            if not acc:
                                await bot.send_message(cl[1], '⭐️ Бесплатный лимит запросов исчерпан. Стоимость дальнейшего использования сервиса - 1179 рублей в месяц. После оплаты Вам будет доступно неограниченное количество запросов.')
                            await bot.send_message(message.chat.id, 'ok')


                    elif message.text.split()[0].lower() == 'set_bonus':
                        tel = message.text.split()[2][-10:]
                        cnt_b = message.text.split()[3]
                        sql = "SELECT * FROM clients WHERE nm=?"
                        cursor.execute(sql, [(tel)])
                        cl = cursor.fetchone()
                        if cl is None:
                            await bot.send_message(message.chat.id, 'Номера нет в базе')
                        else:
                            sql = "UPDATE clients SET cnt_bonus = ? WHERE nm = ?"
                            cursor.execute(sql, (cnt_b, tel))
                            conn.commit()
                            await bot.send_message(message.chat.id, 'ok')


                    elif message.text.split()[0].lower() == 'show_cl_id':
                        for my_cl in clchtid:
                            await bot.send_message(mci, my_cl)
                        await bot.send_message(mci, count_clcht)

                    elif message.text.split()[0].lower() == 'show_comm':
                        for my_comm in m_comm:
                            await bot.send_message(mci, my_comm)

                    elif message.text.split()[0].lower() == 'show_name_db':
                        for my_db in m_db:
                            await bot.send_message(mci, my_db)

                    elif message.text.split()[0].lower() == 'show_cl':
                        if len(message.text.split()) > 2:
                            sql = "SELECT * FROM clients WHERE %s = %s" % (message.text.split()[2], message.text.split()[3])
                            cursor.execute(sql)
                        else:
                            sql = "SELECT * FROM clients"
                            cursor.execute(sql)
                        shw_cl = cursor.fetchall()
                        print(shw_cl)
                        ms = ''
                        n = 0
                        for one_cl in shw_cl:
                            ms = ms + str(one_cl) + '\n'
                            n += 1
                            if n % 10 == 0:
                                await bot.send_message(message.chat.id, ms)
                                ms = ''
                        if ms == '':
                            ms = 'всё'
                        await bot.send_message(message.chat.id, ms)
                        await bot.send_message(message.chat.id, 'Зарегистрировано: ' + str(n))
                        await bot.send_message(message.chat.id, 'Запросов сегодня: ' + str(count_request_today))

                    elif message.text.split()[0].lower() == 'mass_mail':
                        print('mmass')
                        sql = "SELECT * FROM clients"
                        cursor.execute(sql)
                        shw_cl = cursor.fetchall()
                        print(shw_cl)
                        for cl_row in shw_cl:
                            try:
                                await bot.send_message(cl_row[1], message.text[12:])
                            except:
                                await bot.send_message(admins[0], cl_row[1] + ' скорее всего заблокировал чат с ботом')
                                await bot.send_message(admins[1], cl_row[1] + ' скорее всего заблокировал чат с ботом')


                    elif 'add_in_activ_cl' in message.text.split()[0].lower():
                        cl_id = int(message.text.split()[2])
                        print(clchtidrez)
                        if cl_id in clchtidrez:
                            clchtid.append(cl_id)
                            clchtidrez.remove(cl_id)
                            
                            await bot.send_message(admins[0], 'ok')
                        else:
                            await bot.send_message(admins[0], 'Такого id нет')


                    elif 'del_activ_cl' in message.text.split()[0].lower():
                        cl_id = int(message.text.split()[2])
                        if cl_id in clchtid:
                            clchtid.remove(cl_id)
                            
                            await bot.send_message(admins[0], 'ok')
                        else:
                            await bot.send_message(admins[0], 'Такого id нет')

        elif 'show_my_id' in message.text.split()[0].lower():
            await bot.send_message(mci, mci)

        elif 'add_me_in_rez' in message.text.split()[0].lower():
            if message.text.split()[1].lower() in m_pswd:
                clchtidrez.append(mci)
                await bot.send_message(admins[0], 'new cl: ' + str(mci))
                await bot.send_message(mci, 'ok')


        elif 'reg' in message.text.split()[0].lower():
            print(message.text)
            print(message)
            tel = message.text.split()[1][-10:]
            ref = ''
            if len(message.text.split()) == 3:
                ref = message.text.split()[2][-10:]
            sql = "SELECT * FROM clients WHERE id=?"
            cursor.execute(sql, [(mci)])
            res = cursor.fetchone()
            print(res)
            print(mci)
            if ref == tel:
                await bot.send_message(mci, 'Хитро! Но так нельзя)')
                ref = ''
            if res is None:
                sql = "INSERT INTO clients (nm, id, date_end, acc, date_bgn, date_reg, cnt_request, f_name, l_name, ref, cnt_bonus) VALUES (?, ?, '', 0, '', ?, 0, ?, ?, ?, 0)"
                print(ref)
                cursor.execute(sql, (tel, mci, date.today(), message.from_user.first_name, message.from_user.last_name, ref))
            else:
                print(mci)
                sql = "UPDATE clients SET nm = ? WHERE id = ?"
                cursor.execute(sql, (tel, mci))
                if res[7] == None:
                     sql = "UPDATE clients SET f_name = ? WHERE id = ?"
                     cursor.execute(sql, (message.from_user.first_name, mci))
                if res[5] == None:
                     sql = "UPDATE clients SET date_reg = ? WHERE id = ?"
                     cursor.execute(sql, (date.today(), mci))
                if res[8] == None:
                     sql = "UPDATE clients SET l_name = ? WHERE id = ?"
                     cursor.execute(sql, (message.from_user.last_name, mci))
                sql = "UPDATE clients SET ref = ? WHERE id = ?"
                cursor.execute(sql, (ref, mci))

            conn.commit()
            inline_btn1 = types.InlineKeyboardButton('Договор оферты', callback_data = 'oferta')
            inline_btn2 = types.InlineKeyboardButton('Реферальная система бонусов', callback_data='ref')
            inline_kb = types.InlineKeyboardMarkup().add(inline_btn1)
            inline_kb.add(inline_btn2)
            s = '''Для оплаты переведите рублей на карту Сбербанка  \nВ коментарии платежа укажите Ваш телефонный номер.\nПлатежи на карту обрабатываются в ручном режиме. После оплаты возможно задержка 5-20 минут. Ночные платежи обрабатываются утром.\nПосле оплаты Вы получите доступ к информационной проверке истории автомобиля в BotinfoCar.\nПроизведя оплату, Вы подтверждаете ознакомление, согласие и принятие условий договора ОФЕРТЫ.'''
            await bot.send_message(mci, s, reply_markup = inline_kb)

            
        else:

            sql = "SELECT * FROM clients WHERE id=?"
            cursor.execute(sql, [(mci)])
            cl = cursor.fetchone()
            if cl is None:
                await bot.send_message(mci, 'Номер Вашего телефона не зарегистрирован')
                await bot.send_message(mci,'⭐️Для регистрации Вам необходимо отправить боту сообщение следующего формата:\n"reg [Ваш номер телефона]"\nНапример: reg 89991234567')
                await bot.send_message(mci, '⭐️Привел друг? Отметьте его и получите 2 бонусных дня при оплате тарифа!\nВведите: reg [Ваш номер телефона] [Номер телефона друга]\nПример: reg 899912345678 89309876543.')
            else:
                if cl[3] == '0':
                    await bot.send_message(mci, 'Для работы с BotinfoCar необходимо оплатить подписку')
                elif cl[3] == '1':
                    msg = message.text.replace(' ', '')
                    if msg[:1] in ['+', '7', '8', '9']:
                        msg = ''.join([str(i) for i in msg if i in '0123456789'])
                        msg = '7' + msg[-10:]
                    mNN[msg.upper()] = mci
                    
                    if _today == date.today():
                        count_request_today += 1
                    else:
                        _today = date.today()
                        count_request_today = 0
                    #await bot.send_message(mci, zayavkastr)
                    if (len(msg) > 17) or ('188.120.251.13' in msg):
                        await bot.send_message(admins[1], 'Внимание!\nПодозрительное сообщение\n' + str(mci) + '%%%%%' + message.text)
                        await bot.send_message(admins[0], 'Внимание!\nПодозрительное сообщение\n' +  str(mci) + '%%%%%' + message.text)
                        await bot.send_message(mci, 'Неверный формат запроса')
                    elif set('oOQqIi').intersection(msg):
                         await bot.send_message(mci, '📝 VIN не может содержать в себе буквы I, O, Q из-за их сходства с цифрами 1, 0.')
                    else:
                        mNN[msg.upper()] = mci
                        await bot.send_message(clchtid[n_clcht], str(mci) + '%%%%%' + msg)
                    if cl[6] is None:
                        sql = "UPDATE clients SET cnt_request = 0 WHERE id = ?"
                        cursor.execute(sql, (mci))
                    else:
                        sql = "UPDATE clients SET cnt_request = ? WHERE id = ?"
                        cursor.execute(sql, (int(cl[6]) + 1, mci))
                    if cl[5] is None:
                        print(mci)
                        if res[7] == None:
                            sql = "UPDATE clients SET f_name = ? WHERE id = ?"
                            cursor.execute(sql, (message.from_user.first_name, mci))
                        if res[5] == None:
                            sql = "UPDATE clients SET date_reg = ? WHERE id = ?"
                            cursor.execute(sql, (cl[2], mci))
                        if res[8] == None:
                            sql = "UPDATE clients SET l_name = ? WHERE id = ?"
                            cursor.execute(sql, (message.from_user.last_name, mci))
                    conn.commit()
                    print(n_clcht)
                    n_clcht = (n_clcht + 1) % count_clcht
                    print(n_clcht)
                    print(cl[2])
                    print(date.today())
                    d_e = datetime.strptime(cl[2], '%Y-%m-%d').date()
                    if cl[3] == '1' and d_e < date.today():
                        sql = "UPDATE clients SET acc = ? WHERE id = ?"
                        cursor.execute(sql, (0, mci))
                        await bot.send_message(mci, '⭐️ Срок Вашей подписки окончен. Для дальнейшего использования сервиса оплатите 1179 рублей. После оплаты Вам будет доступно неограниченное количество запросов.')
                        conn.commit()



    else:
        print(mNN)
        #bot.send_message(mNN[message.text], '123')
        if 'fail' in message.text:
            await bot.send_message(mNN[message.text.split()[1]], 'К сожалению, по госномеру не удалось найти VIN автомобиля. Попробуйте повторить запрос позже, или запросите отчет по VIN автомобиля.')
            mNN.pop(message.text.split()[1])
        elif '&&&&&' in message.text:
            await bot.send_message(mNN[message.text.split('&&&&&')[0]], message.text.split('&&&&&')[1])
            if '188.120.251.13' in message.text: 
                
                mNN.pop(message.text.split('&&&&&')[0])
        #else:
            '''ff = open(message.text + '.pdf', 'rb')
            print(message.text + '.pdf')
            print(message.chat.id)
            await bot.send_document(mNN[message.text], ff)
            #bot.send_document(mNN[message.text], " FILEID ")
            ff.close()
            os.remove(message.text + '.pdf')'''


executor.start_polling(dp, skip_updates=True)
