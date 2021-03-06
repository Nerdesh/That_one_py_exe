import os
import time
from pathlib import Path
import csv
import pandas as pd

path_ExcelSOURCE = 'xlsx/source/'
path_ExcelTARGET = 'xlsx/target/'
folder1 = os.listdir(path_ExcelSOURCE)  # folder containing your files
folder2 = os.listdir(path_ExcelTARGET)
path_report = '/xlsx/CompareResults/'

html_path = os.getcwd() + path_report
html_path = html_path.replace("\\", "/")
print(html_path)


def excel_diff(PATH_TARGET, PATH_SOURCE, value_TARGET, value_SOURCE):
    df_TARGET = pd.read_csv(PATH_TARGET).fillna(0)
    print(df_TARGET.columns)
    len_target = len(df_TARGET.columns)
    print(len_target)
    df_TARGET = df_TARGET.sort_values([value_TARGET], ascending=['True'])
    df_SOURCE = pd.read_csv(PATH_SOURCE).fillna(0)
    df_SOURCE = df_SOURCE.sort_values([value_SOURCE], ascending=['True'])
    print(df_SOURCE.columns)
    len_source = len(df_SOURCE.columns)
    print(len_source)
    df_Diff = df_TARGET.copy()

    for item1 in folder1:
        for item2 in folder2:
            if (item1 == item2):
                for row in range(df_Diff.shape[0]):
                    for col in range(df_Diff.shape[1]):
                        try:
                            value_TARGET = df_TARGET.iloc[row, col]
                            value_SOURCE = df_SOURCE.iloc[row, col]

                            if value_TARGET == value_SOURCE:
                                df_Diff.iloc[row, col] = df_SOURCE.iloc[row, col]
                            else:
                                df_Diff.iloc[row, col] = ('{}-->{}').format(value_TARGET, value_SOURCE)

                        except:
                            df_Diff.iloc[row, col] = ('{}-->{}').format(value_TARGET, 'NaN')

                        fname = '{} vs {}.csv'.format(PATH_TARGET.stem, PATH_SOURCE.stem)
                        writer = df_SOURCE.to_csv(fname)

                        # writer = pd.ExcelWriter(fname, engine = 'xlsxwriter')

                        df_Diff.to_csv(writer, header='DIFF', index=False)

                        #  df_SOURCE.to_excel (writer , sheet_name = path_SOURCE.stem, index = False)
                        # df_TARGET.to_excel (writer , sheet_name = path_TARGET.stem, index = False)

                        workbook = writer.book
                        worksheet = writer.sheets['DIFF']
                        # worksheet.hide_gridlines(2)

                        # data format

                        date_fmt = workbook.add_format({'align': 'center', 'num_format': 'yyyy-mm-dd'})
                        center_fmt = workbook.add_format({'align': 'center'})
                        number_fmt = workbook.add_format({'align': 'center', 'num_format': '#, ##0.00'})
                        cur_fmt = workbook.add_format({'align': 'center', 'num_format': '$#, ##0.00'})
                        perc_fmt = workbook.add_format({'align': 'center', 'num_format': '0%'})
                        grey_fmt = workbook.add_format({'font_color': '#E0E0E0'})
                        highlight_fmt = workbook.add_format({'font_color': '#FF0000'})

                        worksheet.conditional_format('A1:ZZ1000',
                                                     {'type': 'text',
                                                      'criteria': 'containing',
                                                      'value': '-->',
                                                      'format': highlight_fmt})

                        writer.save()
                        print('Done')


def excel_diff():
    print("##################### Execution Started #######################")
    start_time = time.time()

    HtmlHeaderStartingString = '<html>' + '\n' + '<head>' + '\n' + '<h1 style = "background-color:powderblue; text-align:center;font-size:30px;">' + '\n' + '<img src = "maveric.png" align = "right" alt = "Italian Trulli" width = "100" height = "35" >EXCEL FILE COMPARISON DASHBOARD</h1>' + '\n' + '<link rel="stylesheet" type="text/css" href="mystyle.css">' + '\n' + '</head>' + '\n' + '<div class="floatLeft" >' + '\n'
    HtmlEndString = '</div>'
    TableStartString = '\n' + '<table align="center"  CELLSPACING=0 CELLPADDING=5 border="1">' + '</br>'
    TableColumnHeaderString = '\n' + '<tr>' + '<th width="30%">' + 'SOURCE_VS_TARGET_DIFF_REPORT' + '</th>' + '<th>' + 'OLDVERSION_VS_NEWVERSION FILESIZE' + '</th>' + '<th>' + 'EXECUTION TIME' + '</th>' + '<th>' + 'STATUS' + '</th>' + '<th>' + 'TOTAL DIFFERENCES' + '</th>' + '</tr>' + '</br>'

    with open("OverallReportExcel.html", 'w') as _file:

        _file.write(HtmlHeaderStartingString)
        _file.write(HtmlEndString)
        _file.write(TableStartString)
        _file.write(TableColumnHeaderString)

    for item1 in folder1:
        for item2 in folder2:
            if (item1 == item2):
                path_SOURCE = path_ExcelSOURCE + item1
                # df_OLD = pd.read_excel(path_OLD1).fillna(0)
                df_SOURCE = pd.read_csv(path_SOURCE).fillna(0)
                print(df_SOURCE.dtypes)

                df_SOURCE = df_SOURCE.applymap(lambda x: x.strip() if isinstance(x, str) else x)

                df_SOURCE.rename(columns={df_SOURCE.columns[0]: 'Primary_Key'}, inplace=True)
                value_SOURCE = 'Primary_Key'
                df_SOURCE = df_SOURCE.sort_values([value_SOURCE], ascending=['True'])
                print(path_SOURCE)
                path_TARGET = path_ExcelTARGET + item2
                df_TARGET = pd.read_csv(path_TARGET).fillna(0)
                df_TARGET = df_TARGET.applymap(lambda x: x.strip() if isinstance(x, str) else x)

                df_TARGET.rename(columns={df_TARGET.columns[0]: "Primary_Key"}, inplace=True)
                value_TARGET = 'Primary_Key'
                print("----")
                print(df_TARGET.columns)
                df_TARGET = df_TARGET.sort_values([value_TARGET], ascending=['True'])
                print(df_TARGET.dtypes)
                df_Diff = df_TARGET.copy()
                print("Started Comparing")
                bMisMatch = False
                diffcount = 0

                df_change = pd.DataFrame(columns=['row', 'column', 'change'])
                df_selected = []
                rowNum = 0
                for row in range(df_Diff.shape[0]):
                    for col in range(df_Diff.shape[1]):
                        try:
                            value_TARGET = df_TARGET.iloc[row, col]
                            value_SOURCE = df_SOURCE.iloc[row, col]
                            # print('Do3ne')
                            if value_TARGET == value_SOURCE:
                                df_Diff.iloc[row, col] = df_SOURCE.iloc[row, col]
                            else:
                                df_Diff.iloc[row, col] = ('{}-->{}').format(value_SOURCE, value_TARGET)
                                chge = df_Diff.iloc[row, col] = ('{}-->{}').format(value_SOURCE, value_TARGET)
                                rowNum = rowNum + 1
                                df_change.loc[rowNum, 'row'] = row
                                df_change.loc[rowNum, 'column'] = col
                                df_change.loc[rowNum, 'change'] = chge
                                df_selected.append(row)
                                bMisMatch = True
                                diffcount = diffcount + 1
                        except:
                            df_Diff.iloc[row, col] = ('{}-->{}').format(value_TARGET, 'NaN')

                    # fname = '{} vs {}.xlsx'.format(path_TARGET.stem, path_SOURCE.stem)
                if (bMisMatch == True):
                    status = 'Differences'
                else:
                    status = 'Matched'
                print(status)

                fname = '{}vs{}.CSV'.format(os.path.splitext(item1)[0] + '_Source',
                                            os.path.splitext(item2)[0] + '_Target')

                df_selected = list(set(df_selected))
                df_filtered = df_Diff.iloc[df_selected]

                writer = df_filtered.to_csv("xlsx/CompareResults/" + fname)
                print('final output')
                print(df_filtered)

                df_filtered.to_csv(writer, header='DIFF', index=True)
                # print(df_Diff.to_csv(writer, header='DIFF', index=True))

                # writer = pd.ExcelWriter("xls/CompareResults/" + fname, engine='xlsxwriter')
                # result.to_excel(writer, sheet_name='DIFF', index=True)
                df_SOURCE.to_csv(writer, header='Source', index=True)
                df_TARGET.to_csv(writer, header='Target', index=True)

                # workbook = writer.book
                # worksheet = writer.sheets['DIFF']
                # worksheet.hide_gridlines(2)

                # data format

                # date_fmt = workbook.add_format({'align': 'center', 'num_format': 'yyyy-mm-dd'})
                # center_fmt = workbook.add_format({'align': 'center'})
                # number_fmt = workbook.add_format({'align': 'center', 'num_format': '#, ##0.00'})
                # cur_fmt = workbook.add_format({'align': 'center', 'num_format': '$#, ##0.00'})
                # perc_fmt = workbook.add_format({'align': 'center', 'num_format': '0%'})
                # grey_fmt = workbook.add_format({'font_color': '#E0E0E0'})
                # highlight_fmt = workbook.add_format({'font_color': '#FF0000'})

                # worksheet.conditional_format('A1:ZZ1000',{'type': 'text','criteria': 'containing','value': '-->','format': highlight_fmt})

                # worksheet.conditional_format('A1:ZZ1000',
                #                                        {'type': 'text',
                #                                         'criteria':'containing',
                #                                         'value' :'-->',
                #                                         'format':grey_fmt})

                # writer.save()
                print('Done')

                size1 = os.path.getsize(path_SOURCE)
                size2 = os.path.getsize(path_TARGET)

                end_time1 = time.time()

                TimeTaken = (end_time1 - start_time)

                # total = 1

                DataString = '\n' + '<tr>' + '<td>' + '<a' + ' href = ' + html_path + \
                             os.path.splitext(item1)[0] + "_Source" + "vs" + os.path.splitext(item2)[
                                 0] + "_Target" + ".csv" + '>' + os.path.splitext(item1)[
                                 0] + ".csv"'</a>'  '</td>' + '<td>' + str(
                    size1 / 1000) + ' vs ' + str(
                    size2 / 1000) + ' KB' + '</td>' + '<td>' + str(
                    round(TimeTaken, 4)) + ' sec' + '</td>' + '<td>' + status + '</td>' + '<td>' + str(
                    diffcount) + '</td>''</tr>' + '</br>'
                # print(DataString)
                with open("OverallReportExcel.html", 'a') as _file:

                    _file.write(DataString)
            # print(DataString)
            end_time = time.time()
            TimeTaken = (end_time - start_time)
            # print('Time Taken For Execution:' + str(round(TimeTaken, 4)))
            # print("################ Execution Completed in " + str(TimeTaken) + " ###############")


def main():
    # path_TARGET = Path('C:/Users/O24240/Desktop/DWH/xlsx/target/IRES_Customer_HK.xlsx')
    # path_SOURCE = Path('C:/Users/O24240/Desktop/DWH/xlsx/source/IRES_Customer_HK.xlsx')

    # excel_diff(path_TARGET, path_SOURCE,'cif_client_id','CIF')
    excel_diff()


if __name__ == '__main__':
    main()
