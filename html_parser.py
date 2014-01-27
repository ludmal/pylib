__author__ = 'Ludmal.DESILVA'

from lxml import html
import re
import image_parser
import logging

extract_patterns = 'id:articleImage|' \
                   'id:displayFrame|' \
                   'class:cnnArticleGalleryPhotoContainer|' \
                   'class:article-entry|' \
                   'class:storyBody|' \
                   'class:article-body|'\
                   'class:article-featured-image|' \
                   'class:content'


ignore_patterns = []
ignore_patterns.append('doubleclick.net')

IMAGE_TYPE_REGEX = re.compile('http://.*(jpg|jpeg)$')

_title = ''
_settings = ''


def _validate_image(image_url):
    for i in ignore_patterns:
        if i.lower() in image_url.lower():
            return ''
            break
    return image_url


def _extract_settings(key):
    try:
        if _settings == '':
            return

        sett = _settings.split('|')
        set_dic = {}

        for s in sett:
            i = s.split(':')
            set_dic[i[0]] = i[1]

        return set_dic[key]
    except Exception, ex:
        logging.error('_extract_settings:%s' % ex.message)
        return ''


def _image_count(html_content):
    image_doc = html.fromstring(html_content)
    image_list = image_doc.xpath('//img')
    return len(image_list)


def _get_title(doc):
    val = _extract_settings('title')

    global _title

    if val != '':
        if val == 'h1':
            t = doc.xpath('//h1')
            _title = t[0].text_content() if len(t) > 0 else ''
            return _title

        if val == 'title':
            ti = doc.xpath('//title')
            _title = ti[0].text_content() if len(ti) > 0 else ''
            return _title

        if val == 'h12':
            t = doc.xpath('//h1')
            _title = t[1].text_content if len(t) > 1 else ''
            return _title

    t = doc.xpath('//h1')

    if len(t) > 0:
        _title = t[0].text_content()
    else:
        ti = doc.xpath('//title')
        _title = ti[0].text_content() if len(ti) > 0 else ''

    return _title.strip()


def _get_desc(doc):
    meta = doc.xpath('//meta[re:test(@name, "^description$", "i")]',
                          namespaces={"re": "http://exslt.org/regular-expressions"})

    desc = meta[0].get('content') if len(meta) > 0 else ''
    return desc.strip()


def _get_image(doc):

    image_html = ''

    list = [l for l in extract_patterns.split('|')]

    """for i in list:
        p = i.split(':')
        pattern = Pattern(p[0], p[1])
        patterns.append(pattern)"""

    patterns = [Pattern(i.split(':')[0], i.split(':')[1]) for i in list]

    for p in patterns:
        try:
            if p.pattern_type == 'id':
                d = doc.get_element_by_id(p.pattern_value)
                image_html = html.tostring(d).strip()
                if len(image_html) > 0 and _image_count(image_html):
                    break
            elif p.pattern_type == 'class':
                d = doc.find_class(p.pattern_value)

                if d:
                    image_html = html.tostring(d[0])
                    if len(image_html) > 0 and _image_count(image_html) > 0:
                        break
        except Exception, ex:
            continue

    image_urls = []

    if image_html != '':
        image_doc = html.fromstring(image_html)
        image_extracted_links = image_doc.xpath('//img')
        if len(image_extracted_links) == 1:
            return image_extracted_links[0].get('src')
    else:
        image_extracted_links = doc.xpath('//img')

    for img in image_extracted_links:
        src = img.get('src')
        t = src, img.get('alt')
        image_urls.append(t)
        """if re.match(IMAGE_TYPE_REGEX, src):
            t = src, img.get('alt')
            image_urls.append(t)"""

    return _validate_image(image_parser.get_main_image_from_urls(image_urls, _title))


def _get_html(doc):
    html.tostring(doc)


def _get_summary(doc):
    html.tostring(doc)


class Document():
    def __init__(self, content=None, settings=''):
        global _settings
        _settings = settings

        doc = html.fromstring(content)
        self.html = content
        self.title = _get_title(doc)
        self.image = _get_image(doc)
        self.desc = _get_desc(doc)
        self.summary = _get_summary(doc)


class Pattern():
    def __init__(self, pattern_type, pattern_value):
        self.pattern_type = pattern_type
        self.pattern_value = pattern_value
