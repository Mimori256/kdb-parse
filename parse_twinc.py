import sys

#Convert CSV to JSON for twinc

class Class():

    def __init__(self, class_id, name, module, period, room, description):
        self.class_id = class_id
        self.name = name
        self.module = module
        self.period = period
        self.room = room
        self.description = description

    
# Global consts
global WEEKDAY_LIST 
WEEKDAY_LIST =  ["月","火","水","木","金","土"]


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

    if module.find("春") != -1 and module.find("秋") != -1:
        return True

    else:
        return False


def days_count(period):

    count = 0

    for s in period:
        if s in WEEKDAY_LIST :
            count += 1

    return count
    

def remove_special_module(module):

    remove_list = [" 夏季休業中", " 春季休業中", "夏季休業中", "春季休業中", "通年"]

    for s in remove_list:
           module = module.replace(s, "")
           module = module.replace("春学期","春ABC")
           module = module.replace("秋学期","秋ABC")
       
    return module


def remove_special_period(period):

    remove_list = ["集中", "応談", "随時", ",集中", ",応談", ",随時"]

    for s in remove_list:
        period = period.replace(s, "")
    return period


def get_separate_index(period):
    
    separate_index_list = []

    for i in range(len(period)):
        if period[i] in WEEKDAY_LIST:
            separate_index_list.append(i)

    separate_index_list.pop(0)
    return separate_index_list


def get_num_index(period):

    count = 0

    for i in range(len(period)):
        flag = False
        try:
            tmp = int(period[i])
            return count
            
        except ValueError:
            count += 1
        

def apply_num_info(period, num_info):

    period = list(period)

    #Ex: 月・火1
    if "・" in period:
        period = [s.replace("・", num_info + ",") for s in period]

    else:

        for i in range(len(period)):
            if period[i] in WEEKDAY_LIST:
                period[i] += num_info

    return "".join(period)



def is_split_period(period):

    splited_period = period.split(",")
    for e in splited_period:
        try:
            tmp = int(e)
            return False
        except ValueError:
            pass
    return True


def is_blank_list(l):

    l = list(filter(lambda x: x != "", l))
    return l == []


def is_int(n):
    try:
        int(n)
        return True
    
    except ValueError:
        return False


def count_num_info(period):
    count = 0
    for i in range (len(period) -1):
        if period[i] == "," and period[i+1] in WEEKDAY_LIST:
            count += 1
    return count + 1
            

def split_period(period):
    
    period = list(period)

    for i in range(len(period) - 1):
        if period[i] == "," and period[i+1] in WEEKDAY_LIST:
            period[i] = "."

    return "".join(period).split(".")


def main():

    module_list = []
    period_list = []
    class_list = create_class_list()
    class_len = len(class_list)
    # module_period_list: [module_list, period_list]
    module_period_list = []

    for c in class_list:
        class_id = c.class_id
        name = c.name
        module = c.module
        period = c.period
        room = c.room
        description = c.description


        module_tmp = module.split(" ")
        period_tmp = period.split(" ")



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

        
        # In this case, period_len equals 1 e.g, 春C秋A:火2,3
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


        elif module_len == 1:
            for i in range(period_len):
                module_list.append(module_tmp[0])
                period_list.append(period_tmp[i])

            
        else:
            description = "error"

        #The length of module_list and period_list should be the same
        assert len(module_list) == len(period_list)

        # Remove special modules
        module_list = list(map(remove_special_module, module_list))
        period_list = list(map(remove_special_period, period_list))

    for i in range(class_len):
        if  module_list[i] == "" or period_list[i] == "":
            continue

        else:
            module_period_list.append([module_list[i], period_list[i]])

    # Parse periods 
    # Sunday classes are not available for now since there is no Sunday class in this year
    # The lenths of module_list and period_list are the same


    tmp2=[]

    #Reset period_list
    #period_list = []
    #print(period_list)

    for module_period in module_period_list :
        period = module_period[1]

        if is_blank_list(period):
            continue

        #splited_period = period.split(",")
        tmp1 = []

        if days_count(period) == 1:
            tmp1.append(period)

        elif days_count(period) == count_num_info(period):
            splited_period = split_period(period)
            tmp1.append(splited_period)
            
        else:

            splited_period = split_period(period) 
            for element in splited_period:

                if days_count(element) > 1:

                    num_index = get_num_index(element)
                    num_info = element[num_index:]
                    new_element = apply_num_info(element, num_info).split(",")

                    for p in new_element:
                        tmp1.append(p)
            
                else:
                    tmp1.append(element)
            
            print(tmp1)

    



    sys.exit()


if __name__ == "__main__":
    main()
