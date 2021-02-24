import re
import os
import json
import time
import unidecode
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class imdb():
    def __init__(self):
        self.movies = []
        self.series = []
        self.games = []

        self.movies_genres = []
        self.series_genres = []
        self.games_genres = []

        self.final = []

        self.movie_thread = None
        self.series_thread = None
        self.games_thread = None

        self.firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def start(self, url):
        print("Getting basic info")
        self.driver.get(url)
        self.driver.minimize_window()

        _genres = self.driver.find_elements_by_class_name("article")
        for _ in range(0, 5, 1): _genres.pop(0)
        _genres.pop(2)
        for index, genre in enumerate(_genres):
            for value in genre.find_elements_by_tag_name("a"):
                if index == 0: self.movies_genres.append(value.text)
                if index == 1: self.series_genres.append(value.text)
                if index == 2: self.games_genres.append(value.text)

        self.driver.close()
        print("Done")

    def get_movies(self):
        print("Starting to gather movies informations...")
        __firefox_options = webdriver.FirefoxOptions()
        __driver = webdriver.Firefox(options=__firefox_options)
        __default_url = "https://www.imdb.com/search/title/?genres="
        __default_url2 = "&title_type=feature"
        for index, genre in enumerate(self.movies_genres):
            try:
                print(f"Now in genre {genre} | {index} - {len(self.movies_genres)}")
                __driver.get(__default_url + str(genre).lower() + __default_url2)
                __driver.minimize_window()
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'main'))
                    WebDriverWait(__driver, 10).until(element_present)
                except:
                    pass
                try:
                    qtd = int(str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text).split(" ")[2:-1]).replace(",","").replace("['", "").replace("']", "")) // 50
                except:
                    qtd = re.findall(r"\d+", str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text)))
                    if len(qtd) >= 2: qtd = int(qtd[1])
                    else: qtd = int(qtd[0])
                    qtd = qtd if qtd >= 50 else 1            
                __counter = 1
                #for i in range(1, qtd, 1):
                for i in range(1, 3, 1):
                    try:
                        print(f"Page {i} of {qtd} - movies")
                        __driver.get(__default_url + str(genre).lower() + __default_url2 + "&start=" + str(__counter))
                        movies = __driver.find_elements_by_xpath("//div[contains(@class, 'lister') and contains(@class, 'list')]")[0].find_elements_by_class_name("lister-item")
                        for movie in movies:
                            content = movie.find_elements_by_class_name("lister-item-content")[0]
                            header = content.find_elements_by_class_name("lister-item-header")[0]
                            #print("Step 1 of 13 - concluded")

                            try: movie_id = int(str(header.find_elements_by_tag_name("span")[0].text).replace(".", ""))
                            except: movie_id = -1
                            #print("Step 2 of 13 - concluded")

                            try: movie_title = unidecode.unidecode(str(header.find_elements_by_tag_name("a")[0].text))
                            except: movie_title = "Unknwon"
                            #print("Step 3 of 13 - concluded")

                            try: movie_year = unidecode.unidecode(str(header.find_elements_by_tag_name("span")[1].text))
                            except: movie_year = -1900
                            #print("Step 4 of 13 - concluded")
                            
                            try: movie_duration = unidecode.unidecode(str(content.find_elements_by_class_name("runtime")[0].text))
                            except: movie_duration = "Unknown"
                            #print("Step 5 of 13 - concluded")

                            try: movie_genres = unidecode.unidecode(str(movie.find_elements_by_class_name("genre")[0].text)).split(",")
                            except: movie_genres = ["Unknown"]
                            #print("Step 6 of 13 - concluded")
                            
                            try: movie_rating = float(str(movie.find_elements_by_class_name("ratings-bar")[0].find_elements_by_tag_name("strong")[0].text).replace(",","."))
                            except: movie_rating = -1.0
                            #print("Step 7 of 13 - concluded")

                            try: movie_synopsis = unidecode.unidecode(str(movie.find_elements_by_tag_name("p")[1].text))
                            except: movie_synopsis = "There's no synopsis for this movie"
                            #print("Step 8 of 13 - concluded")

                            try:
                                aux = content.find_elements_by_tag_name("p")
                                aux.pop(0)
                                aux.pop(0)
                                try: aux.pop(1)
                                except: pass
                                aux = str(aux[0].text)
                                #print("Step 9 of 13 - concluded")

                                if aux.count(":") >= 2: movie_directors = unidecode.unidecode(aux).split(":")[1].split("Stars")[0].split(",")
                                else: movie_directors = ["Unknown"]
                                #print("Step 10 of 13 - concluded")

                                try: movie_stars = unidecode.unidecode(aux).split(":")[1].split(",")
                                except: movie_stars = ["Unknown"]
                                #print("Step 11 of 13 - concluded")
                            except:
                                movie_directors = ["Unknown"]
                                movie_stars = ["Unknown"]
                                #print("Step 11.1 of 13 - concluded")

                            for i in range(len(movie_directors)): movie_directors[i].replace("|", "") 
                            for i in range(len(movie_stars)): movie_stars[i].replace("|", "") 

                            movie_title.strip()
                            movie_duration.strip()
                            map(str.strip, movie_genres)
                            movie_synopsis.strip()
                            map(str.strip, movie_directors)
                            map(str.strip, movie_stars)

                            movie_dic = {
                                            "id": movie_id,
                                            "title": movie_title,
                                            "year": movie_year,
                                            "duration": movie_duration,
                                            "genres": movie_genres,
                                            "rating": movie_rating,
                                            "synopsis": movie_synopsis,
                                            "directors": movie_directors,
                                            "stars": movie_stars
                                        }     
                            #print("Step 12 of 13 - concluded")
                            self.movies.append(movie_dic)
                            #print("Step 13 of 13 - concluded")
                        with open(f"movies.json", "w", encoding="utf-8") as f: json.dump(self.movies, f, indent=4)
                    except:
                        pass
                    __counter += 50 
            except Exception as ex:
                pass
        #self.final.append({"movies": self.movies})
        __driver.close()

    def get_series(self):
        print("Starting to gather series informations...")
        __firefox_options = webdriver.FirefoxOptions()
        __driver = webdriver.Firefox(options=__firefox_options)
        __default_url = "https://www.imdb.com/search/title/?genres="
        __default_url2 = "&title_type=tv_series,mini_series"
        for index, genre in enumerate(self.series_genres):
            try:
                print(f"Now in genre {genre} | {index} - {len(self.series_genres)}")
                __driver.get(__default_url + str(genre).lower() + __default_url2)
                __driver.minimize_window()
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'main'))
                    WebDriverWait(__driver, 10).until(element_present)
                except:
                    pass
                try:
                    qtd = int(str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text).split(" ")[2:-1]).replace(",","").replace("['", "").replace("']", "")) // 50
                except:
                    qtd = re.findall(r"\d+", str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text)))
                    if len(qtd) >= 2: qtd = int(qtd[1])
                    else: qtd = int(qtd[0])
                    qtd = qtd if qtd >= 50 else 1            
                __counter = 1
                #for i in range(1, qtd, 1):
                for i in range(1, 3, 1):
                    try:
                        print(f"Page {i} of {qtd} - series")
                        __driver.get(__default_url + str(genre).lower() + __default_url2 + "&start=" + str(__counter))
                        series = __driver.find_elements_by_xpath("//div[contains(@class, 'lister') and contains(@class, 'list')]")[0].find_elements_by_class_name("lister-item")
                        for serie in series:
                            content = serie.find_elements_by_class_name("lister-item-content")[0]
                            header = content.find_elements_by_class_name("lister-item-header")[0]
                            #print("Step 1 of 13 - concluded")

                            try: serie_id = int(str(header.find_elements_by_tag_name("span")[0].text).replace(".", ""))
                            except: serie_id = -1
                            #print("Step 2 of 13 - concluded")

                            try: serie_title = unidecode.unidecode(str(header.find_elements_by_tag_name("a")[0].text))
                            except: serie_title = "Unknwon"
                            #print("Step 3 of 13 - concluded")

                            try: serie_year = unidecode.unidecode(str(header.find_elements_by_tag_name("span")[1].text))
                            except: serie_year = -1900
                            #print("Step 4 of 13 - concluded")
                            
                            try: serie_duration = unidecode.unidecode(str(content.find_elements_by_class_name("runtime")[0].text))
                            except: serie_duration = "Unknown"
                            #print("Step 5 of 13 - concluded")

                            try: serie_genres = unidecode.unidecode(str(serie.find_elements_by_class_name("genre")[0].text)).split(",")
                            except: serie_genres = ["Unknown"]
                            #print("Step 6 of 13 - concluded")
                            
                            try: serie_rating = float(str(serie.find_elements_by_class_name("ratings-bar")[0].find_elements_by_tag_name("strong")[0].text).replace(",","."))
                            except: serie_rating = -1.0
                            #print("Step 7 of 13 - concluded")

                            try: serie_synopsis = unidecode.unidecode(str(serie.find_elements_by_tag_name("p")[1].text))
                            except: serie_synopsis = "There's no synopsis for this serie"
                            #print("Step 8 of 13 - concluded")

                            try:
                                aux = content.find_elements_by_tag_name("p")
                                aux.pop(0)
                                aux.pop(0)
                                try: aux.pop(1)
                                except: pass
                                aux = str(aux[0].text)
                                #print("Step 9 of 13 - concluded")

                                if aux.count(":") >= 2: serie_directors = unidecode.unidecode(aux).split(":")[1].split("Stars")[0].split(",")
                                else: serie_directors = ["Unknown"]
                                #print("Step 10 of 13 - concluded")

                                try: serie_stars = unidecode.unidecode(aux).split(":")[1].split(",")
                                except: serie_stars = ["Unknown"]
                                #print("Step 11 of 13 - concluded")
                            except:
                                serie_directors = ["Unknown"]
                                serie_stars = ["Unknown"]
                                #print("Step 11.1 of 13 - concluded")

                            for i in range(len(serie_directors)): serie_directors[i].replace("|", "") 
                            for i in range(len(serie_stars)): serie_stars[i].replace("|", "") 

                            serie_title.strip()
                            serie_duration.strip()
                            map(str.strip, serie_genres)
                            serie_synopsis.strip()
                            map(str.strip, serie_directors)
                            map(str.strip, serie_stars)

                            serie_dic = {
                                            "id": serie_id,
                                            "title": serie_title,
                                            "year": serie_year,
                                            "duration": serie_duration,
                                            "genres": serie_genres,
                                            "rating": serie_rating,
                                            "synopsis": serie_synopsis,
                                            "directors": serie_directors,
                                            "stars": serie_stars
                                        }     
                            #print("Step 12 of 13 - concluded")
                            self.series.append(serie_dic)
                            #print("Step 13 of 13 - concluded")

                        with open("series.json", "w", encoding="utf-8") as f: json.dump(self.series, f, indent=4)                
                    except:
                        pass
                    __counter += 50 
            except Exception as ex:
                pass
        __driver.close()
        #self.final.append({"series": self.series})

    def get_games(self):
        print("Starting to gather games informations...")
        __firefox_options = webdriver.FirefoxOptions()
        __driver = webdriver.Firefox(options=__firefox_options)
        __default_url = "https://www.imdb.com/search/title/?genres="
        __default_url2 = "&title_type=video_game"
        for index, genre in enumerate(self.games_genres):
            try:
                print(f"Now in genre {genre} | {index} - {len(self.games_genres)}")
                __driver.get(__default_url + str(genre).lower() + __default_url2)
                __driver.minimize_window()
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'main'))
                    WebDriverWait(__driver, 10).until(element_present)
                except:
                    pass

                try:
                    qtd = int(str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text).split(" ")[2:-1]).replace(",","").replace("['", "").replace("']", "")) // 50
                except:
                    qtd = re.findall(r"\d+", str(str(__driver.find_element_by_id("main").find_elements_by_class_name("desc")[0].find_elements_by_tag_name("span")[0].text)))
                    if len(qtd) >= 2: qtd = int(qtd[1])
                    else: qtd = int(qtd[0])
                    qtd = qtd if qtd >= 50 else 1

                __counter = 1
                #for i in range(1, qtd, 1):
                for i in range(1, 3, 1):
                    try:
                        print(f"Page {i} of {qtd} - games")
                        __driver.get(__default_url + str(genre).lower() + __default_url2 + "&start=" + str(__counter))
                        games = __driver.find_elements_by_xpath("//div[contains(@class, 'lister') and contains(@class, 'list')]")[0].find_elements_by_class_name("lister-item")
                        for game in games:
                            content = game.find_elements_by_class_name("lister-item-content")[0]
                            header = content.find_elements_by_class_name("lister-item-header")[0]
                            #print("Step 1 of 13 - concluded")

                            try: game_id = int(str(header.find_elements_by_tag_name("span")[0].text).replace(".", ""))
                            except: game_id = -1
                            #print("Step 2 of 13 - concluded")

                            try: game_title = unidecode.unidecode(str(header.find_elements_by_tag_name("a")[0].text))
                            except: game_title = "Unknwon"
                            #print("Step 3 of 13 - concluded")

                            try: game_year = unidecode.unidecode(str(header.find_elements_by_tag_name("span")[1].text))
                            except: game_year = -1900
                            #print("Step 4 of 13 - concluded")
                            
                            try: game_duration = unidecode.unidecode(str(content.find_elements_by_class_name("runtime")[0].text))
                            except: game_duration = "Unknown"
                            #print("Step 5 of 13 - concluded")

                            try: game_genres = unidecode.unidecode(str(game.find_elements_by_class_name("genre")[0].text)).split(",")
                            except: game_genres = ["Unknown"]
                            #print("Step 6 of 13 - concluded")
                            
                            try: game_rating = float(str(game.find_elements_by_class_name("ratings-bar")[0].find_elements_by_tag_name("strong")[0].text).replace(",","."))
                            except: game_rating = -1.0
                            #print("Step 7 of 13 - concluded")

                            try: game_synopsis = unidecode.unidecode(str(game.find_elements_by_tag_name("p")[1].text))
                            except: game_synopsis = "There's no synopsis for this game"
                            #print("Step 8 of 13 - concluded")

                            try:
                                aux = content.find_elements_by_tag_name("p")
                                aux.pop(0)
                                aux.pop(0)
                                try: aux.pop(1)
                                except: pass
                                aux = str(aux[0].text)
                                #print("Step 9 of 13 - concluded")

                                if aux.count(":") >= 2: game_directors = unidecode.unidecode(aux).split(":")[1].split("Stars")[0].split(",")
                                else: game_directors = ["Unknown"]
                                #print("Step 10 of 13 - concluded")

                                try: game_stars = unidecode.unidecode(aux).split(":")[1].split(",")
                                except: game_stars = ["Unknown"]
                                #print("Step 11 of 13 - concluded")
                            except:
                                game_directors = ["Unknown"]
                                game_stars = ["Unknown"]
                                #print("Step 11.1 of 13 - concluded")

                            for i in range(len(game_directors)): game_directors[i].replace("|", "") 
                            for i in range(len(game_stars)): game_stars[i].replace("|", "") 

                            game_title.strip()
                            game_duration.strip()
                            map(str.strip, game_genres)
                            game_synopsis.strip()
                            map(str.strip, game_directors)
                            map(str.strip, game_stars)

                            game_dic = {
                                            "id": game_id,
                                            "title": game_title,
                                            "year": game_year,
                                            "duration": game_duration,
                                            "genres": game_genres,
                                            "rating": game_rating,
                                            "synopsis": game_synopsis,
                                            "directors": game_directors,
                                            "stars": game_stars
                                        }     
                            #print("Step 12 of 13 - concluded")
                            self.games.append(game_dic)
                            #print("Step 13 of 13 - concluded")

                        with open("games.json", "w", encoding="utf-8") as f: json.dump(self.games, f, indent=4)                          
                    except:
                        pass
                    __counter += 50 
            except Exception as ex:
                pass
        __driver.close()
        #self.final.append({"games": self.games})

    def merge_files(self):
        self.movies.clear()
        self.series.clear()
        self.games.clear()
        print("Merging files")
        with open("movies.json", "r", encoding="utf-8") as f: self.movies = json.loads(f.read())
        print("Movies info loaded")
        with open("series.json", "r", encoding="utf-8") as f: self.series = json.loads(f.read())
        print("Series info loaded")
        with open("games.json", "r", encoding="utf-8") as f: self.games = json.loads(f.read())
        print("Games info loaded")
        self.final.append({"movies": self.movies})
        self.final.append({"series": self.series})
        self.final.append({"games": self.games})
        with open("imdb.json", "w", encoding="utf-8") as f: json.dump(self.final, f, indent=4)
        print("Finished")
        os.remove("movies.json")
        os.remove("series.json")
        os.remove("games.json")

    def check_threads(self):
        while True:
            time.sleep(30)
            print(f"Movies thread alive? {'Yes' if self.movie_thread.is_alive() else 'No'}")
            print(f"Series thread alive? {'Yes' if self.series_thread.is_alive() else 'No'}")
            print(f"Games thread alive? {'Yes' if self.games_thread.is_alive() else 'No'}")

            if not self.movie_thread.is_alive() and not self.series_thread.is_alive() and not self.games_thread.is_alive():
                self.merge_files()
                break
            else: continue        

    def run(self):
        self.start("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")

        self.movie_thread = threading.Thread(target=self.get_movies)
        self.series_thread = threading.Thread(target=self.get_series)
        self.games_thread = threading.Thread(target=self.get_games)
        check = threading.Thread(target=self.check_threads)

        self.movie_thread.start()
        self.series_thread.start()
        self.games_thread.start()
        check.start()

        self.movie_thread.join()
        self.series_thread.join()
        self.games_thread.join()
        check.join()

if __name__ == "__main__":
    imdb = imdb()
    t = time.time()
    imdb.run()
    t2 = time.time() - t
    print(f"Program took {(t2):.5f} seconds to scrape")
    print(f"Program took {((t2) / 60):.5f} hours to scrape")
    print(f"Program took {(((t2) / 60) / 24):.5f} days to scrape")
    print(f"Program took {((((t2) / 60) / 24) / 7):.5f} weeks to scrape")