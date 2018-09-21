from MultiScrappingV3 import MultiScrapper
from time import sleep

# This Function Scraps One Page
def ScrapSingleNews(url):
    data = {"headline":url,"details":"Details Data"}
    return data

# Following Code retrieves all news of a single day
# and inserts it to Database
if __name__ == "__main__":

    # Initialize with 2 threads
    scrapper = MultiScrapper(ScrapSingleNews, 2)

    # Add All Pages to scrap
    scrapper.Add("http://url1")
    scrapper.Add("http://url2")
    scrapper.Add("http://url3")

    # Starts scapping
    Alldata = scrapper.ScrapAll()

    # Print the list of data or insert into Database
    print(Alldata)

    # Clear data and add new list of pages
    scrapper.Reset()
