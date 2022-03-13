from datetime import date

def compile_report(test_result,
                     wellformedness, 
                     syntax, 
                     peppol, 
                     schema, 
                     report = {
                        "title": "Invoice Validation Report",
                        "date": dt_string,
                        "wellformedness_tested": False,
                        "wellformedness_test_result": None
                        "syntax_tested": False,
                        "syntax_test_result": None
                        "peppol_tested": False,
                        "peppol_test_results":None
                        "schema_tested": False,
                        "schema_test_result": None
                    }):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    if syntax:
        report["syntax_tested"] = True
        report["syntax_test_result"] = test_result
        return report
    if peppol:
        report["peppol_tested"] = True
        report["wellformedness_test_result"] = test_result
        return report
    if schema:
        report["schema_tested"] = True
        report["schema_test_result"] = test_result
        return report
    if wellformedness:
        report["wellformedness_tested"] = True
        report["wellformedness_test_result"] = test_result
        return report
    else:
        return