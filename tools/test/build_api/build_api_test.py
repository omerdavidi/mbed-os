"""
mbed SDK
Copyright (c) 2016 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
from mock import patch
from tools.build_api import prepare_toolchain, build_project, build_library

"""
Tests for build_api.py
"""

class BuildApiTests(unittest.TestCase):
    """
    Test cases for Build Api
    """

    def setUp(self):
        """
        Called before each test case

        :return:
        """
        self.target = "K64F"
        self.src_paths = ['.']
        self.toolchain_name = "ARM"
        self.build_path = "build_path"

    def tearDown(self):
        """
        Called after each test case

        :return:
        """
        pass

    @patch('tools.config.Config.__init__')
    def test_prepare_toolchain_app_config(self, mock_config_init):
        """
        Test that prepare_toolchain uses app_config correctly

        :param mock_config_init: mock of Config __init__
        :return:
        """
        app_config = "app_config"
        mock_config_init.return_value = None

        prepare_toolchain(self.src_paths, self.target, self.toolchain_name,
                          app_config=app_config)

        mock_config_init.assert_called_with(self.target, self.src_paths,
                                            app_config=app_config)

    @patch('tools.config.Config.__init__')
    def test_prepare_toolchain_no_app_config(self, mock_config_init):
        """
        Test that prepare_toolchain correctly deals with no app_config

        :param mock_config_init: mock of Config __init__
        :return:
        """
        mock_config_init.return_value = None

        prepare_toolchain(self.src_paths, self.target, self.toolchain_name)

        mock_config_init.assert_called_with(self.target, self.src_paths,
                                            app_config=None)

    @patch('tools.build_api.scan_resources')
    @patch('tools.build_api.mkdir')
    @patch('os.path.exists')
    @patch('tools.build_api.prepare_toolchain')
    def test_build_project_app_config(self, mock_prepare_toolchain, mock_exists, _, __):
        """
        Test that build_project uses app_config correctly

        :param mock_prepare_toolchain: mock of function prepare_toolchain
        :param mock_exists: mock of function os.path.exists
        :param _: mock of function mkdir (not tested)
        :param __: mock of function scan_resources (not tested)
        :return:
        """
        app_config = "app_config"
        mock_exists.return_value = False
        mock_prepare_toolchain().link_program.return_value = 1, 2

        build_project(self.src_paths, self.build_path, self.target,
                      self.toolchain_name, app_config=app_config)

        args = mock_prepare_toolchain.call_args
        self.assertTrue('app_config' in args[1],
                        "prepare_toolchain was not called with app_config")
        self.assertEqual(args[1]['app_config'], app_config,
                         "prepare_toolchain was called with an incorrect app_config")

    @patch('tools.build_api.scan_resources')
    @patch('tools.build_api.mkdir')
    @patch('os.path.exists')
    @patch('tools.build_api.prepare_toolchain')
    def test_build_project_no_app_config(self, mock_prepare_toolchain, mock_exists, _, __):
        """
        Test that build_project correctly deals with no app_config

        :param mock_prepare_toolchain: mock of function prepare_toolchain
        :param mock_exists: mock of function os.path.exists
        :param _: mock of function mkdir (not tested)
        :param __: mock of function scan_resources (not tested)
        :return:
        """
        mock_exists.return_value = False
        # Needed for the unpacking of the returned value
        mock_prepare_toolchain().link_program.return_value = 1, 2

        build_project(self.src_paths, self.build_path, self.target,
                      self.toolchain_name)

        args = mock_prepare_toolchain.call_args
        self.assertTrue('app_config' in args[1],
                        "prepare_toolchain was not called with app_config")
        self.assertEqual(args[1]['app_config'], None,
                         "prepare_toolchain was called with an incorrect app_config")

    @patch('tools.build_api.scan_resources')
    @patch('tools.build_api.mkdir')
    @patch('os.path.exists')
    @patch('tools.build_api.prepare_toolchain')
    def test_build_library_app_config(self, mock_prepare_toolchain, mock_exists, _, __):
        """
        Test that build_library uses app_config correctly

        :param mock_prepare_toolchain: mock of function prepare_toolchain
        :param mock_exists: mock of function os.path.exists
        :param _: mock of function mkdir (not tested)
        :param __: mock of function scan_resources (not tested)
        :return:
        """
        app_config = "app_config"
        mock_exists.return_value = False

        build_library(self.src_paths, self.build_path, self.target,
                      self.toolchain_name, app_config=app_config)

        args = mock_prepare_toolchain.call_args
        self.assertTrue('app_config' in args[1],
                        "prepare_toolchain was not called with app_config")
        self.assertEqual(args[1]['app_config'], app_config,
                         "prepare_toolchain was called with an incorrect app_config")

    @patch('tools.build_api.scan_resources')
    @patch('tools.build_api.mkdir')
    @patch('os.path.exists')
    @patch('tools.build_api.prepare_toolchain')
    def test_build_library_no_app_config(self, mock_prepare_toolchain, mock_exists, _, __):
        """
        Test that build_library correctly deals with no app_config

        :param mock_prepare_toolchain: mock of function prepare_toolchain
        :param mock_exists: mock of function os.path.exists
        :param _: mock of function mkdir (not tested)
        :param __: mock of function scan_resources (not tested)
        :return:
        """
        mock_exists.return_value = False

        build_library(self.src_paths, self.build_path, self.target,
                      self.toolchain_name)

        args = mock_prepare_toolchain.call_args
        self.assertTrue('app_config' in args[1],
                        "prepare_toolchain was not called with app_config")
        self.assertEqual(args[1]['app_config'], None,
                         "prepare_toolchain was called with an incorrect app_config")

if __name__ == '__main__':
    unittest.main()
