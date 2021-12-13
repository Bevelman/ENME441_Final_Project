#!/usr/bin/python37all

import cgi, json

data = cgi.FieldStorage()         

# set up new data from POST:
slider_val1 = data.getvalue('slider1')
slider_val2 = data.getvalue('slider2')
if data.getvalue('launch')=='Launch!':
  launched = 1
else:
  launched = 0

# form new dictionary with user data:
fileData = {'slider1':slider_val1, 'slider2':slider_val2, 'launch':launched}

# write all data to the file:
with open('shooter.txt', 'w') as f:
  json.dump(fileData,f)

# generate new web page:
print("Content-type: text/html\n\n")
print('<html>')
print('<body>')
print('<input type="range" name="slider1" min ="3" max="12" value ="%s"><br>' % slider_val1)
print('<input type="range" name="slider2" min ="3" max="12" value ="%s"><br>' % slider_val2)
print('<input type="submit" name="angle" value="Set angle">')
print('<input type="submit name="launch" value="Launch!">')
print('</form>')
print('</body>')
print('</html>')