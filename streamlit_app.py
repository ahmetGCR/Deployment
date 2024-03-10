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

CentralAir = st.selectbox('Merkezi Klima:', ['Var', 'Yok'])

KitchenQual = st.selectbox('Mutfak Kalitesi:', ['Mükemmel', 'İyi', 'Ortalama', 'Orta', 'Zayıf'])

GrLivArea = st.number_input("Zemin Üstü Yaşam Alanı", 0, 10000)

TotalBsmtSF = st.number_input("Toplam Bodrum Katı Alanı", 0, 10000)

FireplaceQu = st.selectbox('Şömine Kalitesi:', ['Mükemmel', 'İyi', 'Ortalama', 'Orta', 'Zayıf', 'Yok'])

LandContour = st.selectbox('Arazi Durumu:', ['Düz Seviye', 'Yamaçlı', 'Yamaç', 'Alçaklık'])

ExterQual = st.selectbox('Dış Yüzey Kalitesi:', ['Mükemmel', 'İyi', 'Ortalama', 'Orta', 'Zayıf'])

BsmtFinSF1 = st.number_input("Bitmiş Alan", 0, 5000)

GarageType = st.selectbox('Garaj Türü:', ['Birden fazla türde garaj', 'Ev ile bağlantılı', 'Bodrum Katında Garaj', 'Ev İçine Yapılmış', 'Araba Portu', 'Evden ayrı'])

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

df = pd.DataFrame(sample_one, index=[0])

kitchen_qual_mapping = {'Mükemmel': 5, 'İyi': 4, 'Ortalama': 3, 'Orta': 2, 'Zayıf': 1}
df['KitchenQual'] = df['KitchenQual'].map(kitchen_qual_mapping)

fireplace_qu_mapping = {'Mükemmel': 5, 'İyi': 4, 'Ortalama': 3, 'Orta': 2, 'Zayıf': 1, 'Yok': 0}
df['FireplaceQu'] = df['FireplaceQu'].map(fireplace_qu_mapping)

exter_qual_mapping = {'Mükemmel': 5, 'İyi': 4, 'Ortalama': 3, 'Orta': 2, 'Zayıf': 1}
df['ExterQual'] = df['ExterQual'].map(exter_qual_mapping)


central_air_mapping = {'Var': 1, 'Yok': 0}
df['CentralAir'] = df['CentralAir'].map(central_air_mapping)


land_contour_mapping = {'Düz Seviye': 0, 'Yamaçlı': 1, 'Yamaç': 2, 'Alçaklık': 3}
df['LandContour'] = df['LandContour'].map(land_contour_mapping)

garage_type_mapping = {'Birden fazla türde garaj': 0, 'Ev ile bağlantılı': 1, 'Bodrum Katında Garaj': 2, 'Ev İçine Yapılmış': 3, 'Araba Portu': 4, 'Evden ayrı': 5}
df['GarageType'] = df['GarageType'].map(garage_type_mapping)

st.dataframe(df)

model = joblib.load("model.joblib")

if st.button('Tahmin Yap!'):
    tahmin = round(model.predict(df)[0])
    st.write('Evinizin tahmini degeri:',tahmin)





# from sklearn.preprocessing import LabelEncoder
# labelEncoder = ['LandContour','GarageType']
# le_dict = {}
# for column in labelEncoder:
#     le = LabelEncoder()
#     df[column] = le.fit_transform(df[column])
#     le_dict[column] = le

# df = pd.get_dummies(df, drop_first=True,dtype =int, columns=['CentralAir','LandSlope'])


# for col in ['GarageQual','ExterQual','KitchenQual','FireplaceQu']:
#     df[col].replace({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)