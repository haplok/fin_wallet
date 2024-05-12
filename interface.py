# Файл, реализующий интерфейс взаимодействия с кошельком
import os

from model import *
from templates import *

class Fin_wallet:
    ''' Класс интерфейса кошелька с логикой перехода по разделам'''
    def menu(self) -> None:
        ''' Метод для отображения основного меню'''
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            match input(main_menu_text):
                case '1': self.get_balance()
                case '2': self.write_record()
                case '3': self.update_record()
                case '4': self.find_records()
                case '0': raise SystemExit
                case _: 
                    os.system('cls' if os.name == 'nt' else 'clear')
                    input(exception_go_menu)                

    def balance_simple(self) -> None:
        ''' Метод для отображения простого баланса'''
        os.system('cls' if os.name == 'nt' else 'clear')
        d = Data()
        d.read_records()
        inc_mask = Mask(mask_category='Доход')
        spend_mask = Mask(mask_category='Расход')
        income = sum(map(lambda x: x.amount, d.get_filtr_records(inc_mask)))
        spend = sum(map(lambda x: x.amount, d.get_filtr_records(spend_mask)))
        input(balance_simple_text%(income-spend,income,spend))
        
    def balance_full(self) -> None:
        ''' Метод для отображения развернутого баланса'''
        os.system('cls' if os.name == 'nt' else 'clear')
        d = Data()
        d.read_records()
        inc_mask = Mask(mask_category='Доход')
        spend_mask = Mask(mask_category='Расход')
        inc_filtred = d.get_filtr_records(inc_mask)
        spend_filtred = d.get_filtr_records(spend_mask)
        income = sum(map(lambda x: x.amount, inc_filtred))
        spend = sum(map(lambda x: x.amount, spend_filtred))
        print(balance_full_text[0]%income)
        for i_f in inc_filtred:
            print(i_f)
        print(balance_full_text[1]%spend)
        for s_f in spend_filtred:
            print(s_f)
        print(balance_full_text[2]%(income-spend))
        input("\nНАЖМИТЕ ENTER ДЛЯ ВОЗВРАТА В МЕНЮ")

    def get_balance(self) -> None:
        ''' Метод для меню баланса'''
        os.system('cls' if os.name == 'nt' else 'clear')
        key = input(balance_menu_text)
        match key:
            case '1': self.balance_simple()
            case '2': self.balance_full()
            case '0': return
            case _:
                input(exception_go_menu)
                      
    def id_field_validation(self, id: str = None, empty_field = True) -> bool:
        ''' Метод для валидации поля id'''
        if id:
            if not id.isdigit():
                input(exception_go_menu)
                return False
        else:
            if not empty_field:
                input(exception_go_menu)
                return False
        return True
    
    def date_field_validation(self, record_date: str = None, empty_field = True) -> bool:
        ''' Метод для валидации поля record_date'''
        if record_date:
            if (len(record_date.split("-")) != 3 or 
            not record_date.split("-")[0].isdigit() or
            not record_date.split("-")[1].isdigit() or
            not record_date.split("-")[2].isdigit() or
            not 1900 <= int(record_date.split("-")[0]) <= 2100 or
            not 1 <= int(record_date.split("-")[1]) <= 12 or
            not 1 <= int(record_date.split("-")[2]) <= 31):
                input(exception_go_menu)
                return False
        else:
            if not empty_field:
                input(exception_go_menu)
                return False
        return True

    def category_field_validation(self, cat: str = None, empty_field = True) -> bool:
        ''' Метод для валидации поля category'''
        if cat:
            if cat not in ('Д', 'д', 'Р', 'р'): 
                input(exception_go_menu)
                return False
        else:
            if not empty_field:
                input(exception_go_menu)
                return False
        return True
    
    def amount_field_validation(self, amount: str = None, empty_field = True) -> bool:
        ''' Метод для валидации поля amount'''
        if amount:
            if amount.isalpha():
                input(exception_go_menu)
                return False
        else:
            if not empty_field:
                input(exception_go_menu)
                return False
        return True

    def create_new(self) -> None | Record:
        ''' Метод для отображения создения новой записи'''
        os.system('cls' if os.name == 'nt' else 'clear')
        record_date = input("Введите дату записи yyyy-mm-dd: \t")
        if not self.date_field_validation(record_date, empty_field = False): return     
        cat = input("[Д]оход или [Р]асход: \t\t\t")
        if not self.category_field_validation(cat, empty_field = False): return
        category = ""
        match cat:
            case "Д": category = "Доход"
            case "д": category = "Доход"
            case "Р": category = "Расход"
            case "р": category = "Расход"
        
        amount = input("Введите сумму: \t\t\t\t")
        if not self.amount_field_validation(amount, empty_field = False): return
        
        discription = input("Напишите описание: \t\t\t")

        rec = Record(0, record_date, category, amount, discription)
        return rec
        
    def write_record(self) -> None:
        ''' Метод для отображения записи в файл'''
        rec = self.create_new()
        if not rec: return
        data = Data()
        data.create_new_record(rec)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\tВы ввели новую запись: ")
        print(rec)
        input("\nНАЖМИТЕ ENTER ДЛЯ ВОЗВРАТА В МЕНЮ")     

    def update_record(self) -> None:
        ''' метод для отображения внесения из менений в файл'''
        os.system('cls' if os.name == 'nt' else 'clear')
        
        key = input(edit_menu_text)
        match key:
            case '1': self.find_records(key='edit')
            case '2': self.find_records(key='delete')
            case '0': return
            case _:
                input(exception_go_menu)
                
    def find_records(self, key: str = None) -> None:
        ''' Метод для отображения поиска записей с возможностью последующего редактирования, в случае найденой одной записи'''
        os.system('cls' if os.name == 'nt' else 'clear')
        search_fields = []
        for i, s_t in enumerate(search_text):
            if i == 0:
                print(s_t)
            else:
                inp = input(s_t)
                if i in (1,2):
                    if not self.id_field_validation(id=inp): return
                    search_fields.append(int(inp) if inp != '' else None)
                elif i in (3,4):
                    if not self.date_field_validation(record_date=inp): return
                    search_fields.append(inp if inp != '' else None)
                elif i in (5,):
                    if not self.category_field_validation(cat=inp): return
                    search_fields.append(inp if inp != '' else None)
                elif i in (6,7):
                    if not self.amount_field_validation(amount=inp): return
                    search_fields.append(int(inp) if inp != '' else None)
                elif i in (8,):
                    search_fields.append(inp if inp != '' else None)
        d = Data()
        d.read_records()
        m = Mask(*search_fields)
        records = d.get_filtr_records(m)
        os.system('cls' if os.name == 'nt' else 'clear')
        if not key or len(records) != 1:
            print(f"По вашему запросу найдено {len(records)} записей: ")
            for record in records:
                print(record.record_id, record, sep = "\t")
            if key:
                print("Найдена не одна запись, нужно уточнить запрос.\n")
            input("\nНАЖМИТЕ ENTER ДЛЯ ВОЗВРАТА В МЕНЮ")
        else:
            print(f"По вашему запросу найдена запись: ")
            print(records[0].record_id, records[0], sep = "\t")
            if key == 'edit':
                new_record = self.create_new()
                if not new_record: return
                d.update_record(records[0], new_record)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\tВы изменили:\n{records[0]}\n\tНа:\n{new_record}")
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                response = input(f"Введите [Удалить] для подтверждения удаления записи:\n{records[0]}\n")
                if response == 'Удалить':
                    d.delete_record(records[0])
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\tВы удалили запись: \n", records[0])
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Запись:\n{records[0]}\nНЕ БЫЛА УДАЛЕНА")
            input("\nНАЖМИТЕ ENTER ДЛЯ ВОЗВРАТА В МЕНЮ")
        

