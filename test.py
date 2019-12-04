import parse
import subprocess
import re

result = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)
result = str (result.stdout)
result = re.search('BD Address:(.*)ACL', result)
result = result.group(1)
result = result.strip()
#print(result)

seat = {}


parse.parse_seating("bluetooth-info.txt", "pi-info.txt", seat)


#print(seat)


print("I am in seat no."+seat[result])
