
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import OrderedDict

def data_standardize(df,row,col,line,period,value,axis_col=None):
    #standardize data
    df=df.rename(columns={row:'row',
                     col:'col',
                     line:'line',
                     value:'value',
                     period:'period'})

    if axis_col in df.columns and axis_col:
        
            df=df.rename(columns={axis_col:'axis_col'})
            df=df[['row','col','line','period','value','axis_col']]
    else:
        
        df=df[['row','col','line','period','value']]
        
    # per_dict={'PQ0':'Y0','PQ4':'Y1','PQ8':'Y2','PQ12':'Y3'}
    # df['Period']=df['Period'].map(per_dict).fillna(df['Period'])
    return df


def get_lower_upper(data,padding=0.1):
    
    min_value = data['value'].min()
    max_value = data['value'].max()
    
    return min_value * (1-padding),max_value * (1+padding)

def copy_sheet(source_ws, target_wb, new_title):
    """
    Create a new sheet in the target workbook by copying the source worksheet using openpyxl's copy_worksheet.
    
    Parameters:
    - source_ws: The source worksheet to copy.
    - target_wb: The target workbook where the new sheet will be created.
    - new_title: The title of the new sheet.
    
    Returns:
    - The newly created worksheet.
    """
    # Ensure the source worksheet is in a workbook
    if not source_ws.parent:
        raise ValueError("Source worksheet must belong to a workbook.")

    # Since copy_worksheet requires the source worksheet to be in the target workbook,
    # we need to temporarily add it if it's not already there.
    source_wb = source_ws.parent
    if source_wb != target_wb:
        # Create a temporary sheet in the target workbook by copying manually
        temp_ws = target_wb.create_sheet(title="temp")
        for row in source_ws.iter_rows():
            for cell in row:
                new_cell = temp_ws[cell.coordinate]
                new_cell.value = cell.value
                if cell.has_style:
                    new_cell.font = copy(cell.font)
                    new_cell.border = copy(cell.border)
                    new_cell.fill = copy(cell.fill)
                    new_cell.number_format = copy(cell.number_format)
                    new_cell.protection = copy(cell.protection)
                    new_cell.alignment = copy(cell.alignment)
        # Now use copy_worksheet within the same workbook
        target_ws = target_wb.copy_worksheet(temp_ws)
        # Remove the temporary sheet
        target_wb.remove(temp_ws)
    else:
        # If the source worksheet is already in the target workbook, directly use copy_worksheet
        target_ws = target_wb.copy_worksheet(source_ws)

    # Set the new title for the copied worksheet
    target_ws.title = new_title

    return target_ws


from copy import copy

def copy_sheet(source_ws, target_wb, new_title):
    # Create a new sheet in the target workbook
    target_ws = target_wb.create_sheet(title=new_title)

    # --- Copy cell values and styles ---
    for row in source_ws.iter_rows():
        for cell in row:
            new_cell = target_ws[cell.coordinate]
            new_cell.value = cell.value

            if cell.has_style:
                new_cell.font = copy(cell.font)
                new_cell.border = copy(cell.border)
                new_cell.fill = copy(cell.fill)
                new_cell.number_format = copy(cell.number_format)
                new_cell.protection = copy(cell.protection)
                new_cell.alignment = copy(cell.alignment)

    # --- Copy column widths ---
    for col_letter, dim in source_ws.column_dimensions.items():
        target_ws.column_dimensions[col_letter].width = dim.width

    # --- Copy row heights ---
    for row_num, dim in source_ws.row_dimensions.items():
        target_ws.row_dimensions[row_num].height = dim.height

    # --- Copy conditional formatting ---
    for cell_range, rule_list in source_ws.conditional_formatting._cf_rules.items():
        for rule in rule_list:
            copied_rule = copy(rule)
            target_ws.conditional_formatting.add(cell_range, copied_rule)

    # --- Update formula references (optional, depends on your utils) ---
    for row in target_ws.iter_rows():
        for cell in row:
            if cell.data_type == "f":  # formula
                cell.value = utils.update_formula(
                    cell.value,
                    old_sheet_name=source_ws.title,
                    new_sheet_name=new_title
                )

    return target_ws


Sub ExportDataAndAnalysis()

    Dim ws As Worksheet
    Dim wbSource As Workbook
    Dim wbData As Workbook
    Dim wbAnalysis As Workbook
    Dim analysisSheet As Worksheet
    Dim sheetName As String
    
    Set wbSource = ThisWorkbook

    ' === 1. Export all sheets except "summary" and "analysis" ===
    Set wbData = Workbooks.Add(xlWBATWorksheet)
    
    ' Remove the default sheet
    Application.DisplayAlerts = False
    wbData.Sheets(1).Delete
    Application.DisplayAlerts = True

    For Each ws In wbSource.Sheets
        sheetName = LCase(ws.Name)
        If sheetName <> "summary" And sheetName <> "analysis" Then
            ws.Copy After:=wbData.Sheets(wbData.Sheets.Count)
        End If
    Next ws

    ' Save DataOnly.xlsx
    wbData.SaveAs Filename:=wbSource.Path & "\DataOnly.xlsx", FileFormat:=xlOpenXMLWorkbook
    wbData.Close SaveChanges:=False

    ' === 2. Export "analysis" sheet with local formulas ===
    Set wbAnalysis = Workbooks.Add(xlWBATWorksheet)

    Application.DisplayAlerts = False
    wbAnalysis.Sheets(1).Delete
    Application.DisplayAlerts = True

    wbSource.Sheets("analysis").Copy After:=wbAnalysis.Sheets(wbAnalysis.Sheets.Count)

    ' Now remove external references in formulas
    Set analysisSheet = wbAnalysis.Sheets(wbAnalysis.Sheets.Count)
    
    Dim cell As Range
    For Each cell In analysisSheet.UsedRange
        If cell.HasFormula Then
            cell.Formula = Replace(cell.Formula, "[" & wbSource.Name & "]", "")
        End If
    Next cell

    ' Save AnalysisOnly.xlsx
    wbAnalysis.SaveAs Filename:=wbSource.Path & "\AnalysisOnly.xlsx", FileFormat:=xlOpenXMLWorkbook
    wbAnalysis.Close SaveChanges:=False

    MsgBox "Export complete!"

End Sub


