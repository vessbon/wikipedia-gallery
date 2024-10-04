
import bs4
import requests
import lxml


# Scrape wikipedia for images
def get_wikipedia_images(wikipedia_articles):
    images = []

    for article in wikipedia_articles:
        try:
            res = requests.get(article)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
        except:
            print("Could not get article.")
            continue

        main = soup.select('#mw-content-text')
        if len(main) != 0:
            # Get list of valid image holders
            figure_list = main[0].select('figure.mw-default-size')
            trow_list = main[0].select('.trow')

            # Join image holder elements
            img_parents = figure_list + trow_list
            image_list = []

            # Checks parents for images
            for parent in img_parents:
                image_elements = parent.select('img')

                if len(image_elements) != 0:  # Checks if there is an image present
                    sources = [image['src'] for image in image_elements]  # Makes a list out of sources

                    # Append all sources to the image_list
                    for image in sources:
                        image_list.append('https:'+image)

            # Get rid of unnecessary lists
            del image_elements
            del sources

            images.append(image_list)

    return images
