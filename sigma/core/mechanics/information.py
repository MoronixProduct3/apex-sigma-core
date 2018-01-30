# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml


class Information(object):
    @staticmethod
    def get_version():
        return Version()

    @staticmethod
    def get_authors():
        return Authors()

    @staticmethod
    def get_donors():
        return Donors()


class Version(object):
    def __init__(self):
        with open('info/version.yml', encoding='utf-8') as version_file:
            version_data = yaml.safe_load(version_file)
        self.raw = version_data
        self.beta = version_data['beta']
        self.timestamp = version_data['build_date']
        self.codename = version_data['codename']
        self.major = version_data['version']['major']
        self.minor = version_data['version']['minor']
        self.patch = version_data['version']['patch']


class Author(object):
    def __init__(self, author):
        self.name = author['name']
        self.discriminator = author['discriminator']
        self.id = author['id']


class Authors(object):
    def __init__(self):
        with open('info/authors.yml', encoding='utf-8') as authors_file:
            authors_data = yaml.safe_load(authors_file)
        self.raw = authors_data
        self.authors = []
        for author in authors_data:
            author_object = Author(author)
            self.authors.append(author_object)


class Donor(object):
    def __init__(self, donor):
        self.name = donor['name']
        self.tier = donor['tier']
        self.avatar = donor['avatar']
        self.id = donor['duid']


class Donors(object):
    def __init__(self):
        with open('info/donors.yml', encoding='utf-8') as donors_file:
            donors_data = yaml.safe_load(donors_file)
        self.raw = donors_data
        self.raw_list = donors_data['donors']
        self.donors = []
        for donor in donors_data['donors']:
            donor_object = Donor(donor)
            self.donors.append(donor_object)
