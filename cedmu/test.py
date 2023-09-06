from requests.exceptions import Timeout
from requests import get
from tqdm import tqdm

with open('big5-freq-lfreq.csv','r') as f:
    global l
    l = dict(tuple(line.strip().split(',')) for line in f)

with open('MingKwaiCode.txt', 'a') as f, open('MingKwaiCode.log', 'a') as log, open('char.csv') as chars:
    for line in tqdm(chars):
        i, char = line.strip().split(',')
        j, k = i[1:3], i[4:]
        try:
            assert char == eval("b'\\x{0}\\x{1}'".format(j, k)).decode('big5')
        except UnicodeDecodeError:
            log.write(j+k+',,'+'NotABig5Character')
            continue
        except AssertionError:
            log.write(j+k+','+char+','+'Big5DecoderNotMatch')
            continue

        print('')
        
        try:
            htm = get('https://humanum.arts.cuhk.edu.hk/Lexis/Lindict/Lindict.php?query=%{0}%{1}&category=wholerecord'.format(j,k), timeout=1).text
            with open('./htm/{0}{1}.htm', 'w') as w:
                w.write(htm)
            if char not in l:
                pass # write the code to search for the mingkwai encodings
            
        except Timeout:
            log.write(hex(i)[2:]+','+char+','+'TimedOut\n')
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            log.write(hex(i)[2:]+','+char+','+'UnknownError')
        
