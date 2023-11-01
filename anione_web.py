import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import os
import time
from PIL import Image
from datetime import datetime
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/CHhI6tn.jpg[/img]");
             background-attachment: fixed;
             background-size: cover
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
st.set_page_config(page_title='ani-1',layout="wide")
st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #0099ff !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#FFFFFF;
}
div.stButton > button:hover {
    background-color: #0099ff;
    color:#ffffff;
    }
</style>""", unsafe_allow_html=True)
add_bg_from_url()
df_gong=pd.read_csv('df_gong')
df_sa=pd.read_csv('df_sa')
df_gong2=df_gong.sort_values('구조일자')
df_sa2=df_sa.sort_values('구조일자')
st.sidebar.header('잃어버린 동물 정보')
date_list=sorted(list(set(list(df_gong['구조일자'].values)+list(df_sa['구조일자'].values))))
date_input=st.sidebar.selectbox('실종 일자를 선택하세요',date_list)
plc1_list=sorted(list(set(list(df_gong['구조장소'].values)+list(df_sa['구조장소'].values))))
plc_dict={}
for i in plc1_list:
    il=i.split('-')
    if il[0] not in plc_dict.keys():
        plc_dict[il[0]]=[il[1]]
    else:
        plc_dict[il[0]].append(il[1])
plc1_input=st.sidebar.selectbox('대단위 지역을 선택하세요',plc_dict.keys())
plc2_input=st.sidebar.multiselect('시군구를 선택하세요 (복수 선택 가능)',plc_dict[plc1_input])

animal_type=st.sidebar.selectbox('동물 종류를 선택하세요', ['강아지','고양이','기타축종'])
df_type1=df_gong[['축종','품종']]
df_type2=df_sa[['축종','품종']]
df_type3=pd.concat([df_type1,df_type2])
dce={'강아지':[],'고양이':[],'기타축종':[]}
for i,j in df_type3.iterrows():
    if j['축종']=='강아지':
        dce['강아지'].append(j['품종'])
    elif j['축종']=='고양이':
        dce['고양이'].append(j['품종'])
    else:
        dce['기타축종'].append(j['품종'])
dce['강아지']=sorted(list(set(dce['강아지'])))
dce['고양이']=sorted(list(set(dce['고양이'])))
dce['기타축종']=sorted(list(set(dce['기타축종'])))
next_type=st.sidebar.selectbox('품종을 선택하세요',dce[animal_type])
gender=st.sidebar.selectbox('성별을 선택하세요',['수컷','암컷','미상'])
button=st.sidebar.button('검색')
st.session_state['wait']='조금만 기다려주세요. 데이터를 가져오는 중입니다.'

if button==True:
    st.subheader('보호소 또는 동물병원')
    col1,col2,col3=st.columns(3)
    col_num=1
    date_input1=datetime.strptime(date_input,"%Y-%m-%d")
    abc=False
    for i,j in df_gong2.iterrows():
        rescue_date=datetime.strptime(j['구조일자'],"%Y-%m-%d")
        if date_input1<=rescue_date and j['구조장소'][:2]==plc1_input and j['구조장소'][3:] in plc2_input and j['축종']==animal_type and j['품종']==next_type and j['성별']==gender:
            print(j['사진'])
            abc=True
            if col_num==1:
                with col1:
                    if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                    else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                    imgs=imgs.resize((176,154))
                    st.image(imgs)
                    st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                    st.write(j[['구조일자','구조장소','품종','성별']])
                col_num+=1
            elif col_num==2:
                with col2:
                    if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                    else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                    imgs=imgs.resize((176,154))
                    st.image(imgs)
                    st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                    st.write(j[['구조일자','구조장소','품종','성별']])
                col_num+=1
            else:
                with col3:
                    if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                    else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                    imgs=imgs.resize((176,154))
                    st.image(imgs)
                    st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                    st.write(j[['구조일자','구조장소','품종','성별']])
                col_num=1
    if abc==False:
        with col2:
            st.write('올라온 공고가 없습니다')
    st.write('')
    st.write('')
    st.write('')
    st.subheader('목격 또는 임시보호')
    abc=False
    first=[]
    second=[]
    third=[]
    last=[]
    for i,j in df_sa2.iterrows():
        rescue_date=datetime.strptime(j['구조일자'],"%Y-%m-%d")
        if date_input1<=rescue_date and j['구조장소'][:2]==plc1_input and j['구조장소'][3:] in plc2_input and j['축종']==animal_type:
            if j['품종']==next_type and j['성별']==gender:
                first.append([j['구조일자'],j['구조장소'],j['품종'],j['성별'],j['사진'],j['웹페이지주소']])
            elif j['품종']==next_type and j['성별']=='미상':
                second.append([j['구조일자'],j['구조장소'],j['품종'],j['성별'],j['사진'],j['웹페이지주소']])
            elif ((j['품종']=='기타') or (j['품종']=='미상')) and j['성별']==gender:
                third.append([j['구조일자'],j['구조장소'],j['품종'],j['성별'],j['사진'],j['웹페이지주소']]) 
            elif ((j['품종']=='기타') or (j['품종']=='미상')) and j['성별']=='미상':
                last.append([j['구조일자'],j['구조장소'],j['품종'],j['성별'],j['사진'],j['웹페이지주소']])
    sa_df=pd.DataFrame({"구조일자":[],"구조장소":[],"품종":[],"성별":[],"사진":[],"웹페이지주소":[]})
    for i in first:
        sa_df.loc[len(sa_df)]=i
    for i in second:
        sa_df.loc[len(sa_df)]=i
    for i in third:
        sa_df.loc[len(sa_df)]=i
    for i in last:
        sa_df.loc[len(sa_df)]=i
    col4,col5,col6=st.columns(3)
    col_num=1
    for i,j in sa_df.iterrows():
        abc=True
        if col_num==1:
            with col4:
                if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                imgs=imgs.resize((176,154))
                st.image(imgs)
                st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                st.write(j[['구조일자','구조장소','품종','성별']])
            col_num+=1
        elif col_num==2:
            with col5:
                if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                imgs=imgs.resize((176,154))
                st.image(imgs)
                st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                st.write(j[['구조일자','구조장소','품종','성별']])
            col_num+=1
        else:
            with col6:
                if j['사진']=='No image':
                        imgs=Image.open("no_image.jpg")
                else:
                        url =j['사진']
                        os.system("curl " + '--globoff '+url + " > test.jpg")
                        imgs = Image.open("test.jpg")
                imgs=imgs.resize((176,154))
                st.image(imgs)
                st.write('[해당 웹페이지로 이동]('+j['웹페이지주소']+')')
                st.write(j[['구조일자','구조장소','품종','성별']])
            col_num=1
    print(first)
    print(second)
    print(third)
    print(last)
    if abc==False:
        with col5:
            st.write('올라온 공고가 없습니다')