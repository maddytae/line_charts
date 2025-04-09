Sub SplitWorkbook()
    Dim wbOriginal As Workbook
    Dim wbOtherTabs As Workbook
    Dim wbAnalysis As Workbook
    Dim ws As Worksheet
    Dim filePath As String
    Dim formulaRange As Range
    
    ' Set the original workbook
    Set wbOriginal = ThisWorkbook
    
    ' Define the file path for saving (modify as needed)
    filePath = wbOriginal.Path & "\"
    
    ' Step 1: Create a new workbook for all tabs except Summary and Analysis
    Set wbOtherTabs = Workbooks.Add
    For Each ws In wbOriginal.Worksheets
        If ws.Name <> "Summary" And ws.Name <> "Analysis" Then
            ws.Copy Before:=wbOtherTabs.Sheets(1)
            ' Delete the default Sheet1 that comes with a new workbook (if it's still there)
            If wbOtherTabs.Sheets.Count > 1 Then
                Application.DisplayAlerts = False
                wbOtherTabs.Sheets(wbOtherTabs.Sheets.Count).Delete
                Application.DisplayAlerts = True
            End If
        End If
    Next ws
    
    ' Save the new workbook with other tabs
    wbOtherTabs.SaveAs filePath & "OtherTabs.xlsx"
    wbOtherTabs.Close SaveChanges:=False
    
    ' Step 2: Create a new workbook for the Analysis tab
    Set wbAnalysis = Workbooks.Add
    wbOriginal.Sheets("Analysis").Copy Before:=wbAnalysis.Sheets(1)
    
    ' Delete the default Sheet1 in the new Analysis workbook
    Application.DisplayAlerts = False
    wbAnalysis.Sheets(wbAnalysis.Sheets.Count).Delete
    Application.DisplayAlerts = True
    
    ' Adjust formulas in the Analysis tab to remove external references
    With wbAnalysis.Sheets("Analysis")
        On Error Resume Next ' In case no formulas are found
        Set formulaRange = .Cells.SpecialCells(xlCellTypeFormulas)
        On Error GoTo 0
        If Not formulaRange Is Nothing Then
            formulaRange.Replace What:="[" & wbOriginal.Name & "]", Replacement:="", LookAt:=xlPart
        End If
    End With
    
    ' Save the Analysis workbook
    wbAnalysis.SaveAs filePath & "AnalysisLocal.xlsx"
    wbAnalysis.Close SaveChanges:=False
    
    MsgBox "Files created successfully!" & vbNewLine & _
           "1. OtherTabs.xlsx" & vbNewLine & _
           "2. AnalysisLocal.xlsx", vbInformation
End Sub
