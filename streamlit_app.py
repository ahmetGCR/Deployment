import streamlit as st
import joblib
import pandas as pd

st.title("Ev Fiyatı Tahmin Uygulaması") 
#st.header("Evinizin Fiyatını Tahmin Edin")
st.image("ev.jpg", width=600)

min_OverallQual = 1
max_OverallQual = 10
OverallQual = st.slider("Genel Kalite Değeri:", min_value=min_OverallQual, max_value=max_OverallQual)

GarageCars = st.selectbox("Garaj Kapasitesi", [0, 1, 2, 3, 4])

CentralAir = st.selectbox('Merkezi Klima:', ['N', 'Y'])

KitchenQual = st.selectbox('Mutfak Kalitesi:', ['Ex', 'Gd', 'TA', 'Fa', 'Po'])

GrLivArea = st.number_input("Zemin Üstü Yaşam Alanı", 0, 10000)

TotalBsmtSF = st.number_input("Toplam Bodrum Katı Alanı", 0, 10000)

FireplaceQu = st.selectbox('Şömine Kalitesi:', ['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA'])

LandContour = st.selectbox('Arazi Durumu:', ['Lvl', 'Bnk', 'HLS', 'Low'])

ExterQual = st.selectbox('Dış Yüzey Kalitesi:', ['Ex', 'Gd', 'TA', 'Fa', 'Po'])

BsmtFinSF1 = st.number_input("Bitmiş Alan", 0, 5000)

GarageType = st.selectbox('Garaj Türü:', ['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd','NA'])

sample_one = {
    "OverallQual": OverallQual,
    "GarageCars": GarageCars,
    "CentralAir": CentralAir,
    "KitchenQual": KitchenQual,
    "GrLivArea": GrLivArea,
    "TotalBsmtSF": TotalBsmtSF,
    "FireplaceQu": FireplaceQu,
    "LandContour": LandContour,
    "ExterQual": ExterQual,
    "BsmtFinSF1": BsmtFinSF1,
    "GarageType": GarageType
}



df_s = pd.DataFrame(sample_one, index=[0])
df_s

# ordinal encoder yükle
from sklearn.preprocessing import OrdinalEncoder
ordinal_columns = joblib.load("ordinal_columns.joblib")
for col in ordinal_columns:
    encoder = joblib.load(f"{col}_encoder.joblib")
    transformed_column = encoder.transform(df_s[[col]])
    df_s[col] = transformed_column


# label encoder yükle
from sklearn.preprocessing import LabelEncoder
label_columns = joblib.load("labelEncoder_columns.joblib")     
for col in label_columns:
    le = joblib.load(f"{col}_encoder.joblib")
    transformed_column = le.transform(df_s[col])
    df_s[col] = transformed_column

get_dummies_columns = joblib.load("dummies_columns.joblib")
df_dummies = pd.get_dummies(df_s, drop_first=True, dtype=int).reindex(columns=get_dummies_columns, fill_value=0)


import pandas as pd
yeni_df = df_s.drop(columns="CentralAir")
yeni_df = pd.concat([yeni_df, df_dummies], axis=1)


model = joblib.load("model.joblib")

pred_price = round(model.predict(yeni_df)[0])
st.write('Evinizin Değeri:', pred_price)

