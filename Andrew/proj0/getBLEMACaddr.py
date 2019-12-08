import subprocess
import re

result = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)
result = str (result.stdout)
result = re.search('BD Address:(.*)ACL', result)
result = result.group(1)
result = result.strip()
print(result)
