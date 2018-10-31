from data import XmlData
from excel import Excel


class ExportXml(object):
    def __init__(self, func_relation_id):
        self.func_relation_id = func_relation_id

    def run(self):
        excel = Excel()

        xml = XmlData(self.func_relation_id)
        xml_data = xml.get_func_xml()
        xml_filename = xml.func_info.name

        excel.write_to_xls(xml_data, xml_filename)


if __name__ == '__main__':
    export_xml = ExportXml(1)
    export_xml.run()
