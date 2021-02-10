from selenium import webdriver
import json

class genres():
    def __init__(self):
        self.movies = []
        self.series = []
        self.games = []

        self.movies_genres = []
        self.series_genres = []
        self.games_genres = []

        self.firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def get(self, url):
        self.driver.get(url)

        _genres = self.driver.find_elements_by_class_name("article")
        for _ in range(0, 5, 1): _genres.pop(0)
        _genres.pop(2)
        for index, genre in enumerate(_genres):
            for value in genre.find_elements_by_tag_name("a"):
                if index == 0: self.movies_genres.append(value.text)
                if index == 1: self.series_genres.append(value.text)
                if index == 2: self.games_genres.append(value.text)

        self.driver.close()

    # TODO 
    # checkar se o filme tem so um ano ou nao, se so tiver 1 tirar o "- "
    
    def get_movies(self):
        __firefox_options = webdriver.FirefoxOptions()
        __driver = webdriver.Firefox(options=__firefox_options)
        __default_url = "https://www.imdb.com/search/title/?genres="
        for genre in self.movies_genres:
            __counter = 1
            #for _ in range(1, 6313, 1):
            for _ in range(1, 2, 1):
                try:
                    __driver.get(__default_url + str(genre).lower() + "&start=" + str(__counter))
                    movies = __driver.find_elements_by_xpath("//div[contains(@class, 'lister') and contains(@class, 'list')]")[0].find_elements_by_class_name("lister-item")
                    for movie in movies:
                        content = movie.find_elements_by_class_name("lister-item-content")[0]
                        header = content.find_elements_by_class_name("lister-item-header")[0]

                        try: movie_id = int(str(header.find_elements_by_tag_name("span")[0].text).replace(".", ""))
                        except: movie_id = -1

                        try: movie_title = str(header.find_elements_by_tag_name("a")[0].text)
                        except: movie_title = "Unknwon"

                        try: movie_year = str(header.find_elements_by_tag_name("span")[1].text)
                        except: movie_year = -1900
                        
                        try: movie_duration = content.find_elements_by_class_name("runtime")[0]
                        except: movie_duration = "Unknown"

                        try: movie_genres = str(movie.find_elements_by_class_name("genre")[0].text).split(",")
                        except: movie_genres = ["Unknown"]
                        
                        try: movie_rating = float(str(movie.find_elements_by_class_name("ratings-bar")[0].find_elements_by_tag_name("strong")[0].text).replace(",","."))
                        except: movie_rating = -1.0

                        try: movie_synposis = str(movie.find_elements_by_tag_name("p")[1].text)
                        except: movie_synposis = "There's no synposis for this movie"

                        try:
                            aux = content.find_elements_by_tag_name("p")
                            aux.pop(0)
                            aux.pop(0)
                            try: aux.pop(1)
                            except: pass
                            aux = str(aux[0].text)

                            if aux.count(":") >= 2: movie_directors = aux.split(":")[0].split(",")
                            else: movie_directors = ["Unknown"]

                            try: movie_stars = aux.split(":")[1].split(",")
                            except: movie_stars = ["Unknown"]
                        except:
                            movie_directors = ["Unknown"]
                            movie_stars = ["Unknown"]

                        movie_dic = {
                                        "id": movie_id,
                                        "title": movie_title,
                                        "year": movie_year,
                                        "duration": movie_duration,
                                        "genres": movie_genres,
                                        "rating": movie_rating,
                                        "synposis": movie_synposis,
                                        "directos": movie_directors,
                                        "stars": movie_stars
                                    }     

                        self.movies.append(movie_dic)
                except:
                    pass
                __counter += 50 

            with open("imdb.json", "w", encoding="utf-8") as f:
                json.dump({"movies": self.movies}, f, indent=4)

if __name__ == "__main__":
    genres = genres()
    genres.get("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")
    genres.get_movies()