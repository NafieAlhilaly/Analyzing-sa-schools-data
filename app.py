import streamlit as st
import streamlit.components.v1 as com
import pandas as pd
import plotly.express as px 

# toDO :
 # add all("الكل") option for selecboxes
 # seperate students count to be male students cont and female students count over years
 # more statistical discripions 


"# نظرة تحليلية على بيانات المدارس  في السعودية من سنة 2014 إلى 2021"
"[مصدر البيانات](https://data.gov.sa/Data/tl/dataset/2014-2021)"

data = pd.read_excel("./data/data.xlsx")

with st.expander(label="عينات عشوائية من جدول البيانات"):
  st.write(data.sample(8))
with st.expander(label="معلومات إحصائية عن جدول البيانات"):
  st.write(data.describe())

# translating Arabic columns names to English
trans_cols_names = ["year", "year_hijri", "location", "edu_administration", "edu_office",
                    "school_type",
                    "grade",
                    "study_type",
                    "sex",
                    "school_system",
                    "classis",
                    "students_count",
                    "saudi_students_count",
                    "new_students",
                    "new_saudi_students",
                    "techers_count",
                    "saudi_teachers_count",
                    "administrators_count",
                    "saudi_administrators_count",
                    "servats_count",
                    "workers_count"]

"نظرا لكون أسماء الأعمدة باللغة العربية قد تحدث بعض الإشكالات ائناء معالجتها"
"سنقوم بتغيير اسماء الأعمدة للغة الإنقليزية"

# renaming table columns with English ranslations
with st.expander(label="أسماء الأعمدة بعد التغيير"):
  for index, col in enumerate(data.columns):
      st.write("{} --> {}".format(col, trans_cols_names[index]))
      data.rename(columns={str(col):trans_cols_names[index]}, inplace=True)
st.write("الجدول بعد تغيير اسماء الأعمدة")
st.write(data.sample(8))

"""
---------------------------
"""

loc_lst = list(data['location'].unique())
# loc_lst.append('الكل') its not yet working proberly

year_lst = list(data['year'].unique())
# year_lst.append('الكل')

study_type_lst = list(data['study_type'].unique())
# study_type_lst.append("الكل")

school_sex_lst = list(data["sex"].unique())
# school_sex_lst.append('الكل')

school_system_lst = list(data["school_system"].unique())
# school_system_lst.append('الكل')

school_type_lst = list(data["school_type"].unique())
# school_type_lst.append('الكل')

grades_lst = list(data["grade"].unique())
# grades_lst.append('الكل')

st.subheader("عدد الطلاب والمدارس بناءا على القيم المختار")
# this will devide the screen into blocks like in Bootstrap grid system
# here its 4 block/columns
col1, col2, col3, col4 = st.columns(4)
with st.container():
  with col1:
    loc = st.selectbox("إختر المنطقة الإدارية :", loc_lst)
  with col2:
    year = st.selectbox("إختر السنة :", year_lst)
  with col3:
    study_type = st.selectbox("إختر نوع السلطة", study_type_lst)
  with col4:
    school_sex = st.selectbox("إختر جنس المدرسة", school_sex_lst)

col5, col6, col7 = st.columns(3)
with st.container():
  with col5:
    school_system = st.selectbox("إختر نظام الدراسة", school_system_lst)
  with col6:
    school_type = st.selectbox("إختر نوع الدراسة", school_type_lst)
  with col7:
    grade = st.selectbox("إختر المرحلة الدراسية", grades_lst)


  filtered_data = data[(data['location'] == loc )&
                      (data['year'] == year)&
                      (data['study_type'] == study_type)&
                      (data["sex"] == school_sex)&
                      (data["school_system"] == school_system)&
                      (data["school_type"] == school_type)&
                      (data["grade"] == grade)]

  schools_count = filtered_data['location'].count()
  stds_count = sum(filtered_data["students_count"])
  sa_stds_count = sum(filtered_data['saudi_students_count'])
  nonsa_stds_count = stds_count - sa_stds_count

  com.html(
  """
  <!doctype html>
  <html lang="en">
    <head>
      <!-- Required meta tags -->
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <!-- Bootstrap CSS -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
      <!-- jQuery library -->
      <script src="js/jquery.min.js"></script>
      
      <!-- jsPDF-->
      <script src="https://unpkg.com/jspdf@latest/dist/jspdf.umd.min.js"></script>
    </head>
    <body>
      <!-- Optional JavaScript; choose one of the two! -->
      <!-- Option 1: Bootstrap Bundle with Popper -->
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
      <!-- Option 2: Separate Popper and Bootstrap JS -->
      <!--
      <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
      -->
          <div class="card mt-2">
            <h5 class="align-self-center mb-0">جدول يوضح عدد الطلاب وعدد المدارس بناءا على القيم المعطاه</h5>
            <div class="m-2">
              <table class="table table-bordered mb-0">
                  <thead>
                    <tr class="table-active">
                      <th scope="col">عدد الطلاب الكلي</th>
                      <th scope="col">عدد الطلاب السعوديين</th>
                      <th scope="col">عدد الطلاب الغير سعوديين</th>
                      <th scope="col">عدد المدارس</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                    </tr>
                  </tbody>
                </table>
          </body>
  </html>

  """.format(stds_count, sa_stds_count, nonsa_stds_count, schools_count))

"--------------"
stds_count = list()
ml_stds_count = list()
fm_stds_count = list()
schools_count = list()
df = pd.DataFrame()
for year in data['year'].unique():
    stds_count.append(sum(data.students_count[data['year'] == year]))
    ml_stds_count.append(sum(data.students_count[(data['year'] == year) & (data['sex'] == "بنين")]))
    fm_stds_count.append(sum(data.students_count[(data['year'] == year) & (data['sex'] == "بنات")]))
    schools_count.append(data.students_count[data['year'] == year].count())
df.insert(0,"السنوات", year_lst)
df.insert(0, "عدد الطلاب", stds_count)
df.insert(0, "عدد المدارس", schools_count)
df.insert(0, "الطلاب", ml_stds_count)
df.insert(0, "الطالبات", fm_stds_count)


"## توزيع الطلاب على السنوات لكل جنس"
st.write(df)
col1, col2 = st.columns(2)

com.html("""
    <!DOCTYPE html>
    <html lang="en">
      <head>
          <!-- Required meta tags -->
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">

          <!-- Bootstrap CSS -->
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

      </head>
      <body>
        <div class="card">
          <div class="card-body text-end">
            مجموع عدد الطلاب {}, تشكل الإناث منه نسبة %{} وعددهم {}, بينما يشكل الذكور نسبة %{} وعددهم {}
          <div/>
        </div>
      </body>
    </html>
    """.format(sum(stds_count), 
    round(sum(fm_stds_count)/sum(stds_count)*100, 2),
    sum(fm_stds_count),
    round(sum(ml_stds_count)/sum(stds_count)*100, 2),
    sum(ml_stds_count))
    )
st.write(px.line(df, x=df['السنوات'], y=['الطلاب','الطالبات']))
