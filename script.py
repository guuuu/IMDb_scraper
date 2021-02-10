from selenium import webdriver
import json

class genres():
    def __init__(self):
        self.movies = []
        self.series = []
        self.games = []

        self.movie = {
            "title": None,            
            "year": None,            
            "duration": None,            
            "genres": [],            
            "rating": 0.0,            
            "synposis": None,            
            "directos": [], 
            "stars": []
        }
        self.serie = {}
        self.game = {}

        self.movies_genres = []
        self.series_genres = []
        self.games_genres = []

        self.firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def get(self, url):
        self.driver.get(url)

        genres = self.driver.find_elements_by_class_name("article")
        for _ in range(0, 5, 1): genres.pop(0)
        genres.pop(2)
        for index, genre in enumerate(genres):
            for value in genre.find_elements_by_tag_name("a"):
                if index == 0: self.movies_genres.append(value.text)
                if index == 1: self.series_genres.append(value.text)
                if index == 2: self.games_genres.append(value.text)
        self.driver.close()


if __name__ == "__main__":
    genres().get("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")