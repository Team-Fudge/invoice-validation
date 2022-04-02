from datetime import datetime

import hashlib
import jwt
import secrets
import src

from src.data_store import data_store
from src.error import AccessError, InputError
from src.register import SECRET


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



def valid_user_id(u_id):
    store = data_store.get()
    return any(u['u_id'] == u_id for u in store['users'])

def valid_token(token):
    store = data_store.get()
    sessions = store['sessions']

    try:
        decoded_jwt = jwt.decode(token, src.register.SECRET, algorithms=['HS256']) 
    except Exception:
        print("Could not decode token")
        return False
    except jwt.ExpiredSignatureError as timeout:
        raise AccessError('Unfortunately your user session has expired. Please Log in again!')
    
    u_id = decoded_jwt['u_id']
    s_id = decoded_jwt['s_id']
    

    # Is the user valid?
    if not valid_user_id(u_id):
        print(f"Invalid UID {u_id}")
        return False
    
    # Is the session valid?
    return any(s == s_id for s in sessions)
