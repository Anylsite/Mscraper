from selenium.webdriver.chrome.options import Options
import re

options = Options()
options.add_argument('--headless')
HEADLESS_OPTIONS = {'chrome_options': options}


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def split_lists(lst, num):
    k, m = divmod(len(lst), num)
    return [lst[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(num)]


class AnyEC(object):
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except:
                pass
        return False


def get_first_element(element, selector, default=None, getText=False):
    """Return the first found element with a given css selector

    Params:
        - element {beautifulsoup element}: element to be searched
        - selector {str}: css selector to search for
        - default {any}: default return value
        - getText

    Returns:
        beautifulsoup element if match is found, otherwise return the default.
    """
    try:
        el = element.select_one(selector)
        if not el:
            return default

        if getText:
            return getTextSafe(el)
        else:
            return el
    except AttributeError as err:
        print(err.args)
        print("ERROR, get_first_element")
        return default

def getTextSafe(element):

    if element is not None:
        return element.getText().strip()



def all_or_default(element, selector, default=[]):
    """Get all matching elements for a css selector within an element

    Params:
        - element: beautifulsoup element to search
        - selector: str css selector to search for
        - default: default value if there is an error or no elements found

    Returns:
        {list}: list of all matching elements if any are found, otherwise return
        the default value
    """
    try:
        elements = element.select(selector)
        if len(elements) == 0:
            return default
        return element.select(selector)
    except AttributeError as err:
        print(err.args)
        print("ERROR, all_or_default")
        return default


def get_job_info(job):
    """
    Returns:
        dict of job's title, company, date_range, location, description
    """
    position_elements = all_or_default(
        job, '.pv-entity__role-details-container')

    # Handle UI case where user has muttiple consec roles at same company
    if (position_elements):
        company = get_first_element(job,
                                  '.pv-entity__company-summary-info > h3 > span:nth-of-type(2)', getText=True)

        company_href = get_first_element(
            job, 'a[data-control-name="background_details_company"]')['href']
        pattern = re.compile('^/company/.*?/$')
        if pattern.match(company_href):
            li_company_url = 'https://www.linkedin.com/' + company_href
        else:
            li_company_url = ''
        positions = list(map(lambda pos: get_info(pos, {
            'title': '.pv-entity__summary-info-v2 > h3 > span:nth-of-type(2)',
            'date_range': '.pv-entity__date-range span:nth-of-type(2)',
            'location': '.pv-entity__location > span:nth-of-type(2)',
            'description': '.pv-entity__description'
        }), position_elements))
        for pos in positions:
            pos['company'] = company
            pos['li_company_url'] = li_company_url
            if pos['description'] is not None:
                pos['description'] = pos['description'].replace(
                    'See less\n', '').replace('... See more', '').strip()

        return positions

    else:
        job_info = get_info(job, {
            'title': '.pv-entity__summary-info h3:nth-of-type(1)',
            'company': '.pv-entity__secondary-title',
            'date_range': '.pv-entity__date-range span:nth-of-type(2)',
            'location': '.pv-entity__location span:nth-of-type(2)',
            'description': '.pv-entity__description',
        })
        if job_info['description'] is not None:
            job_info['description'] = job_info['description'].replace(
                'See less\n', '').replace('... See more', '').strip()

        company_href = get_first_element(
            job, 'a[data-control-name="background_details_company"]')['href']
        pattern = re.compile('^/company/.*?/$')
        if pattern.match(company_href):
            job_info['li_company_url'] = 'https://www.linkedin.com' + company_href
        else:
            job_info['li_company_url'] = ''

        return [job_info]


def get_info(element, mapping, default=None):
    """Turn beautifulsoup element and key->selector dict into a key->value dict

    Args:
        - element: A beautifulsoup element
        - mapping: a dictionary mapping key(str)->css selector(str)
        - default: The defauly value to be given for any key that has a css
        selector that matches no elements

    Returns:
        A dict mapping key to the text content of the first element that matched
        the css selector in the element.  If no matching element is found, the
        key's value will be the default param.
    """
    return {key: get_first_element(element, mapping[key], default=default, getText=True) for key in mapping}


def get_school_info(school):
    """
    Returns:
        dict of school name, degree, grades, field_of_study, date_range, &
        extra-curricular activities
    """
    return get_info(school, {
        'name': '.pv-entity__school-name',
        'degree': '.pv-entity__degree-name span:nth-of-type(2)',
        'grades': '.pv-entity__grade span:nth-of-type(2)',
        'field_of_study': '.pv-entity__fos span:nth-of-type(2)',
        'date_range': '.pv-entity__dates span:nth-of-type(2)',
        'activities': '.activities-societies',
        'description': '.pv-entity__extra-details'
    })
