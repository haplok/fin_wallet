# Файл, реализующий взаимодействие с данными.

from config import *

class Mask:
    ''' Класс реализует фильтрацию по полям класса Record'''
    def __init__(self, id_min: int = None, 
                 id_max: int = None, 
                 date_min: str = None, 
                 date_max: str = None, 
                 mask_category: str = None, 
                 amount_min: int = None, 
                 amount_max: int = None, 
                 mask_discription: str = None) -> None:
        self.id_min = id_min
        self.id_max = id_max
        self.date_min = date_min
        self.date_max = date_max
        self.mask_category = mask_category
        self.amount_min = amount_min
        self.amount_max = amount_max
        self.mask_discription = mask_discription


class Record:
    ''' Экземпляры данного класса соотвествуют записям в финансовом кошельке'''
    def __init__(self, record_id: int, record_date: str, category: str, amount: int, discription: str) -> None:
        self.record_id = int(record_id)
        rec_date = record_date.split("-")
        rec_date[1].zfill(2), rec_date[2].zfill(2)
        self.record_date = '-'.join(rec_date)
        self.category = category
        self.amount = int(amount)
        self.discription = discription
        

    def __repr__(self) -> str:
        return f'{self.record_date} \t{" " if self.category == "Доход" else "-"}{self.amount} \t{self.discription}'
    
    def __eq__(self, value: object) -> bool:
        if (self.record_id == value.record_id and
            self.record_date == value.record_date and
            self.category == value.category and
            self.amount == value.amount and
            self.discription == value.discription):
            return True
        else:
            return False


    def is_valid(self, mask: Mask = None) -> bool:
        ''' Метод для определения соотвествия экземпляра класса заданному фильтру(mask)'''
        if mask != None:
            if mask.id_min and mask.id_min > self.record_id:
                return False
            if mask.id_max and mask.id_max < self.record_id:
                return False
            if mask.date_min and mask.date_min > self.record_date:
                return False
            if mask.date_max and mask.date_max < self.record_date:
                return False
            if mask.mask_category and self.category.lower().find(mask.mask_category.lower()) == -1:
                return False
            if mask.amount_min and mask.amount_min > self.amount:
                return False
            if mask.amount_max and mask.amount_max < self.amount:
                return False
            if mask.mask_discription and self.discription.lower().find(mask.mask_discription.lower()) == -1:
                return False   
        return True

class Data:
    ''' Класс для работы с данными'''
    def read_records(self) -> list[Record]:
        ''' Метод для чтения всех записей из файла'''
        self.records = []
        with open(data_file, "r", encoding='utf8') as file:
            while True:
                record = file.readline().strip()
                if not record:
                    break
                r = Record(*record.split("•"))
                self.records.append(r)
        return self.records
        
    def get_filtr_records(self, mask:Mask = None) -> list[Record]:
        ''' Метод для фильтрации считанных записей с помощью фильтра mask'''
        return list(filter(lambda x: x.is_valid(mask), self.records))
    
    def create_new_record(self, record: Record) -> None:
        ''' Метод для добавление новой записи в конец файла'''
        prev_id = None
        with open(data_file, "r", encoding='utf8') as file:
            lines = file.readlines()
            if lines == []:
                prev_id = 0
                print(lines)
            else:
                prev_id = int(lines[-1].split("•")[0])
        with open(data_file, "a", encoding='utf8') as file:    
            file.write(f"{prev_id+1}•{record.record_date}•{record.category}•{record.amount}•{record.discription}\n")
            
    def delete_record(self, deleted_record: Record) -> None:
        ''' Метод для удаления конкретной записи из файла'''
        records = self.read_records()
        with open(data_file, "w", encoding='utf8') as file:
            for i, record in enumerate(records):
                if record != deleted_record:
                    file.write(f"{record.record_id}•{record.record_date}•{record.category}•{record.amount}•{record.discription}\n")
    
    def update_record(self, old_record: Record, new_record: Record) -> None:
        ''' Метод для изменения конкретной записи на новую'''
        records = self.read_records()
        with open(data_file, "w", encoding='utf8') as file:
            for record in records:
                if record == old_record:
                    id = record.record_id
                    record = new_record
                    record.record_id = id
                file.write(f"{record.record_id}•{record.record_date}•{record.category}•{record.amount}•{record.discription}\n")
