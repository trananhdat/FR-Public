import re, uuid
# after each 2 digits, join elements of getnode().
# using regex expression
print (':'.join(re.findall('..', '%012x' % uuid.getnode())))

from getmac import get_mac_address as gma 

print(gma())