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


def is_multiple_terms(module):

    if module.find("春") + module.find("秋") != -2:
        return True

    else:
        return False


def main():

    class_list = create_class_list()
    print(len(class_list))

    for c in class_list:
        class_id = c.class_id
        name = c.name
        module = c.module
        period = c.period
        room = c.room
        description = c.description

        module_tmp = module.split()
        period_tmp = period.split()

        module_list = []
        period_list = []

        module_len = len(module_tmp)
        period_len = len(period_tmp)

        if module_len == period_len:

            for i in range(module_len):

                if is_multiple_terms(module_tmp[i]):
                    split_index = module.find("秋")
                    module_list.append(module_tmp[i][0:split_index])
                    module_list.append(module_tmp[i][split_index:])
                    period_list.append(period_tmp[i])
                    period_list.append(period_tmp[i])

                else:
                    module_list.append(module_tmp[i])
                    period_list.append(period_tmp[i])

            assert len(module_list) == len(period_list)
        
        # In this case, period_len equals 1
        elif module_len > period_len:

            for i in range(module_len):
                
                if is_multiple_terms(module_tmp[i]):
                    split_index = module.find("秋")
                    module_list.append(module_tmp[i][0:split_index])
                    module_list.append(module_tmp[i][split_index:])
                    period_list.append(period_tmp[0])
                    period_list.append(period_tmp[0])

                else:
                    module_list.append(module_tmp[i])
                    period_list.append(period_tmp[0])

            assert len(module_list) == len(period_list)

        elif module_len == 1:
            for i in range(period_len):
                module_list.append(module_tmp[0])
                period_list.append(period_tmp[i])

            assert len(module_list) == len(period_list)
            
        else:
            print("{}:{}:{}".format(name,module_tmp,period_tmp))



            




if __name__ == "__main__":
    main()
