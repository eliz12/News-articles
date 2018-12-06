from save_articles import FoxNewsSite

directory = 'fox' 
main_url = 'https://www.foxnews.com'
fox = FoxNewsSite(main_url, directory)
fox.save_all()
