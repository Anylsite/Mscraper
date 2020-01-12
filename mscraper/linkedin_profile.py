from utils import *
from ResultsObject import ResultsObject
import re


class LinkedinProfile(ResultsObject):

    attributes = ['personal_info','experiences'
                 ,'skills', 'accomplishments', 'interests'
                  ]

    def to_dict(self):
        info = super(LinkedinProfile, self).to_dict()
        return info

    @property
    def personal_info(self):
        personal_info = {}

        # logged account
        personal_info['name'] = getTextSafe(get_first_element(self.soup, '.pv-top-card-v3--list').find('li'))
        personal_info['headline'] = getTextSafe(get_first_element(self.soup, '.flex-1.mr5').find('h2'))
        personal_info['location'] = getTextSafe(get_first_element(self.soup, '.pv-top-card-v3--list-bullet').find('li'))
        personal_info['company'] = getTextSafe(get_first_element(self.soup, 'a[data-control-name="position_see_more"]'))
        personal_info['school'] = getTextSafe(get_first_element(self.soup, 'a[data-control-name="education_see_more"]'))
        personal_info['summary'] = get_first_element(self.soup, '.pv-about-section .pv-about__summary-text', '', getText=True).replace('... see more', '').strip()

        return personal_info

    @property
    def experiences(self):
        experiences = {}
        container = get_first_element(self.soup, '.background-section')

        jobs = all_or_default(
            container, '#experience-section ul .pv-position-entity')
        jobs = list(map(get_job_info, jobs))
        jobs = flatten_list(jobs)

        experiences['jobs'] = jobs

        schools = all_or_default(
            container, '#education-section .pv-education-entity')
        schools = list(map(get_school_info, schools))
        experiences['education'] = schools

        return experiences

    @property
    def skills(self):
        skills_els = self.soup.select('.pv-skill-category-entity__skill-wrapper')
        skills = []

        for el in skills_els:
            skills.append(getTextSafe(el.find("span")))

        return skills

    @property
    def accomplishments(self):
        accomplishments = dict.fromkeys([
            'publications', 'certifications', 'patents',
            'courses', 'projects', 'honors',
            'test_scores', 'languages', 'organizations'
        ])
        container = get_first_element(self.soup, '.pv-accomplishments-section')
        for key in accomplishments:
            accs = all_or_default(container, 'section.' + key + ' ul > li')
            accs = map(lambda acc: acc.get_text() if acc else None, accs)
            accomplishments[key] = list(accs)
        return accomplishments

    @property
    def interests(self):
        container = get_first_element(self.soup, '.pv-interests-section')
        interests = all_or_default(container, 'ul > li')
        interests = map(lambda i: get_first_element(
            i, '.pv-entity__summary-title', getText=True), interests)
        return list(interests)
