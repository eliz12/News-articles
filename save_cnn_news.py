from save_articles import CnnSite

directory = 'cnn' 
main_url = 'https://edition.cnn.com'
cnn = CnnSite(main_url, directory)
cnn.save_all()
