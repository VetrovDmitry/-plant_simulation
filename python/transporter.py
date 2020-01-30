from myXOR import XOR as xor


class CreateDevice():
    """Класс создает девайс(датчик или камеру)
    
    Конструктор принимает в качестве аргументов имя девайса и частоту"""
    def __init__(self, name_='default', frequency_=100):
        self.characteristic = {
            'name': name_,
            'frequency': frequency_,
        }
    
    def deviceInfo(self):
        """Метод возвращает лист с характеристикой"""
        return self.characteristic
    
    def setInfo(self, char_name, value):
        """Метод добавляет или изменяет информацию о девайсе"""
        self.characteristic[char_name] = value

    def delInfo(self, char_name):
        """Метод удаляет информацию"""
        self.characteristic.pop(char_name)


class Bottle():
    """Класс генерирует заданное количество флаконов
    
    Конструктор принимает диаметр в качестве аргумента"""
    def __init__(self, diametr_=16, quantity_=50):
        self.bottle_size = diametr_
        self.quantity = quantity_
        self.start_coordinates = 0
     
    def getBottleSize(self):
        """Метод возвращает диаметр сгенерированной партии"""
        return self.bottle_size

    def get_bottles(self):
        """Метод возвращает партию флаконов"""
        bottles = list()
        while self.quantity != 0:
            bottles.append(self.bottle_size)
            self.quantity -=1
        return bottles


class Buffer():
    """Метод моделирует работу буфера зоны подачи на конвейер
    
    Конструктор создает кластер из сгенерированных флаконов с определенным промежутком между ними"""
    def __init__(self, max_count_=10, range_=1):
        self._items = list()
        self.item_count = 0 # - Счетчик поступивших единиц продукции
        self.max_count = max_count_ # - Максимальное количество флаконов в кластере
        self.B_B = range_  # mm - Расстояние между флаконами
    
    def putToBuffer(self, element):
        """Метод загружает сгенерированные единицы продукции в буфер зоны подачи"""
        start_position = 0 
        end_position = 0
        # Равномерное распределение продукции по конвейеру
        while xor(self.item_count != self.max_count,self.item_count != len(element)):
            end_position = start_position + element[self.item_count]
            self._items.append([start_position, end_position])
            start_position = (end_position + self.B_B)
            self.item_count += 1
            
        response = {
            'Bottles': self.item_count,
            'Max count': self.max_count,
            'Range': self.B_B,
            'length': self._items[-1][1]
            }
        return response

    def getCount(self):
        return self.item_count

    def getBuffer(self):
        return self._items
 
        
class Conveyor():
    """Класс моделирующий работу конвейера
    
    Конструктор принимает: длину конвейера, максимальную скорость перемещения ленты,
    относительную скорость ленты(в процентах)"""
    def __init__(self, velocity_proc_=50, length_=1200, max_speed_=300):
        max_velocity = max_speed_  # mm/sec - Максимальная скорость
        self.default_speed = velocity_proc_*(max_velocity/100)
        self.conveyor_length = length_  # mm - Длина конвейера
        self.x_coordinate = None
        self.timer = 0
        self.item_count = 0
        self.items = dict()
        self.information = dict()

    def setDevice(self, device, x_coordinate=0):
        """Метод устанавливает девайс на определенные координаты
        (по умолчанию x=0)"""
        self.dev_coordinate = x_coordinate

    def start(self):
        """Метод запускает конвейер"""
        count = 0
        while self.dev_coordinate < self.conveyor_length:
            self.dev_coordinate += 1
            self.timer += 1/self.default_speed
            count += self.__checkBuffer(self.dev_coordinate)
        self.information = {
                'time': self.timer,
                'count': count,
                }

    def __checkBuffer(self, coordinate):
        """Метод считает количество единиц продукции обработанных камерой"""
        count = 0
        for item in self.buffer:
            if coordinate <= item[1]:
                break
            elif coordinate > item[1]:
                self.buffer.remove(item)
                count +=1
        return count

    def putBufferToConv(self, buffer):
        """Метод отправляет сформированный в буфере кластер на конвейер"""
        self.buffer = buffer
        return self.buffer

    def analytics(self):
        """Метод рассчитывает скорость и время обработки продукции камерой"""
        speed = self.information.get('count')/self.information.get('time')
        self.information['speed']= int(speed)
        return self.information


if __name__ == "__main__":
    conveyor = Conveyor(50, 1200, 300)
    camera_1 = CreateDevice('Камера', 100)
    bottles_batch = Bottle(30, 2000).get_bottles
    origin_buffer = Buffer(100, 20)
    origin_buffer.putToBuffer(bottles_batch())
    buffer = origin_buffer.getBuffer()
    conveyor.putBufferToConv(buffer)
    conveyor.setDevice(camera_1)
    conveyor.start()
    stat = conveyor.analytics()
    print(stat)



