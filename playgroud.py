import hashlib
token = 'c5b1ee79137880cbbfe6d65f406f9a31'
v = '1590911637192'
x = '12574478'

data = '{"broadcasterId":"1759494485","start":0,"limit":10}'
aR = token + "&" + v + "&" + x + "&" + '{}'.format(data)
sign = hashlib.md5(aR.encode()).hexdigest()

print(sign)
