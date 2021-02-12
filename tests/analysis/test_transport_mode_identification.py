# -*- coding: utf-8 -*-

import datetime
import os

import pytest
import numpy as np
import geopandas as gpd
from numpy.testing import assert_almost_equal

import trackintel as ti
from trackintel.io.dataset_reader import read_geolife


class TestTransportModeIdentification:
    def test_check_empty_dataframe(self):
        """Assert that the method does not work for empty DataFrames (but
        that the rest works fine, e.g., method signature)."""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')
        empty_frame = tpls[0:0]
        with pytest.raises(AssertionError):
            empty_frame.as_triplegs.predict_transport_mode(method='simple-coarse')

    def test_simple_coarse_identification_no_crs(self):
        """Assert that the simple-coarse transport mode identification throws the correct \
warning and and yields the correct results for WGS84 ."""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')

        with pytest.warns(UserWarning, match='Your data is not projected. WGS84 is assumed and for length \
calculation the haversine distance is used'):
            tpls_transport_mode = tpls.as_triplegs.predict_transport_mode(method='simple-coarse')

        assert tpls_transport_mode.iloc[0]['mode'] == 'slow_mobility'
        assert tpls_transport_mode.iloc[1]['mode'] == 'motorized_mobility'
        assert tpls_transport_mode.iloc[2]['mode'] == 'fast_mobility'

    def test_simple_coarse_identification_wgs_84(self):
        """Asserts the correct behaviour with data in wgs84"""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')
        tpls_2 = tpls.set_crs(epsg=4326)
        tpls_transport_mode_2 = tpls_2.as_triplegs.predict_transport_mode(method='simple-coarse')

        assert tpls_transport_mode_2.iloc[0]['mode'] == 'slow_mobility'
        assert tpls_transport_mode_2.iloc[1]['mode'] == 'motorized_mobility'
        assert tpls_transport_mode_2.iloc[2]['mode'] == 'fast_mobility'

    def test_simple_coarse_identification_projected(self):
        """Asserts the correct behaviour with data in projected coordinate systems"""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')
        tpls_2 = tpls.set_crs(epsg=4326)
        tpls_3 = tpls_2.to_crs(epsg=2056)
        tpls_transport_mode_3 = tpls_3.as_triplegs.predict_transport_mode(method='simple-coarse')
        assert tpls_transport_mode_3.iloc[0]['mode'] == 'slow_mobility'
        assert tpls_transport_mode_3.iloc[1]['mode'] == 'motorized_mobility'
        assert tpls_transport_mode_3.iloc[2]['mode'] == 'fast_mobility'

    def test_simple_coarse_identification_geographic(self):
        """asserts the correct behaviour with data in geographic coordinate systems"""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')
        tpls_2 = tpls.set_crs(epsg=4326)
        tpls_4 = tpls_2.to_crs(epsg=4269)
        with pytest.raises(UserWarning,
                           match='Your data is in a geographic coordinate system, length calculation fails'):
            tpls_4.as_triplegs.predict_transport_mode(method='simple-coarse')

    def test_check_categories(self):
        """asserts the correct identification of valid category dictionaries"""
        tpls = ti.read_triplegs_csv('tests/data/triplegs_transport_mode_identification.csv', sep=';')
        correct_dict = {2: 'cat1', 7: 'cat2', np.inf: 'cat3'}

        assert ti.analysis.transport_mode_identification.check_categories(correct_dict)
        with pytest.raises(ValueError):
            incorrect_dict = {10: 'cat1', 5: 'cat2', np.inf: 'cat3'}
            tpls.as_triplegs.predict_transport_mode(method='simple-coarse', categories=incorrect_dict)