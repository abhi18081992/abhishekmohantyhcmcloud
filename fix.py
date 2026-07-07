import xml.etree.ElementTree as ET, re, os, html as h 
tree = ET.parse(r'C:\Users\mohan\Downloads\blogpost.xml') 
root = tree.getroot() 
ns = '{http://www.w3.org/2005/Atom}' 
bl = '{http://schemas.google.com/blogger/2008}' 
entries = root.findall(f'{ns}entry') 
print(f'Total entries: {len(entries)}') 
kinds = [e.find(f'{bl}type') for e in entries] 
[print(k.text if k is not None else 'NO-KIND') for k in kinds[:5]] 
