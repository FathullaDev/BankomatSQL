import os
import sys
import psycopg2
connection=psycopg2.connect(
    host='localhost',
    user='postgres',
    password='123',
    dbname='postgres'
)
cursor=connection.cursor()
proceed=True
class Card:
    def __init__(self,card_number,pin_code,card_validity,balance):
        self.card_number=card_number
        self.pin_code=pin_code
        self.card_validity=card_validity
        self.balance=balance

class Bankomat:
    def __init__(self):
        self.current_card_number = None
        self.current_card_key = None
        self.proceed=True

    def show_balance(self,current_card_number):
        cursor.execute(f"select balance from cards where card_number=%s",(current_card_number,))
        print(cursor.fetchone()[0])
        print("Amalyot yakunlandi")
        exit()

    def check_number_card(self,current_card_number):
        card_pin_code=None
        card_key=None
        cursor.execute("SELECT 1 FROM cards WHERE card_number = %s", (current_card_number,))
        exists=cursor.fetchone()
        if exists:
            if current_card_number.endswith('x'):
                exit("Karta bloklangan!")
            cursor.execute(f"select pin_code from cards "
                                         f"where card_number = %s", (current_card_number,))
            row=cursor.fetchone()
            c=row[0]
            card_pin_code=str(c).strip()
            # print(card_pin_code[0])
            attempt = 0
            while True:
                # print(card_pin_code)
                card_code = str(input("PIN-kodni kiriting: "))
                clear_console()
                if card_code == card_pin_code:
                    break
                else:
                    print("PIN-kod xato!", end="")
                    attempt += 1
                if attempt < 3:
                    print(f"urinishalr soni: {3 - attempt}")
                if attempt == 3:
                    cursor.execute(
                        f"UPDATE cards SET card_number ={current_card_number + 'x'}"
                        f"WHERE card_number={current_card_number}")
                    connection.commit()
                    cursor.close()
                    connection.close()
                    exit("\nPIN-kodni 3 marta noto‘g‘ri kiritdingiz. Kartangiz bloklandi!")

    def cash_withdrawal(self):
        card_balance=cursor.execute(f"select balance from cards where card_number={current_card_number}")
        amount = int(input("Summani kiriting: "))
        clear_console()
        new_balance = float(card_balance) - (amount + amount / 100)

        if new_balance < 0:
            exit("Mablag' yetarli emas!")
        else:
            cursor.execute(
                f"UPDATE cards SET balance ={new_balance}"
                f"WHERE card_number={current_card_number}")
            connection.commit()
            cursor.close()
            connection.close()
            print("Yechilgan:", amount, "so'm")
            print("Komissiya:", amount / 100, "so'm")
            print("Jami:", amount + amount / 100, "so'm")
            print(f"Qoldiq: {new_balance} - so'm")

    def money_to_card(self):
        fill_amount = int(input("Summani kiriting: "))
        card_balance = cursor.execute(f"select balance from cards where card_number={current_card_number}")
        new_balance = float(card_balance) + fill_amount - fill_amount / 100
        cursor.execute(
            f"UPDATE cards SET balance ={new_balance}"
            f"WHERE card_number={current_card_number}")
        connection.commit()
        cursor.close()
        connection.close()
        print("Kiritildi:", f"{float(fill_amount):,}", "so'm")
        print("Komissiya:", f"{float(fill_amount) / 100:,}", "so'm")
        print("To'ldirildi:", f"{float(fill_amount) - float(fill_amount) / 100:,}", "so'm")
        print("Qoldiq:", new_balance)



def clear_console():
    if sys.stdout.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n"*30)

bankomat = Bankomat()

while True:
    if proceed or bankomat.proceed:
        current_card_number = str(input("Xush kelibsiz!\nKartangizni kiriting: "))
        bankomat.current_card_number=current_card_number
        clear_console()
        bankomat.check_number_card(current_card_number)
    print("Amalyotni turini tanlang")
    print("1 - Balansni ko'rish\n2 - Naqd pul olish\n3 - Kartani to'ldirish\n4 - Amalyotni yakunlash")
    operation_key = int(input("Kiriting: "))
    clear_console()
    if operation_key==1:
        bankomat.show_balance(current_card_number)
        proceed=False
        bankomat.proceed=False
    elif operation_key==2:
        bankomat.cash_withdrawal()
        proceed = False
        bankomat.proceed = False
    elif operation_key==3:
        bankomat.money_to_card()
        proceed = False
        bankomat.proceed = False
    elif operation_key==4:
        print("Amalyot yakunlandi!")
        break