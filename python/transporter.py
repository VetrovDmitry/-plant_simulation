from myXOR import XOR as xor


class bottle():
    def __init__(self, diametr_=16):
        self.bottle_size = diametr_
        self.start_coordinates = 0
     
    def getBottleSize(self):
        return self.bottle_size

    def bottle_set(self, count):
        bottles = list()
        while count != 0:
            bottles.append(self.bottle_size)
            count -=1
        return bottles


class buffer():
    def __init__(self, max_count_=10, range_=1):
        self._items = list()
        self.item_count = 0
        self.max_count = max_count_
        self.B_B = range_  # mm
    
    def putToBuffer(self, element):
        start_position = 0
        end_position = 0
        while xor(self.item_count != self.max_count,self.item_count != len(element)):
            end_position = start_position + element[self.item_count]
            self._items.append([start_position, end_position])
            start_position = (end_position + self.B_B)
            self.item_count += 1
            
        response = {
            'Bottles': self.item_count,
            'Max count': self.max_count,
            'Range': self.B_B,
            }
        return response

    def getCount(self):
        return self.item_count

    def getBuffer(self):
        return self._items
    
    def getLong(self):
        return self._items[-1][1]
        

class conveyor():
    def __init__(self, velocity_proc_=50, length_=1200, max_speed_=300):
        max_velocity = max_speed_  # mm/sec
        self.default_speed = velocity_proc_*(max_velocity/100)
        self.conveyor_length = length_  # mm
        self.x_coordinate = None
        self.timer = 0
        self.item_count = 0
        self.items = dict()

    def setCam(self, x_coordinate=0):
        self.cam_coordinate = x_coordinate

    def start(self):
        count = 0
        while self.cam_coordinate < self.conveyor_length:
            self.cam_coordinate += 1
            self.timer += 1/self.default_speed
            count += self._checkBuffer(self.cam_coordinate)
        return {
                'time': self.timer,
                'count': count,
                }

    def _checkBuffer(self, coordinate):
        count = 0
        for item in self.buffer:
            if coordinate <= item[1]:
                break
            elif coordinate > item[1]:
                self.buffer.remove(item)
                count +=1
        return count

    def putBufferToConv(self, buffer):
        self.buffer = buffer
        return self.buffer

    def analytics(self, information):
        speed = information.get('count')/information.get('time')
        information['speed']= int(speed)
        return information


if __name__ == "__main__":
    part = bottle(diametr_=30)
    rr = part.bottle_set(2000)
    # print(rr)
    local_buffer = buffer(max_count_=100, range_= 1)
    Info = local_buffer.putToBuffer(rr)
    print(Info)
    full_buffer = local_buffer.getBuffer()
    # print(full_buffer)
    CONV = conveyor(velocity_proc_=20)
    CONV.setCam()
    CONV.putBufferToConv(full_buffer)
    stat = CONV.start()
    # print(stat)
    print(CONV.analytics(stat))