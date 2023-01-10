# -*-coding:utf-8-*-
import os
import shutil

import xlrd
import pandas as pd

def read_excel(xslx_data, tag_path):
    """
    读取xlsx数据，将数据中有sheet的数据切割，有合并单元格的数据和没有合并单元格的数据
    :param xslx_data: xlsx数据文件
    :param tag_path: 切割好的数据
    :return: 切分好的数据
    """
    judge_file(tag_path)
    xlsx_file = xlrd.open_workbook(xslx_data, file_contents=xslx_data.read())

    for sheet_index in range(xlsx_file.nsheets):

        sh = xlsx_file.sheet_by_index(sheet_index)          # sheet索引从0开始
        sh_name = sh.name                                   # sheet名字
        rows_num = sh.nrows                                 # 行数
        cols_num = sh.ncols                                 # 列数
        merged = get_merged_cells(sh)                       # 获取所有的合并单元格

        tag_file = tag_path + '/' + sh_name + '.csv'
        if merged == []:
            pd.read_excel(xslx_data, sh_name, index_col=0).to_csv(tag_file)

        if merged != []:
            data = []
            for r in range(rows_num):
                entity_dict = {}                            # 行数据
                for c in range(cols_num):
                    cell_value = sh.row_values(r)[c]
                    # print(f'第{r}行第{c}列的值：[{sh.row_values(r)[c]}]')
                    if (cell_value is None or cell_value == ''):
                        cell_value = (get_merged_cells_value(sh, merged, r, c))

                    the_key = 'column' + str(c + 1)         # 构建Entity
                    entity_dict[the_key] = cell_value       # 动态设置各属性值
                data.append(entity_dict)
            df = pd.DataFrame(data)
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            df.to_csv(tag_file, index=False)

def judge_file(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        os.makedirs(file_path)
    else:
        os.makedirs(file_path)

def get_merged_cells(sheet):
    """
    获取所有的合并单元格下表信息，格式如下：
    [(4, 5, 2, 4), (5, 6, 2, 4), (1, 4, 3, 4)]
    (4, 5, 2, 4) 的含义为：
        行 从下标4开始，到下标5（不包含）
        列 从下标2开始，到下标4（不包含），为合并单元格
    :param sheet: xlsx中的sheet（名字或者索引）
    :return: 所有的合并单元格坐标
    """
    return sheet.merged_cells


def get_merged_cells_value(sheet, merged, row_index, col_index):
    """
    先判断给定的单元格，是否属于合并单元格；
        如果是合并单元格，就返回合并单元格的内容
        如果不是合并单元格，不处理
    :return: 合并单元格的数据
    """
    for (rlow, rhigh, clow, chigh) in merged:                       # 遍历表格中所有合并单元格位置信息
        if (row_index >= rlow and row_index < rhigh):               # 行坐标判断
            if (col_index >= clow and col_index < chigh):           # 列坐标判断
                cell_value = sheet.cell_value(rlow, clow)           # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
                # print(f'该单元格[{row_index, col_index}]属于合并单元格，值为[{cell_value}]')
                return cell_value
                break                                               # 不符合条件跳出循环，防止覆盖
    return None


# if __name__ == "__main__":
    # path = os.path.abspath(os.path.dirname(__file__))
    # print(path)
    # tag_file = '../static/cache_data'
    #
    # read_excel('enterprise-attack-v11.3.xlsx', tag_file)
