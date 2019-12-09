
def search_num(num):
    if num[0].isdigit():
        return num[0]+search_num(num[1:])
    else:
        return ""


def buildMappingFrom(filename, MAC_mapping): #Predetermined MAC Addresses and assigned index
    file = open(filename, 'r')
        
    for line in file:
        assignedIndx = search_num(line)
        mac_idx = line.find(',') + 1
        MAC_mapping[assignedIndx] = line[mac_idx:mac_idx+17]
        
    file.close()
        
        
def buildSeatingMapFrom(filename, MAC_mapping, Seating): #From google form
    file = open(filename, 'r')
    #Seat Number, MAC address mapping
    for line in file:
        seat_num = search_num(line)
        indxOfMACIndx = (line.find(',')+1)
        Seating[MAC_mapping[line[indxOfMACIndx]]] = seat_num
        
    file.close()
    



