import streamlit as st
import streamlit.components.v1 as com
import pandas as pd
import plotly.express as px 

# toDO :
 # add all("الكل") option for selecboxes
 # add more statistical discripions 


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

st.subheader("عدد الطلاب والمدارس بناءا على القيم المختارة")
# this will devide the screen into blocks like in Bootstrap grid system
col1, col2, col3, col4 = st.columns(4)
with st.container():
  with col1:
    loc = st.selectbox("إختر المنطقة الإدارية :", loc_lst)
    year = st.selectbox("إختر السنة :", year_lst)
  with col2:
    school_sex = st.selectbox("إختر جنس المدرسة", school_sex_lst)
    school_system = st.selectbox("إختر نظام الدراسة", school_system_lst)
  with col3:
    grade = st.selectbox("إختر المرحلة الدراسية", grades_lst)
    study_type = st.selectbox("إختر نوع السلطة", study_type_lst)
  with col4:
    school_type = st.selectbox("إختر نوع الدراسة", school_type_lst)



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
st.write(pd.DataFrame({'عدد الطلاب الكلي':[stds_count], "عدد الطلاب السعوديين":[sa_stds_count], 'عدد الطلاب الغير سعوديين':[nonsa_stds_count],'عدد المدارس':[schools_count]}))

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
    schools_count.append(data.school_type[data['year'] == year].count())
df.insert(0,"السنوات", year_lst)
df.insert(0, "مجموع الطلاب والطالبات", stds_count)
df.insert(0, "عدد المدارس", schools_count)
df.insert(0, "الطلاب", ml_stds_count)
df.insert(0, "الطالبات", fm_stds_count)

"## توزيع الطلاب والطالبات على السنوات لكل جنس"
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
"-------"
"## عدد المدارس لكل منطقة حسب السنة"


# loc = st.selectbox("المنطقة", loc_lst)

df = pd.DataFrame()
for location in loc_lst:
  schools_per_year = list()
  for year in year_lst:
    schools_per_year.append(len(data.school_type[(data['location'] == location) & (data['year'] == year)]))
  df.insert(0, str(location), schools_per_year)
df.insert(0, 'السنة', year_lst)
st.write(df)
st.write(px.line(df, x=df['السنة'], y=[*df.columns]))