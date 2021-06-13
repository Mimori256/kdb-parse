#Convert CSV to JSON for twinc
class Class():

    def __init__(self, class_id, name, module, period, room, description):
        self.class_id = class_id
        self.name = name
        self.module = module
        self.period = period
        self.room = room
        self.description = description

    
    """def remove_special_module(self):

        remove_list = [" 夏季休業中", " 春季休業中"]
        for s in remove_list:
            self.module.replace(s, "")
        
        return self.module"""

    def separate_module(self):


def create_class_list():

    with open("kdb.csv", "r", encoding="utf_8") as f:
        class_list = []
        lines = f.readlines()

      # Remove the header
        lines.pop(0)

        for line in lines:
          tmp = line.split('"')
          class_id = tmp[1]
          name = tmp[3]
          module = tmp[11]
          period = tmp[13]
          room = tmp[15]
          description = tmp[21]

          if room == "":
              room = " " 
        
          # Remove classes that are not opened in this year
          if not "" in set([class_id, name, module, period, room, description]):
              class_list.append(Class(class_id, name, module, period, room, description))

        return class_list


def main():

    class_list = create_class_list()
    print(len(class_list))

    for c in class_list:
        class_id = c.class_id
        name = c.name
        module = c.separate_module()
        period = c.period
        room = c.room
        description = c.description




if __name__ == "__main__":
    main()
