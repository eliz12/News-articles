from save_articles import  FoxNewsSite


directory = 'fox' 
main_url = 'https://www.foxnews.com/'
fox = FoxNewsSite(main_url, directory)

print 'please insert the phrase you are looking for'
words = raw_input()

f = open('search_result.txt', 'wb')
for i in fox.in_files(words):
    f.write(i + '\r\n')
f.close()