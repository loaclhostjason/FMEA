import xlwt
from config import Config
import os


class Excel(object):
    def __init__(self):
        self.xls_name = 'Sheet Name'

    @staticmethod
    def set_style(center=False, vi=False):
        alignment = xlwt.Alignment()
        # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT,
        # HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        if center:
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
        # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        if vi:
            alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
        style = xlwt.XFStyle()  # Create Style
        style.alignment = alignment  # Add Alignment to Style
        return style

    def write_to_xls(self, content, filename):
        table_head = [
            '过程',
            '过程步骤',
            '作业要素',
            '过程项目功能',
            '过程步骤功能和产品特性',
            '作业要素功能和过程特性',
            'FE(过程项目失效后果)',
            'S',
            'FM(失效模式)',
            'FC(失效原因)',
            '预防',
            'O',
            '探测原因',
            '探测失效模式',
            'D',
            'RPN',
            'AP',
            '预防',
            '探测',
            '责任人',
            '生成日期',
            '状态',
            '证据',
            '完成日期',
            'S',
            'O',
            'D',
            'RPN',
            'AP'
        ]

        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet(self.xls_name, cell_overwrite_ok=True)

        sheet.write_merge(0, 0, 0, 2, '结构分析', self.set_style(center=True))
        sheet.write_merge(0, 0, 3, 5, '功能分析', self.set_style(center=True))
        sheet.write_merge(0, 0, 6, 9, '失效分析', self.set_style(center=True))
        sheet.write_merge(0, 0, 10, 16, '风险分析', self.set_style(center=True))
        sheet.write_merge(0, 0, 17, 28, '优化分析', self.set_style(center=True))

        # 写excel表头
        head_len = len(table_head)
        for i in range(head_len):
            sheet.write(1, i, table_head[i])
            sheet.col(i).width = 256 * 30

        # start -----------------------------
        for row, val in enumerate(content):
            for i, col in enumerate(val):
                sheet.write(row + 2, i, col)
        # end ---------------------------------------

        # 行 字段 value
        # sheet.write(0, 2, '333')  # row, column, value

        # contentRow = len(content)  # 列表元素个数  = 待写入内容行数

        # 从content获取要写入的第一列的内容,存入列表
        # first_col = []
        # for i in range(contentRow):
        #     first_col.append(content[i][0])
        # print("first_col", first_col)
        #
        # # 去掉列表中重复元素，并且顺序不变
        # nfirst_col = list(set(first_col))
        # nfirst_col.sort(key=first_col.index)  # sort排序与原顺序一致
        # print("nfirst_col", nfirst_col)

        # row = 2
        # for i in nfirst_col:
        #     count = first_col.count(i)  # 计算元素的重复个数，比如测试 ：3
        #     uprange = row + count - 1  # 合并范围后的上行数
        #     sheet.write_merge(row, uprange, 0, 0, i,
        #                       self.set_style(vi=True))  # 合并单元格写入内容 top_row, bottom_row, left_column, right_column
        #     row = uprange + 1  # 从下一行开始写入
        #
        # # 获取content子列表第二个元素，循环写入excel第2列到最后开始的数据
        # for row in range(contentRow):
        #     for col in range(1, len(content[row])):
        #         sheet.write(row + 2, col, content[row][col])

        path = Config.UPLOADS_XML_DEST
        file_path = os.path.join(path, '%s.xls' % filename)
        workbook.save(file_path)