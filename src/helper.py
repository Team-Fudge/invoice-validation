from datetime import datetime
def compile_report(test_result,
                     wellformedness = False, 
                     syntax = False, 
                     peppol = False, 
                     schema = False, 
                     report = {
                        "title": "Invoice Validation Report",
                        "date": "",
                        "wellformedness_tested": False,
                        "wellformedness_test_result": None,
                        "syntax_tested": False,
                        "syntax_test_result": None,
                        "peppol_tested": False,
                        "peppol_test_results":None,
                        "schema_tested": False,
                        "schema_test_result": None,
                    }):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    report["date"] = dt_string
    if syntax:
        report["syntax_tested"] = True
        report["syntax_test_result"] = test_result
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = None 
        return report
    if peppol:
        report["peppol_tested"] = True
        report["peppol_test_result"] = test_result
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = None 
        return report
    if schema:
        report["schema_tested"] = True
        report["schema_test_result"] = test_result
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = None 
        return report
    if wellformedness:
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = test_result
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = None 
        return report
    else:
        return
        