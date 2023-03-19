import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 
st. set_page_config(layout="wide")
import re
import pandas as pd

#title
st.title(":orange[UNLOCKING DATA FROM BUSINESS CARDS USING OCR]") 
st.write(" ")
col1, col2,col3= st.columns([3,0.5,4.5])
with col1:
    #image uploader
    st.write("## UPLOAD IMAGE")
    image = st.file_uploader(label = "",type=['png','jpg','jpeg'])

@st.cache
def load_model(): 
    reader = ocr.Reader(['en'])#,model_storage_directory='.')
    return reader 

reader = load_model() #load model

if image is not None:
    input_image = Image.open(image) #read image
    with col1:
        #st.write("## YOUR IMAGE")
        st.image(input_image) #display image        
    
    result = reader.readtext(np.array(input_image))
    result_text = [] #empty list for results
    for text in result:
        result_text.append(text[1])
          
    PH=[]
    PHID=[]  
    ADD=set()
    AID=[]
    EMAIL=''
    EID=''
    PIN=''
    PID=''
    WEB=''
    WID=''
    
    for i, string in enumerate(result_text):   
        #st.write(string.lower())     
        
        # TO FIND EMAIL
        if re.search(r'@', string.lower()):
            EMAIL=string.lower()
            EID=i
        
        # TO FIND PINCODE
        match = re.search(r'\d{6,7}', string.lower())
        if match:
            PIN=match.group()
            PID=i
                       
        # TO FIND PHONE NUMBER    
        # match = re.search(r'(?:ph|phone|phno)?(?:[+-]?\d*){7,}', string)
        #match = re.search(r'(?:ph|phone|phno)?\s*(?:[+-]?\d\s*){7,}', string)
        match = re.search(r'(?:ph|phone|phno)?\s*(?:[+-]?\d\s*[\(\)]*){7,}', string)
        if match and len(re.findall(r'\d', string)) > 7:
            PH.append(match.group())
            PHID.append(i)
            
        # TO FIND ADDRESS 
        keywords = ['road', 'floor', ' st ', 'st,', 'street', ' dt ', 'district',
                    'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road',
                   'state','country', 'post','zip','city','zone','mandal','town','rural',
                    'circle','next to','across from','area','building','towers','village',
                    ' ST ',' VA ',' VA,',' EAST ',' WEST ',' NORTH ',' SOUTH ']
        # Define the regular expression pattern to match six or seven continuous digits
        digit_pattern = r'\d{6,7}'
        # Check if the string contains any of the keywords or a sequence of six or seven digits
        if any(keyword in string.lower() for keyword in keywords) or re.search(digit_pattern, string):
            ADD.add(string)
            AID.append(i)
            
        # TO FIND STATE (USING SIMILARITY SCORE)
        states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
          'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
              "United States", "China", "Japan", "Germany", "United Kingdom", "France", "India", 
               "Canada", "Italy", "South Korea", "Russia", "Australia", "Brazil", "Spain", "Mexico", 'USA','UK']

        import Levenshtein
        def string_similarity(s1, s2):
            distance = Levenshtein.distance(s1, s2)
            similarity = 1 - (distance / max(len(s1), len(s2)))
            return similarity * 100
        
        for x in states:
            similarity = string_similarity(x.lower(), string.lower())
            if similarity > 50:
                ADD.add(string)
                AID.append(i)
                
        # WEBSITE URL          
        if re.match(r"(?!.*@)(www|.*com$)", string):
            WEB=string.lower()
            WID=i 
    with col3: 
        # DISPLAY ALL THE ELEMENTS OF BUSINESS CARD 
        st.write("## EXTRACTED TEXT")
        st.write('##### :red[WEBSITE URL: ] '+ str(WEB))
        st.write('##### :red[EMAIL: ] '+ str(EMAIL)) 
        st.write('##### :red[PIN CODE: ] '+ str(PIN)) 
        ph_str = ' '.join([str(elem) for elem in PH])
        st.write('##### :red[PHONE NUMBER(S): ] '+ph_str)
        add_str = ' '.join([str(elem) for elem in ADD])
        st.write('##### :red[ADDRESS: ] ', add_str)

        IDS= [EID,PID,WID]
        IDS.extend(AID)
        IDS.extend(PHID)
#         st.write(IDS)
        oth=''                               
        fin=[]                        
        for i, string in enumerate(result_text):
            if i not in IDS:
                if len(string) >= 4 and ',' not in string and '.' not in string and 'www.' not in string:
                    if not re.match("^[0-9]{0,3}$", string) and not re.match("^[^a-zA-Z0-9]+$", string):
                        numbers = re.findall('\d+', string)
                        if len(numbers) == 0 or all(len(num) < 3 for num in numbers) and not any(num in string for num in ['0','1','2','3','4','5','6','7','8','9']*3):
                            fin.append(string)
        st.write('##### :red[CARD HOLDER & COMPANY DETAILS: ] ')
        for i in fin:
            st.write('##### '+i)
            
        # DATABASE CODE
        
        website=str(WEB)
        email=str(EMAIL)
        pincode=str(PIN)
        phoneno=ph_str
        address=add_str
        det_str = ' '.join([str(elem) for elem in fin])
        details=det_str
        with open(image, 'rb') as file:
            photo = file.read()

        data = (website, email,pincode , phoneno, address, details, photo)


        import base64
        import pymysql
        import streamlit as st
        from PIL import Image
        import io

        # Connect to the database
        cnx = pymysql.connect(
            host='phonepedatabase.cw0dknqm0t6h.us-east-1.rds.amazonaws.com',
            user='admin',
            password='12345phone',
            database="PhonepeDB"
        )

        # Create the business_cards table with additional columns
        cursor = cnx.cursor()
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS business_cards (
        #         id INT AUTO_INCREMENT PRIMARY KEY,
        #         website_url VARCHAR(255),
        #         email VARCHAR(255),
        #         pin_code VARCHAR(10),
        #         phone_numbers VARCHAR(255),
        #         address VARCHAR(255),
        #         card_holder_details VARCHAR(255),
        #         businesscard_photo MEDIUMBLOB
        #     )
        # """)

        if st.button('UPLOAD BUSINESS CARD',key='biz'):

            # Insert the image into the business_cards table
            # with open(r'C:\Users\91939\OneDrive\Desktop\OCR_P7\DATASET\10.jpg', 'rb') as file:
            #     photo = file.read()

            data = (website, email,pincode , phoneno, address, details, photo)
            sql = "INSERT INTO business_cards (website_url, email, pin_code, phone_numbers, address, card_holder_details, businesscard_photo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            cnx.commit()

        # DISPLAY ID AS BUTTONS CODE 
        # ========================================

        # Retrieve all the ids from the business_cards table
        cursor.execute("SELECT id FROM business_cards")
        rows = cursor.fetchall()

        # Display the ids as buttons
        for row in rows:
            button_label = f"SHOW BUSINESS CARD WITH ID: {row[0]}"
            if st.button(button_label):
                # If the button is clicked, display the corresponding row
                cursor.execute(f"SELECT * FROM business_cards WHERE id={row[0]}")
                row = cursor.fetchone()
                website_url = row[1]
                email = row[2]
                pin_code = row[3]
                phone_numbers = row[4]
                address = row[5]
                card_holder_details = row[6]
                photo = row[7]

                # Display the details of the business card
                st.write(f"# Business Card for {card_holder_details}")
                st.write(f"Website: {website_url}")
                st.write(f"Email: {email}")
                st.write(f"PIN Code: {pin_code}")
                st.write(f"Phone Numbers: {phone_numbers}")
                st.write(f"Address: {address}")
                image = Image.open(io.BytesIO(photo))
                st.image(image, caption="Business Card", use_column_width=True)



        

