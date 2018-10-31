from data import XmlData
from excel import Excel


class ExportXml(object):
    def __init__(self, func_relation_id, xls_filename):
        self.func_relation_id = func_relation_id
        self.xls_filename = xls_filename

    def run(self):
        excel = Excel(self.xls_filename)

        xml = XmlData(self.func_relation_id)
        xml_data = xml.get_func_xml()

        excel.write_to_xls(xml_data)


if __name__ == '__main__':
    export_xml = ExportXml(1, 'a')
    export_xml.run()
