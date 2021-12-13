#!/usr/bin/python37all
import cgi, json

data = cgi.FieldStorage()         

# set up new data from POST:
slider_val1 = data.getvalue('slider1')
slider_val2 = data.getvalue('slider2')

# form new dictionary with user data:
fileData = {'slider1':slider_val1, 'slider2':slider_val2}

# write all data to the file:
with open('shooter.txt', 'w') as f:
  json.dump(fileData,f)

# generate new web page:
print("Content-type: text/html\n\n")
print('<html>')
print('<body>')
print("s1 = " + data.getvalue('slider1') + '<br>')
print("s2 = " + data.getvalue('slider2') + '<br>')
print('<input type="submit" value="Submit">')
print('</form>')
print('</body>')
print('</html>')