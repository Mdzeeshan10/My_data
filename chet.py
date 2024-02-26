# Function to convert select query into seletable XPATS
import json

def get_select_jsonPath(select_query):
    mapping_arr=[  {
            "source": {
                "path": "$['d']['__next']"
            },
            "sink": {
                "name": "__next"
            }
        },]
    select_attrs=select_query.split(",")
    for select_attr in select_attrs:
        select_attr=select_attr.strip()
        if select_attr.strip().startswith('to_'):
            select_expand_attrs=select_attr.split("/")
            expand_json_path=""
            # for select_expand_attr in select_expand_attrs:
            for index in range(len(select_expand_attrs)-1):
                expand_json_path=f"{expand_json_path}['{select_expand_attrs[index]}']['results'][0]"
            expand_json_string=f"{expand_json_path}['{select_expand_attrs[index+1]}']"
            mapping_arr.append({"source":{"path":expand_json_string},"sink":{"name":"_".join(select_expand_attrs),"type":"String"}})
        else:
            mapping_arr.append({"source":{"path":f"['{select_attr}']"},"sink":{"name":select_attr,"type":"String"}})
           
    mapping_json={
        "type": "TabularTranslator",
        "mappings": mapping_arr,
        "collectionReference": "$['d']['results']",
        "mapComplexValuesToString": False
    }
    print('done')
    return mapping_json
 

 


def create_json_file(select_list, json_file_name):
    mapping_out=get_select_jsonPath(select_list)
    
    with open(f'{json_file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(mapping_out, f, ensure_ascii=False, indent=4)

    return f"all Success Create json file {json_file_name}.json"



if __name__ == "__main__":

    select_list="BusinessPartner,BusinessPartnerGrouping,OrganizationBPName1,OrganizationBPName2,OrganizationBPName3,OrganizationBPName4,to_BusinessPartnerAddress/CareOfName,to_BusinessPartnerAddress/CityName,to_BusinessPartnerAddress/Country,to_BusinessPartnerAddress/PostalCode,to_BusinessPartnerAddress/Region,to_BusinessPartnerAddress/StreetName,to_BusinessPartnerAddress/StreetPrefixName,to_BusinessPartnerAddress/AdditionalStreetPrefixName,to_Customer/Customer,to_Customer/to_CustomerSalesArea/CustomerGroup,to_Customer/to_CustomerSalesArea/PriceListType,to_Customer/to_CustomerSalesArea/SalesOffice,to_Customer/to_CustomerSalesArea/SalesDistrict,to_Customer/to_CustomerSalesArea/CustomerAccountAssignmentGroup,to_Customer/to_CustomerSalesArea/IncotermsClassification,to_Customer/to_CustomerSalesArea/to_PartnerFunction/BPCustomerNumber,to_Customer/to_CustomerSalesArea/SalesOrganization,to_Customer/to_CustomerSalesArea/to_PartnerFunction/SalesOrganization,to_Customer/to_CustomerSalesArea/to_PartnerFunction/PartnerFunction"
    print(create_json_file(select_list, "myjson"))


from flask import Flask, session, g, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user
from your_module import User  # import your User class

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user)
            g.user = user  # store the user object in g
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    user = g.get('user', None)  # get the user object from g
    if user is not None:
        # use the user object here
        pass
    return render_template('home.html')
