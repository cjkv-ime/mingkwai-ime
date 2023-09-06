from requests import get
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, NavigableString

with open('char.csv','w') as f, open('img.csv', 'w') as F, open('listSyllable') as ㄈ:
    ls = ㄈ.readlines()
    for syl in tqdm(ls):
        print()
        w = get('https://humanum.arts.cuhk.edu.hk/Lexis/Lindict/syllabary/'+syl.strip()+'.htm').text
        soup = bs(w, 'html.parser')
        for i in soup.find_all('a'):
            l, c = i.get('href'), i.contents[0]
            if l.find('/Lexis/Lindict/Lindict.php?query=') == -1:
                continue
            if l.find('wholerecord',l.find('=')) == -1:
                continue
            if type(c) == Tag:
                s=c.get('src')
                F.write( l[l.find('=')+1 : l.find('&')] + ',' + s + '\n')
                continue
            try:
                f.write(l[l.find('=')+1:l.find('&')] + ',' + c.encode('iso-8859-1').decode('big5') + '\n')
            except UnicodeDecodeError:
                F.write(l[l.find('=')+1:l.find('&')] + ',' + repr(c.encode('iso-8859-1')) +' (raw)\n')
            
