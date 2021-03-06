"""
Created on Tue Sep 29 17:42:01 2020

@author: Ankan Datta
"""

import streamlit as st
import warnings

warnings.filterwarnings("ignore")
# EDA Pkgs
import pandas as pd

# To Hide Warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')
import seaborn as sns

sns.set_style('darkgrid')

STYLE = """
<style>
img {
    max-width: 100%;
}
</style> """


def main():
    """ Common ML Dataset Explorer """
    st.title("Common ML Dataset Explorer")
    st.subheader("Datasets For ML Explorer with Streamlit")

    html_temp = """
	<div style="background-color:tomato;"><p style="color:white;font-size:50px;padding:10px">Streamlit is Awesome</p></div>
	"""
    st.markdown(html_temp, unsafe_allow_html=True)

    def file_selector():
        """Run this function to display the Streamlit app"""
        st.info(__doc__)

        file = st.file_uploader("Upload file", type=["csv", "xlsx"])
        show_file = st.empty()

        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(["csv", "xlsx"]))
            return

        FileType = str(file)[0:8]

        if FileType == "<_io.Str":
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)

        return data

    df = file_selector()
    try:
        df = df.dropna()
        df = df.drop_duplicates()
    except:
        st.write("")

    if st.checkbox("Show Dataset, a pivoted view would be seen"):
        st.dataframe(df.head())

    # Show Columns
    if st.button("Column Names"):
        st.write(pd.DataFrame(df.columns, columns=["Column Names "]))

        # Show Shape
    if st.checkbox("Shape of Dataset"):
        data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"))
        if data_dim == 'Rows':
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim == 'Columns':
            st.text("Number of Columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)

    # Select Columns
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select", all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)

    # Show Values
    if st.button("Value Counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:, -1].value_counts())

    # Show Datatypes
    if st.button("Data Types"):
        st.write(df.dtypes)

    # Show Summary
    if st.checkbox("Summary"):
        st.write(df.describe().T)
        ## Plot and Visualization

        st.subheader("Data Visualization")
        # Correlation
        # Seaborn Plot
    if st.checkbox("Correlation Plot[Seaborn]"):
        st.write(sns.heatmap(df.corr(), annot=True))
        st.pyplot()

    # Pie Chart
    if st.checkbox("Pie Plot"):
        all_columns_names = df.columns.tolist()
        if st.button("Generate Pie Plot"):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
            st.pyplot()

    if st.checkbox("Pairplots"):
        st.write(sns.pairplot(df, size=5))
        st.pyplot()

    # Count Plot
    if st.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
        selected_columns_names = st.multiselect("Select Columns", all_columns_names)
        if st.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:, -1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

        # Customizable Plot
    try:

        st.subheader("Customizable Plot")
        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

        if st.button("Generate Plot"):
            st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

            # Plot By Streamlit
            if type_of_plot == 'area':
                cust_data = df[selected_columns_names]
                st.area_chart(cust_data)

            elif type_of_plot == 'bar':
                cust_data = df[selected_columns_names]
                st.bar_chart(cust_data)

            elif type_of_plot == 'line':
                cust_data = df[selected_columns_names]
                st.line_chart(cust_data)

            # Custom Plot
            elif type_of_plot:
                cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                st.write(cust_plot)
                st.pyplot()

        numeric_columns = df.select_dtypes(["float64", "float32", "int32", "int64"]).columns

        st.sidebar.header("About App")
        st.sidebar.info("A Simple EDA App for Exploring ML Datasets")
        st.sidebar.text("Built with Streamlit")
        st.sidebar.subheader("Scatter-plot setup")
        box1 = st.sidebar.selectbox(label="X axis", options=numeric_columns)
        box2 = st.sidebar.selectbox(label="Y axis", options=numeric_columns)
        sns.jointplot(x=box1, y=box2, data=df, kind="reg", color="red")
        st.pyplot()

        if st.button("Thanks"):
            st.balloons()
    except:
        st.write("Please Enter a File to Proceed")


if __name__ == '__main__':
    main()