'''
A collection of utilities for the Recording Representation
project.
'''
# Import libraries
import requests, bs4, re, os, shutil

def image_scraper (url, company):
    '''
    A web scraping utility used to get album covers and record label board pics.
    It downloads and saves images in a directory named after the company.

    Inputs:
        target_url = URL source of images (string)
        company = name of company, used for naming storage (string)

    Output:
        Downloaded images website images saved in local data directory
    '''

    # Declare data directories
    cache_dir = os.path.join("data", "img", company)  # where to store cache files
    os.makedirs(cache_dir, exist_ok=True)  # ensure cache directory exists

    # Save root URL HTML data into bs4 object
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, features="html.parser")

    # Create list of img src locations
    page_imgs = soup.select('img')
    img_list = []
    for img in page_imgs:
        img_str = str(img)
        url = re.search("src=\"([^\n\r]*)\"", img_str)
        img_list.append(url[1])

    # Download and save images
    for i in range(len(img_list)):
    # Set up the image URL and filename
        image_url = img_list[i]
        image_format = image_url.split('.')[-1]
        filename = str(i)+'.'+image_format

        try:
            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream = True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with wb ( write binary ) permission.
                with open(os.path.join(cache_dir, filename),'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ',filename)
            else:
                print('Image Couldn\'t be retreived')
        except:
            print('Bad url: ' + image_url)
