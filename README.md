# Text-Extraction-From-Business-Card-Using-OCR
This code is an OCR application that extracts text from images uploaded by users, using the EasyOCR library. 
The extracted text is then processed to extract information such as email, phone number, pin code, address, 
and website URL, and displayed on a Streamlit web app interface.

Features

    Extracts Website URL, Email, Pin Code, Phone Number(s), and Address from the uploaded image.
    Displays the uploaded image along with the extracted text.
    
Installation

    Clone the repository using the following command:

    git clone https://github.com/shubham5351/OCR-for-Text-Extraction.git

    Navigate to the directory using the following command:

    cd OCR-for-Text-Extraction

    Install the required libraries using the following command:

    pip install -r requirements.txt

    Run the application using the following command:

    streamlit run app.py

Usage

    Once the application is running, upload an image using the “Upload Image” button.
    
    The application will extract the text from the image and display it in the “Extracted Text” section.
    
    The extracted text will include the Website URL, Email, Pin Code, Phone Number(s), and Address.
    
    Note: The application can extract text in English language only.
