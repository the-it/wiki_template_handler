from unittest import TestCase

__author__ = 'eso'

import sys
sys.path.append('../../')
from template_handler import TemplateHandler

test_title = "vorlage"
test_title_sperr = "Sperrsatz"
test_title_test = "testtitle"

test_string_argument_1 = "1=test1"
test_string_argument_1_no_key = "test1"
test_string_argument_2 = "2=test2"
test_string_argument_3 = "test3"
test_string_argument_4 = "4=test4"
test_string_argument_5 = "5=test5"

test_string_12_complex = "{{" + test_title + "\n|" + test_string_argument_1 + "\n|" + test_string_argument_2 + "\n}}"
test_string_12_simple = "{{" + test_title + "|" + test_string_argument_1 + "|" + test_string_argument_2 + "}}"

test_dict_argument_1 = {"key": '1', "value": 'test1'}
test_dict_argument_1_no_key = {"key": None, "value": 'test1'}
test_dict_argument_2 = {"key": '2', "value": 'test2'}
test_dict_argument_3 = {"key": None, "value": 'test3'}
test_dict_argument_4 = {"key": '4', "value": 'test4'}
test_dict_argument_5 = {"key": '5', "value": 'test5'}

test_list_12 = [test_dict_argument_1, test_dict_argument_2]


class TestTemplateHandler(TestCase):
    def test_template_from_page(self):
        handler = TemplateHandler(test_string_12_complex)
        self.assertEqual(test_list_12, handler.get_parameterlist())

    def test_get_parameter(self):
        handler = TemplateHandler(test_string_12_complex)
        self.assertEqual(test_dict_argument_1, handler.get_parameter('1'))
        self.assertEqual(test_dict_argument_2, handler.get_parameter('2'))

    def test_get_str(self):
        handler = TemplateHandler()
        handler.set_title(test_title)
        handler.update_parameters(test_list_12)
        self.assertEqual(test_string_12_simple, handler.get_str(str_complex=False))
        self.assertEqual(test_string_12_complex, handler.get_str(str_complex=True))

    def test_without_key(self):
        test_string_12_no_key = "{{" + test_title + "|" + test_string_argument_1_no_key + "|" + test_string_argument_2 + "}}"
        test_list_12_no_key = [test_dict_argument_1_no_key, test_dict_argument_2]
        handler = TemplateHandler(test_string_12_no_key)
        self.assertEqual(test_list_12_no_key, handler.get_parameterlist())

    def test_update_parameters(self):
        test_string_345_simple = "{{" + test_title + "|" + test_string_argument_3 + "|" + test_string_argument_4 + "|" + test_string_argument_5 + "}}"
        test_list_345 = [test_dict_argument_3, test_dict_argument_4, test_dict_argument_5]
        handler = TemplateHandler(test_string_12_simple)
        self.assertEqual(test_dict_argument_1, handler.get_parameter('1'))
        self.assertEqual(test_dict_argument_2, handler.get_parameter('2'))
        handler.update_parameters(test_list_345)
        self.assertEqual(test_string_345_simple, handler.get_str(str_complex=False))

    def test_template_in_template(self):
        test_string_argument_template = "{{otherTemplate|other_argument}}"
        test_string_12_template = "{{" + test_title + "|" + test_string_argument_template + "|" + test_string_argument_2 + "}}"
        test_dict_template_no_key = {'key': None, 'value': '{{otherTemplate|other_argument}}'}
        test_list_template_no_key = [test_dict_template_no_key, test_dict_argument_2]
        handler = TemplateHandler(test_string_12_template)
        self.assertListEqual(test_list_template_no_key, handler.get_parameterlist())
        del handler

        test_string_argument_template2 = "{{Kapitaelchen|Test}}"
        test_string_template_2 = "{{" + test_title_sperr + "|" + test_string_argument_template2 + "}}"
        test_dict_template_2 = {'key': None, 'value': '{{Kapitaelchen|Test}}'}
        test_list_template_2 = [test_dict_template_2]
        handler = TemplateHandler(test_string_template_2)
        self.assertListEqual(test_list_template_2, handler.get_parameterlist())
        del handler

        test_string_argument_1_template = "1={{otherTemplate|other_argument}}"
        test_string_12_template_no_key = "{{" + test_title + "|" + test_string_argument_1_template + "|" + test_string_argument_2 + "}}"
        test_dict_template = {'key': '1', 'value': '{{otherTemplate|other_argument}}'}
        test_list_template = [test_dict_template, test_dict_argument_2]
        handler = TemplateHandler(test_string_12_template_no_key)
        self.assertListEqual(test_list_template, handler.get_parameterlist())

    def test_set_title(self):
        test_string_12_test_title = "{{" + test_title_test + "|" + test_string_argument_1 + "|" + test_string_argument_2 + "}}"
        handler = TemplateHandler(test_string_12_simple)
        handler.set_title(test_title_test)
        self.assertEqual(test_string_12_test_title, handler.get_str(str_complex=False))

    def test_link_with_text(self):
        test_string_argument_2_link = "2 = [[link|text for link]] more"
        test_string_12_link = "{{" + test_title + "|" + test_string_argument_1_no_key + "|" + test_string_argument_2_link + "}}"
        test_dict_link = {"key": '2', "value": '[[link|text for link]] more'}
        test_list_link = [test_dict_argument_1_no_key, test_dict_link]
        handler = TemplateHandler(test_string_12_link)
        self.assertEqual(test_list_link, handler.get_parameterlist())

        del handler

        test_string_argument_link = "[[link|text for link]] more"
        test_string_12_link_no_key = "{{" + test_title + "|" + test_string_argument_1_no_key + "|" + test_string_argument_link + "}}"
        test_dict_link_no_key = {"key": None, "value": '[[link|text for link]] more'}
        test_list_link_no_key = [test_dict_argument_1_no_key, test_dict_link_no_key]
        handler = TemplateHandler(test_string_12_link_no_key)
        self.assertEqual(test_list_link_no_key, handler.get_parameterlist())

        del handler

        test_string_argument_link_new = "HERKUNFT=''[[Hände (Březina)|Hände]],'' S. 57"
        test_string_12_link_no_key = "{{" + test_title + "|" + test_string_argument_1_no_key + "|" + test_string_argument_link_new + "}}"
        test_dict_link_no_key = {"key": "HERKUNFT", "value": "''[[Hände (Březina)|Hände]],'' S. 57"}
        test_list_link_no_key = [test_dict_argument_1_no_key, test_dict_link_no_key]
        handler = TemplateHandler(test_string_12_link_no_key)
        self.assertEqual(test_list_link_no_key, handler.get_parameterlist())

    def test_second_equal(self):
        test_string_argument_second_equal = "BILD=Der Todesgang des armenischen Volkes.pdf{{!}}page=276"
        test_string_second_equal = "{{" + test_title_test + "|" + test_string_argument_1 + "|" + test_string_argument_second_equal + "}}"
        test_dict_second_equal = {"key": "BILD", "value": 'Der Todesgang des armenischen Volkes.pdf{{!}}page=276'}
        test_list_second_equal = [test_dict_argument_1, test_dict_second_equal]
        handler = TemplateHandler(test_string_second_equal)
        self.assertEqual(test_list_second_equal, handler.get_parameterlist())


    def test_BUG_2016_01_07(self):
        test_string = "{{Textdaten\n|AUTOR=[[Otokar Březina]]\n|VORIGER=Hände (Březina)/Orte der Harmonie und der Versöhnung\n|NÄCHSTER=Hände (Březina)/Frauen\n|TITEL=*\n|SUBTITEL=\n|HERKUNFT=''[[Hände (Březina)|Hände]],'' S. 57\n|HERAUSGEBER=\n|AUFLAGE= 1. Auflage\n|ENTSTEHUNGSJAHR=1908\n|ERSCHEINUNGSJAHR=1908\n|ERSCHEINUNGSORT=Wien\n|VERLAG=Moriz Frisch\n|ÜBERSETZER=[[Emil Saudek]]\n|ORIGINALTITEL=*\n|ORIGINALHERKUNFT=''Ruce,'' Prag 1901\n|BILD=\n|QUELLE=[[C:Hände (Březina)|Commons]]\n|KURZBESCHREIBUNG=\n|BEARBEITUNGSSTAND=fertig\n|WIKIPEDIA=\n|INDEXSEITE=Hände (Březina)\n}}"
        handler = TemplateHandler(test_string)
        list_of_keys = ["AUTOR",
                        "VORIGER",
                        "NÄCHSTER",
                        "TITEL",
                        "SUBTITEL",
                        "HERKUNFT",
                        "HERAUSGEBER",
                        "AUFLAGE",
                        "ENTSTEHUNGSJAHR",
                        "ERSCHEINUNGSJAHR",
                        "ERSCHEINUNGSORT",
                        "VERLAG",
                        "ÜBERSETZER",
                        "ORIGINALTITEL",
                        "ORIGINALHERKUNFT",
                        "BILD",
                        "QUELLE",
                        "KURZBESCHREIBUNG",
                        "BEARBEITUNGSSTAND",
                        "WIKIPEDIA",
                        "INDEXSEITE"]
        list_of_values = ["[[Otokar Březina]]",
                          "Hände (Březina)/Orte der Harmonie und der Versöhnung",
                          "Hände (Březina)/Frauen",
                          "*",
                          "",
                          "''[[Hände (Březina)|Hände]],'' S. 57",
                          "",
                          "1. Auflage",
                          "1908",
                          "1908",
                          "Wien",
                          "Moriz Frisch",
                          "[[Emil Saudek]]",
                          "*",
                          "''Ruce,'' Prag 1901",
                          "",
                          "[[C:Hände (Březina)|Commons]]",
                          "",
                          "fertig",
                          "",
                          "Hände (Březina)"]
        for i in range(len(list_of_keys)):
            self.assertDictEqual({'value': list_of_values[i], 'key': list_of_keys[i]}, handler.get_parameter(list_of_keys[i]))