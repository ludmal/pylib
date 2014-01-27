
from google.appengine.api import urlfetch
import similarity
import util
from lxml import html
from PIL import Image
import cStringIO
import logging

IMAGE_SIZE = 20000
ALT_SIMILARITY = 0.4
IMAGE_SIZE_RATIO = 0.3


def get_size_ratio(height=0, width=0):
    diff = height-width
    return abs(diff/float(height+width))


def get_main_image_from_urls(urls, title=''):
    try:
        valid_urls = []
        if len(urls) == 0:
            return ''

        for u in urls:
            url = util.valid_url(u[0])

            if url != '':
                valid_urls.append(url)

                if similarity.get_similarity(u[1], title) > ALT_SIMILARITY:
                    return url
                    break

        for url in valid_urls:

            try:

                if url != '':
                    result = urlfetch.fetch(url)
                    if result.status_code == 200:
                        file = cStringIO.StringIO(result.content)
                        im = Image.open(file)
                        size = result.headers["Content-Length"]
                        height, width = im.size
                        if not size or size == '':
                            size = 0
                        #print get_size_ratio(height, width)
                        #print url
                        if int(size) > IMAGE_SIZE and get_size_ratio(height, width) < IMAGE_SIZE_RATIO:
                            return url
                            break

            except Exception, ex:
                logging.error('get_main_image_from_urls: %s' % ex.message)
                continue

        return ''
    except Exception, ex:
        logging.error('get_main_image_from_urls: %s' % ex.message)
        return ''


def get_main_image(link):
    try:
        data = urlfetch.fetch(str(link))

        if data.statuscode == 200:
            result = data.content
            doc = html.fromstring(result)

            t = doc.xpath('//h1')

            if len(t) > 0:
                title = t[0].text_content()
            else:
                ti = doc.xpath('//title')
                title = ti[0].text_content() if len(ti) > 0 else ''

            image_urls = []

            for img in doc.xpath('//img'):
                t = img.get('src'), img.get('alt')
                image_urls.append(t)

            return get_main_image_from_urls(image_urls, title)
        return ''
    except Exception, ex:
        logging.error('get_main_image: %s' % ex.message)
        return ''
