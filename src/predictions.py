import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import seaborn as sns
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from itertools import product
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn import metrics



#Function that will predict the euribor rate for the upcoming 12 months using ARIMA model
def euribor_predict():
    df_euribor = pd.read_csv('../data/final_data/idealista_euribor_monthly_until_june_2023.csv', encoding='utf-8-sig')
    # Make sure the "date" column is of type datetime
    df_euribor['Fecha'] = pd.to_datetime(df_euribor['Fecha'])
    df_euribor.set_index('Fecha', inplace=True)
    df_euribor.sort_index(inplace=True)
    
    # Fit the ARIMA model
    model = ARIMA(df_euribor['Valor'], order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast the future 12 months
    forecast = model_fit.forecast(steps=12)
    forecast_dates = pd.date_range(start=df_euribor.index[-1], periods=13, freq='M')[1:]  # Generate 12 upcoming months
    forecast_df = pd.DataFrame({'Fecha': forecast_dates, 'Valor': forecast})
    forecast_df.set_index('Fecha', inplace=True)

    #Combining the euribor df with the forecast into a new one
    new_df = pd.concat([df_euribor, forecast_df])
    new_df = new_df.rename(columns = {'index':'Fecha'})
    new_df.reset_index(inplace=True)
    new_df['Year'] = new_df['Fecha'].dt.year 
    new_df['Month'] = new_df['Fecha'].dt.month 
    new_df.rename(columns={'Fecha':'Date', 'Valor':'Euribor'},inplace=True)
    new_df.drop(columns=['Año','Mes'], inplace=True)
    #Saving the predicted df into a new csv file
    new_df.to_csv('../models/idealista_euribor_monthly_predicted.csv', encoding='utf-8-sig', index=False)
    print('Predicted df saved into new csv file')
    return model_fit.summary()

#Function that will predict the m2 price by neightborhood from ayuntamiento csv using Linear Regression Model
def ayuntamiento_predict():
    df_ayu = pd.read_csv(f'../data/final_data/ayuntamiento_scrape_with_BarcelonaCiutat_Barris_melt.csv', encoding='utf-8-sig')
    #Adding mean price for neightborhoods that did not have information or was 0
    df_ayu["Price"] = df_ayu.groupby(["Barrios", "Year"])["Price_m2"].transform(lambda x: x.fillna(x.mean()))
    # Step 1: Calculate average prices
    average_prices = df_ayu.groupby("Barrios")["Price_m2"].mean()

    # Step 2: Create a new column "Precio" with replaced values
    df_ayu["Precio"] = df_ayu["Price_m2"].copy()  # Create a copy of "Price_m2" column

    for index, row in df_ayu.iterrows():
        if row["Precio"] == 0:
            barrio = row["Barrios"]
            average_price = average_prices[barrio]
            df_ayu.loc[index, "Precio"] = average_price
    df_ayu_model = df_ayu.drop(columns=['Price', 'Price_m2'])
    encoded_df_1 = pd.get_dummies(df_ayu_model, columns=['Barrios'], dtype="int")
    # Create a scaler instance
    scaler = MinMaxScaler()

    # Scale the "Year" column
    encoded_df_1["Year"] = scaler.fit_transform(encoded_df_1[["Year"]])
    # Usiung the model LinearRegression since it gave me a RMSE, error: 361.3633090643075 and r2: 0.9339224374755266
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Generate future years for prediction -> taking the last year from the DataFrame and adding 3 years

    future_years = range(encoded_df_1["Year"].max() + 1, encoded_df_1["Year"].max() + 4)  # Next 3 years
    barrios = df_ayu_model["Barrios"].unique()  # Unique "Barrios" values

    # Create a prediction dataset with combinations of "Barrios" and future years
    prediction_data = pd.DataFrame(list(product(barrios, future_years)), columns=["Barrios", "Year"])

    # Perform one-hot encoding on "Barrios" column
    encoded_data = pd.get_dummies(prediction_data, columns=["Barrios"])

    # Make predictions
    predictions = model.predict(encoded_data)

    # Combine "Barrios", "Year", and "Precio" into a single dataframe
    predictions_df = pd.DataFrame({"Barrios": prediction_data["Barrios"],
                                "Year": prediction_data["Year"],
                                "Precio": predictions})
    # Concatenate the original DataFrame with predictions_df
    pred_df = pd.concat([df_ayu_model, predictions_df], ignore_index=True)

    # Sort the concatenated data by "Barrio" and "Year"
    pred_df = pred_df.sort_values(by=["Barrios", "Year"], ascending=[True, True])

    # Reset the index
    pred_df = pred_df.reset_index(drop=True)

    # Change the datatype of "Precio" column to float with two decimal places
    pred_df["Precio"] = pred_df["Precio"].round(2).astype(float)

    # Rename the "Precio" column to "Price_m2"
    pred_df = pred_df.rename(columns={"Precio": "Price_m2"})

    # Saving the predictions into csv file
    pred_df.to_csv('../models/ayuntamiento_scrape_with_BarcelonaCiutat_Barris_predicted.csv', encoding='utf-8-sig', index=False)
    #Saving the model into sav file for future usage
    filename = 'ayuntamiento_final_model.sav'
    joblib.dump(model, filename)
    print('Prediction succcessfully created and saved into sav and csv file')
    return

#Function that will predict the m2 price by neightborhood from habitaclia csv using GradientBoostingRegressor Model
def habitaclia_predict(scrape_date):
    date=scrape_date
    #Opening the file into df
    df_hab = pd.read_csv(f'../data/final_data/habitaclia_bcn_all_data_combined_{date}_with_districts.csv', encoding='utf-8-sig')
    #Droping the columns not needed
    df_hab.drop(columns=['ID', 'Address', 'City', 'Neightbourhood', 'Links', 'Description','Date_Scraped', 'District', 'Price_€'], inplace=True)
    
    #Filtering the dataframe to have Price_m2 bigger than 1000 and lower than 10000 to avoid outliters in the model
    df_new = df_hab[(df_hab['Price_m2'] > 1000) & (df_hab['Price_m2'] < 10000)]

    #Encoding columns
    scaler = StandardScaler()
    min_max_scaler = MinMaxScaler()
    df_new = pd.get_dummies(df_new, columns=['nom_barri', 'Property_type'], dtype="int")
    df_new["Rooms"] = scaler.fit_transform(df_new["Rooms"].values.reshape(-1, 1))
    df_new["Bathrooms"] = scaler.fit_transform(df_new["Bathrooms"].values.reshape(-1, 1))
    df_new["Size_m2"] = min_max_scaler.fit_transform(df_new["Size_m2"].values.reshape(-1, 1))

    models = GradientBoostingRegressor(n_estimators=6000)

    #Splitting data

    X = df_new.drop("Price_m2", axis=1)
    y = df_new.Price_m2

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    #Fitting the data to the model
    models.fit(X_train, y_train)
    print(models)
    #Predicting with the model into Test data
    y_pred = models.predict(X_test)
    print(f"MAE, error: {metrics.mean_absolute_error(y_test, y_pred)}")
    print(f"MSE, error: {metrics.mean_squared_error(y_test, y_pred)}")
    print(f"RMSE, error: {np.sqrt(metrics.mean_squared_error(y_test, y_pred))}")
    print(f"r2: {metrics.r2_score(y_test, y_pred)}")

    #Saving the model into sav file
    filename = 'habitaclia_final_model.sav'
    joblib.dump(models, filename)
    
    print('Model created and saved into sav file')
    return