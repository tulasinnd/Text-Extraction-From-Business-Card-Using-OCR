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
    
Advantages

    Time-saving: OCR technology enables the automated extraction of data from business cards, saving time and effort 
    that would otherwise be spent on manual data entry.

    Increased accuracy: OCR technology has the potential to reduce errors and improve accuracy compared to manual data entry.

    Scalability: OCR technology can handle large volumes of business cards, making it an ideal solution for businesses 
    with high volumes of contacts.

    Easy integration: OCR technology can be easily integrated into existing systems and applications, making it a seamless 
    addition to existing workflows.

    Cost-effective: OCR technology can be a cost-effective solution compared to hiring additional staff to handle manual 
    data entry tasks.
    
Limitations

    While the app has been designed to make accurate predictions, occasional incorrect outputs may occur.
    
    This can happen due to various factors such as low-quality input data or unexpected changes in the input data.
    
Note

    The application can extract text in English language only.
    
    It will extract information only from BUSINESS CARDS 
