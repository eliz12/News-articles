import urllib2
import os.path
from bs4 import BeautifulSoup as BS
from selenium import webdriver


class Site(object):
    
    def __init__(self, main_url, directory):
        self.main_url = main_url
        self.cache = Cache(directory)

    def save_html(self, url):
        """
        This function save the article if the
        article is not already saved.
		The url of the article will also be saved
		
		Args:
			url (str): The relevant link
        """
        full_url = self.get_full_url(url)
        if full_url in self.cache.dic:
            print 'already saved', full_url
            return
        try:
            data = self.get_data(full_url)
            completeName = os.path.join(self.cache.directory, str(self.cache.num_of_art) +".txt")         
            f =  open(completeName, "wb")
            f.write(full_url + '\r\n')
            f.write(data)
            f.close()
            self.cache.save_in_cache(full_url)
            print 'successfully saved', full_url
        except Exception as ex:
            print full_url
            print ex

    def get_data(self, url):
        raise NotImplementedError()
    
    def save_all(self):
        raise NotImplementedError()


    def get_full_url(self, url):
        """
        This function gets url, and fixes it if needed.
        """
        if "://" in url:
            full_url = str(url)
        elif url.startswith("//"):
            full_url = "https:" + url
        else:
            full_url = self.main_url + url
        return full_url


    def in_files(self, listwords):
        """
        This function checks if a specific word or a sentence
        is in a specific file.
        """
        
        listwords = listwords.lower().split()
        for file_name in os.listdir(self.cache.directory):
            print file_name
            if file_name != 'cache.txt':
                f = open(os.path.join(self.cache.directory, file_name))
                read = f.readlines()
                f.close()
                
                read = str(read).lower().split()
                i = 0
                while i < len(read) - len(listwords):
                    if read[i:i + len(listwords)] == listwords:
                        yield file_name
                        break
                    i += 1     


class FoxNewsSite(Site):

    def __init__(self, main_url, directory):
        super(FoxNewsSite, self).__init__(main_url, directory)
        print self.main_url
    
        
    def save_all(self):
        """
        This function save all the articles of the main site
        The function calls to the function save_html
        """
        res = urllib2.urlopen(self.main_url)
        soup = BS(res.read(), "html.parser")
        contents = soup.findAll("h2")
        for content in contents:
            self.save_html(content.a["href"])
    

    def get_data(self, url):
        """
        This function gets the relevant data for saving
		Args:
			url (str): The relevant link
		Returns:
			data (str): the relevant data for saving
		
		"""
        res = urllib2.urlopen(url)
        soup = BS(res, 'html.parser')
        body = soup.body
        text =''
        for paragraph in body.findAll('p'):
            text += paragraph.text.encode('utf8')
        return text

class CnnSite(Site):
    def __init__(self, main_url, directory):
        super(CnnSite, self).__init__(main_url, directory)
        print self.main_url
    
        
    def save_all(self):
        """
        This function save all the articles of the main site
        The function calls to the function save_html
        """
        browser = webdriver.Firefox()
        browser.get(self.main_url)
        html = browser.page_source
        browser.close()
        soup = BS(html, "html.parser")
        contents = soup.findAll("h3")
        for content in contents:
            try:
                self.save_html(content.a["href"])
            except Exception as e:
                print e

    def get_data(self, url):
        res = urllib2.urlopen(url)
        soup = BS(res, 'html.parser')
        body = soup.body
        text =''

        for paragraph in body.findAll('p', class_ = 'zn-body__paragraph speakable'):
            text += paragraph.text.encode('utf8')
        for div in soup.findAll('div', class_ = 'zn-body__paragraph'):
            text += div.text.encode('utf8')
        for div in soup.findAll('div', class_ = 'Paragraph__component'):
            text += div.text.encode('utf8')
        return text    


class Cache(object):
    """
	In the Cache class there is the dictionary of
	the url and the names of the files.
	"""
    
    def __init__(self, directory):
        self.directory = directory
        self.dic = {}
        self.num_of_art = 1
        if not os.path.exists(directory):
             os.makedirs(directory)
        try:
            f = open(os.path.join(self.directory, 'cache.txt'))
            for line in f:
                self.dic[line.split(',')[0]] = line.split(',')[1]
                self.num_of_art += 1
            f.close()
        except:
            f = open(os.path.join(self.directory, 'cache.txt'), 'wb')
            f.close()

    
    def save_in_cache(self, url):
        """
        This function save in the dictionary urls that already been saved.
        """
        f = open(os.path.join(self.directory, 'cache.txt'), 'ab')
        f.write(url + ',' + str(self.num_of_art) + '\r\n')
        f.close()
        self.dic[url] = self.num_of_art
        self.num_of_art += 1






