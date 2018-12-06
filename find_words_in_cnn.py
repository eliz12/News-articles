from save_articles import  CnnSite


directory = 'cnn' 
main_url = 'https://edition.cnn.com/'
cnn = CnnSite(main_url, directory)

print 'please insert the phrase you are looking for'
words = raw_input()

f = open('search_result.txt', 'wb')
for i in cnn.in_files(words):
    f.write(i + '\r\n')
f.close()