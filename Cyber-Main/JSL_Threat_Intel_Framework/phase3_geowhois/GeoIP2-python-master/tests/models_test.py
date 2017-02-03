#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
sys.path.append('..')

import geoip2.models

if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] == 2:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches


class TestModels(unittest.TestCase):
    def test_insights_full(self):
        raw = {
            'city': {
                'confidence': 76,
                'geoname_id': 9876,
                'names': {'en': 'Minneapolis'},
            },
            'continent': {
                'code': 'NA',
                'geoname_id': 42,
                'names': {'en': 'North America'},
            },
            'country': {
                'confidence': 99,
                'geoname_id': 1,
                'iso_code': 'US',
                'names': {'en': 'United States of America'},
            },
            'location': {
                'average_income': 24626,
                'accuracy_radius': 1500,
                'latitude': 44.98,
                'longitude': 93.2636,
                'metro_code': 765,
                'population_density': 1341,
                'time_zone': 'America/Chicago',
            },
            'postal': {
                'code': '55401',
                'confidence': 33,
            },
            'subdivisions': [{
                'confidence': 88,
                'geoname_id': 574635,
                'iso_code': 'MN',
                'names': {'en': 'Minnesota'},
            }, {
                'geoname_id': 123,
                'iso_code': 'HP',
                'names': {'en': 'Hennepin'},
            }],
            'registered_country': {
                'geoname_id': 2,
                'iso_code': 'CA',
                'names': {'en': 'Canada'},
            },
            'represented_country': {
                'geoname_id': 3,
                'iso_code': 'GB',
                'names': {'en': 'United Kingdom'},
                'type': 'military',
            },
            'traits': {
                'autonomous_system_number': 1234,
                'autonomous_system_organization': 'AS Organization',
                'domain': 'example.com',
                'ip_address': '1.2.3.4',
                'is_anonymous_proxy': 0,
                'is_us_military': 1,
                'isp': 'Comcast',
                'network_speed': 'cable/DSL',
                'organization': 'Blorg',
                'user_type': 'college',
            },
        }

        model = geoip2.models.Insights(raw)
        self.assertEqual(
            type(model), geoip2.models.Insights,
            'geoip2.models.Insights object')
        self.assertEqual(
            type(model.city), geoip2.records.City,
            'geoip2.records.City object')
        self.assertEqual(
            type(model.continent), geoip2.records.Continent,
            'geoip2.records.Continent object')
        self.assertEqual(
            type(model.country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.registered_country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.represented_country), geoip2.records.RepresentedCountry,
            'geoip2.records.RepresentedCountry object')
        self.assertEqual(
            type(model.location), geoip2.records.Location,
            'geoip2.records.Location object')
        self.assertEqual(
            type(model.subdivisions[0]), geoip2.records.Subdivision,
            'geoip2.records.Subdivision object')
        self.assertEqual(
            type(model.traits), geoip2.records.Traits,
            'geoip2.records.Traits object')
        self.assertEqual(model.raw, raw, 'raw method returns raw input')
        self.assertEqual(model.subdivisions[0].iso_code, 'MN',
                         'div 1 has correct iso_code')
        self.assertEqual(model.subdivisions[0].confidence, 88,
                         'div 1 has correct confidence')
        self.assertEqual(model.subdivisions[0].geoname_id, 574635,
                         'div 1 has correct geoname_id')
        self.assertEqual(model.subdivisions[0].names, {'en': 'Minnesota'},
                         'div 1 names are correct')
        self.assertEqual(model.subdivisions[1].name, 'Hennepin',
                         'div 2 has correct name')
        self.assertEqual(model.subdivisions.most_specific.iso_code, 'HP',
                         'subdivisions.most_specific returns HP')
        self.assertEqual(model.represented_country.name, 'United Kingdom',
                         'represented_country name is correct')
        self.assertEqual(model.represented_country.type, 'military',
                         'represented_country type is correct')
        self.assertEqual(model.location.average_income, 24626,
                         'correct average_income')
        self.assertEqual(model.location.latitude, 44.98, 'correct latitude')
        self.assertEqual(model.location.longitude, 93.2636,
                         'correct longitude')
        self.assertEqual(model.location.metro_code, 765, 'correct metro_code')
        self.assertEqual(model.location.population_density, 1341,
                         'correct population_density')

        self.assertRegex(
            str(model),
            r'^geoip2.models.Insights\(\{.*geoname_id.*\}, \[.*en.*\]\)',
            'Insights str representation looks reasonable')

        self.assertEqual(model, eval(repr(model)),
                         "Insights repr can be eval'd")

        self.assertRegex(
            str(model.location), r'^geoip2.records.Location\(.*longitude=.*\)',
            'Location str representation is reasonable')

        self.assertEqual(model.location, eval(repr(model.location)),
                         "Location repr can be eval'd")

    def test_insights_min(self):
        model = geoip2.models.Insights({'traits': {'ip_address': '5.6.7.8'}})
        self.assertEqual(
            type(model), geoip2.models.Insights,
            'geoip2.models.Insights object')
        self.assertEqual(
            type(model.city), geoip2.records.City,
            'geoip2.records.City object')
        self.assertEqual(
            type(model.continent), geoip2.records.Continent,
            'geoip2.records.Continent object')
        self.assertEqual(
            type(model.country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.registered_country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.location), geoip2.records.Location,
            'geoip2.records.Location object')
        self.assertEqual(
            type(model.traits), geoip2.records.Traits,
            'geoip2.records.Traits object')
        self.assertEqual(
            type(model.subdivisions.most_specific), geoip2.records.Subdivision,
            'geoip2.records.Subdivision object returned even'
            'when none are available.')
        self.assertEqual(model.subdivisions.most_specific.names, {},
                         'Empty names hash returned')

    def test_city_full(self):
        raw = {
            'continent': {
                'code': 'NA',
                'geoname_id': 42,
                'names': {'en': 'North America'},
            },
            'country': {
                'geoname_id': 1,
                'iso_code': 'US',
                'names': {'en': 'United States of America'},
            },
            'registered_country': {
                'geoname_id': 2,
                'iso_code': 'CA',
                'names': {'en': 'Canada'},
            },
            'traits': {
                'ip_address': '1.2.3.4',
                'is_satellite_provider': True,
            },
        }
        model = geoip2.models.City(raw)
        self.assertEqual(
            type(model), geoip2.models.City, 'geoip2.models.City object')
        self.assertEqual(
            type(model.city), geoip2.records.City,
            'geoip2.records.City object')
        self.assertEqual(
            type(model.continent), geoip2.records.Continent,
            'geoip2.records.Continent object')
        self.assertEqual(
            type(model.country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.registered_country), geoip2.records.Country,
            'geoip2.records.Country object')
        self.assertEqual(
            type(model.location), geoip2.records.Location,
            'geoip2.records.Location object')
        self.assertEqual(
            type(model.traits), geoip2.records.Traits,
            'geoip2.records.Traits object')
        self.assertEqual(model.raw, raw, 'raw method returns raw input')
        self.assertEqual(model.continent.geoname_id, 42,
                         'continent geoname_id is 42')
        self.assertEqual(model.continent.code, 'NA', 'continent code is NA')
        self.assertEqual(model.continent.names, {'en': 'North America'},
                         'continent names is correct')
        self.assertEqual(model.continent.name, 'North America',
                         'continent name is correct')
        self.assertEqual(model.country.geoname_id, 1,
                         'country geoname_id is 1')
        self.assertEqual(model.country.iso_code, 'US',
                         'country iso_code is US')
        self.assertEqual(model.country.names,
                         {'en': 'United States of America'},
                         'country names is correct')
        self.assertEqual(model.country.name, 'United States of America',
                         'country name is correct')
        self.assertEqual(model.country.confidence, None,
                         'country confidence is None')
        self.assertEqual(model.registered_country.iso_code, 'CA',
                         'registered_country iso_code is CA')
        self.assertEqual(model.registered_country.names, {'en': 'Canada'},
                         'registered_country names is correct')
        self.assertEqual(model.registered_country.name, 'Canada',
                         'registered_country name is correct')
        self.assertEqual(model.traits.is_anonymous_proxy, False,
                         'traits is_anonymous_proxy returns False by default')
        self.assertEqual(model.traits.is_satellite_provider, True,
                         'traits is_setellite_provider is True')
        self.assertEqual(model.raw, raw, 'raw method produces raw output')

        self.assertRegex(
            str(model),
            r'^geoip2.models.City\(\{.*geoname_id.*\}, \[.*en.*\]\)')

        self.assertFalse(model == True,
                         '__eq__ does not blow up on weird input')

    def test_unknown_keys(self):
        model = geoip2.models.City({'traits': {'ip_address': '1.2.3.4',
                                               'invalid': 'blah'},
                                    'unk_base': {'blah': 1}})
        with self.assertRaises(AttributeError):
            model.unk_base
        with self.assertRaises(AttributeError):
            model.traits.invalid
        self.assertEqual(model.traits.ip_address, '1.2.3.4', 'correct ip')


class TestNamess(unittest.TestCase):

    raw = {
        'continent': {
            'code': 'NA',
            'geoname_id': 42,
            'names': {
                'de': 'Nordamerika',
                'en': 'North America',
                'es': 'América del Norte',
                'ja': '北アメリカ',
                'pt-BR': 'América do Norte',
                'ru': 'Северная Америка',
                'zh-CN': '北美洲',
            },
        },
        'country': {
            'geoname_id': 1,
            'iso_code': 'US',
            'names': {
                'en': 'United States of America',
                'fr': 'États-Unis',
                'zh-CN': '美国',
            },
        },
        'traits': {
            'ip_address': '1.2.3.4',
        },
    }

    def test_names(self):
        model = geoip2.models.Country(self.raw, locales=['sq', 'ar'])
        self.assertEqual(model.continent.names, self.raw['continent']['names'],
                         'Correct names dict for continent')
        self.assertEqual(model.country.names, self.raw['country']['names'],
                         'Correct names dict for country')

    def test_three_locales(self):
        model = geoip2.models.Country(self.raw, locales=['fr', 'zh-CN', 'en'])
        self.assertEqual(model.continent.name, '北美洲',
                         'continent name is in Chinese (no French available)')
        self.assertEqual(model.country.name, 'États-Unis',
                         'country name is in French')

    def test_two_locales(self):
        model = geoip2.models.Country(self.raw, locales=['ak', 'fr'])
        self.assertEqual(model.continent.name, None,
                         'continent name is undef (no Akan or French '
                         'available)')
        self.assertEqual(model.country.name, 'États-Unis',
                         'country name is in French')

    def test_unknown_locale(self):
        model = geoip2.models.Country(self.raw, locales=['aa'])
        self.assertEqual(model.continent.name, None,
                         'continent name is undef (no Afar available)')
        self.assertEqual(model.country.name, None,
                         'country name is in None (no Afar available)')

    def test_german(self):
        model = geoip2.models.Country(self.raw, locales=['de'])
        self.assertEqual(model.continent.name, 'Nordamerika',
                         'Correct german name for continent')


if __name__ == '__main__':
    unittest.main()
