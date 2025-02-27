import streamlit as stlib
import pandas as panda
import os
from io import BytesIO

# Set Our Apps 
stlib.set_page_config(
    page_title="Data Sweeper",
    layout="wide"
)
page_display_data : dict[str:any] = {
    "title":"Data Sweeper",
    "first_text":"""It can transform files across CSV and Excel Formats with built-in
     data cleaning and visualization""",
     "fileUploadText":"Upload Your CSV or Excel File Here!"
}
stlib.title(page_display_data["title"])
stlib.write(page_display_data["first_text"])
uploaded_files = stlib.file_uploader(
    page_display_data["fileUploadText"], 
    type=['csv','xlsx'],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext : str = os.path.splitext(file.name)[-1].lower()

        if file_ext==".csv":
            df = panda.read_csv(file)
        elif file_ext==".xlsx":
            df = panda.read_excel(file)
        else:
            stlib.error(f"Unsupported File Extension {file_ext}")
        continue
    # Displaying files information
    stlib.write("File Name: ",file.name)
    stlib.write("File Size: ",round(file.size/1024,2),"MB")
    # Displaying 5 rows of data frame
    stlib.write("5 rows of data frame")
    stlib.dataframe(df.head())
    stlib.subheader("Data Cleaning Options")
    if stlib.checkbox(f"Clean your data for {file.name}"):
        col1,col2 = stlib.columns(2)
        with col1:
            if stlib.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                stlib.write("Duplicates Removed")

        with col2:
            if stlib.button(f"Fill Missing Values of {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                stlib.write(f"Missing Values of {file.name} have been filled!") 
        # Enabling Users to Choose Specific Columns to keep or convert
        stlib.subheader("Select Columns to Convert")
        columns = stlib.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        if stlib.button(f"Show Updated {file.name}"):
            stlib.dataframe(df)
        # Create Some Visualizations 
        stlib.subheader("Data Visualization for")
        if stlib.checkbox(f"Show Data Visualization for {file.name}"):
            stlib.bar_chart(df.select_dtypes(include="number").iloc[:,:2])
        
        # Convert the file
        stlib.header("Conversion Options")
        conversion_type = stlib.radio(f"Convert {file.name} to: ",["CSV","Excel"],key=file.name)
        if stlib.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type =="CSV":
                df.to_csv(buffer,index = False)
                new_file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            elif conversion_type =="Excel":
               df.to_excel(buffer,index=False)
               new_file_name = file.name.replace(file_ext,".xlsx")
               mime_type = "application/vnd.ms-excel"
            buffer.seek(0)

            # Download File
            stlib.download_button(
                file_name=new_file_name,
                mime=mime_type,
                data=buffer,
                label=f"Downlad {file.name} as {conversion_type}"
            )