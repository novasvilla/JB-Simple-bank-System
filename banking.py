class bankingSystem():
    import random
    import sqlite3
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    accounts = {}

    def __init__(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS card'
                         '(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
        self.conn.commit()
        self.welcome()

    def showbalane(self, card, pin):
        self.cur.execute('SELECT balance FROM card WHERE number = ?', (card,))
        row = self.cur.fetchone()
        print(row[0])
        self.balance(card, pin)

    def balance(self, card, pin):
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        user_input = int(input())
        if user_input == 1:
            self.showbalane(card, pin)
        if user_input == 5:
            print('You have successfully logged out!')
            self.welcome()
        if user_input == 2:
            self.add_income(card, pin)
        if user_input == 3:
            self.do_transfer(card, pin)
        if user_input == 4:
            self.close_account(card, pin)
        else:
            exit()

    def generate_account(self):
        inn = 400000
        can = self.random.randrange(100000000, 999999999)  # customer account number
        checksum = self.luhnalgoritmun(inn, can)
        # random.sed(can)
        pin = self.random.randrange(1000, 9999)
        number = ''.join(str(inn) + str(can) + str(checksum))
        self.cur.execute('INSERT INTO card(number,pin) VALUES (?, ?)', (number, pin))
        self.conn.commit()
        print("Your card has been created")
        print('Your card number:')
        print(number)
        print('Your card PIN:')
        print(pin)
        self.welcome()

    def logging(self):
        print('Enter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        self.cur.execute('SELECT * FROM card WHERE number = ?', (card,))
        row = self.cur.fetchall()
        if len(row) < 1 or row is None:
            print('wrong card number or PIN!')
        elif row[0][2] != pin:
            print('wrong card number or PIN!')
        else:
            print("You have successfully logged in!")
            self.balance(card, pin)

    def welcome(self):
        while True:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            userinput = int(input())
            if userinput == 1:
                self.generate_account()
            if userinput == 2:
                self.logging()
            else:
                print("Bye!")
                self.conn.close()
                exit()

    @staticmethod
    def luhnalgoritmun(inn, can):
        card = list(''.join(str(inn) + str(can)))

        checksum = 0
        i = 0
        for item in card:
            if (i + 1) % 2 != 0 or i == 0:
                card[i] = int(item) * 2
            if int(card[i]) > 9:
                card[i] = int(card[i]) - 9
            i += 1
        total = 0
        for item in card:
            total += int(item)
        while (total + checksum) % 10 != 0:
            checksum += 1
        return checksum

    def add_income(self, card, pin):
        income = input('Enter income: ')
        self.cur.execute('SELECT balance FROM card WHERE number = ?', (card,))
        old_balance = self.cur.fetchone()[0]
        new_balnce = int(old_balance) + int(income)
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balnce, card,))
        self.conn.commit()
        print('Income was added!')
        self.balance(card, pin)

    def add_tranference(self, card, remote_card, pin, money):
        self.cur.execute('SELECT balance FROM card WHERE number = ?', (remote_card,))
        old_balance = self.cur.fetchone()[0]
        new_balance = int(old_balance) + int(money)
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balance, remote_card,))
        self.conn.commit()
        self.balance(card, pin)

    def do_transfer(self, card, pin):
        remote_card = input('Enter card number: ')
        if remote_card == card:
            print("You can't transfer money to the same account!")
        elif not self.pass_luhnalgoritmun(remote_card):
            print("Probably you made a mistake in the card number. Please try again!")
        elif self.account_exist(remote_card):
            money = input('Enter how much money you want to transfer: ')
            # Update local account money minus money to transfer
            self.cur.execute('SELECT balance FROM card WHERE number = ?', (card,))
            old_balance_local = self.cur.fetchone()[0]
            if int(old_balance_local) >= int(money):
                new_balance_local = int(old_balance_local) - int(money)
                self.cur.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balance_local, card,))
                self.conn.commit()
                # Update Remote account money\
                self.add_tranference(card, remote_card, "0000", money)
                print('Success!')

            else:
                print('Not enough money!')

        else:
            print("Such a card does not exist.")
        self.balance(card, pin)

    def close_account(self, card, pin):
        self.cur.execute('DELETE FROM card WHERE number = ?', (card,))
        self.conn.commit()
        print('The account has been closed!')
        self.welcome()

    def account_exist(self, remote_card):
        self.cur.execute('SELECT * FROM card WHERE number = ?', (remote_card,))
        row = self.cur.fetchall()
        if len(row) < 1 or row is None:
            return False
        else:
            return True

    def pass_luhnalgoritmun(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0


metropolitan = bankingSystem()
