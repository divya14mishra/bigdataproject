from import_lib import *


def covid_viz_graphs():
    try:
        # Basic Modification of Data
        covid = pd.read_csv('data/covid.csv')
        covid.drop(["SNo"], 1, inplace=True)
        covid["ObservationDate"] = pd.to_datetime(covid["ObservationDate"])

        grouped_country = covid.groupby(["Country/Region", "ObservationDate"]).agg(
            {"Confirmed": 'sum', "Recovered": 'sum', "Deaths": 'sum'})
        grouped_country["Active Cases"] = grouped_country["Confirmed"] - grouped_country["Recovered"]-grouped_country["Deaths"]
        grouped_country["log_confirmed"] = np.log(grouped_country["Confirmed"])
        grouped_country["log_active"] = np.log(grouped_country["Active Cases"])

        datewise = covid.groupby(["ObservationDate"]).agg(
            {"Confirmed": 'sum', "Recovered": 'sum', "Deaths": 'sum'})
        datewise["Days Since"] = datewise.index-datewise.index.min()

        # ######## Plotting Graph 1 ################
        fig1 = px.bar(
            x=datewise.index, y=datewise["Confirmed"]-datewise["Recovered"]-datewise["Deaths"])
        fig1.update_layout(title="Distribution of Number of Active Cases",
                           xaxis_title="Date", yaxis_title="Number of Cases",paper_bgcolor="lightblue",font_color='blue')
        fig1.write_image("./static/all_visualizations/fig1.jpg")

        ######## Plotting Graph 2 ################
        fig2 = px.bar(x=datewise.index,
                      y=datewise["Recovered"]+datewise["Deaths"])
        fig2.update_layout(title="Distribution of Number of Closed Cases",
                           xaxis_title="Date", yaxis_title="Number of Cases",paper_bgcolor="lightblue",font_color='blue')
        fig2.write_image("./static/all_visualizations/fig2.jpg")

        ######## Plotting Graph 3 ################
        
        india_data = covid[covid["Country/Region"]=="India"]
        datewise_india = india_data.groupby(["ObservationDate"]).agg({"Confirmed":'sum',"Recovered":'sum',"Deaths":'sum'})
        datewise_india["WeekOfYear"]=datewise_india.index.weekofyear

        week_num=[]
        weekwise_confirmed=[]
        weekwise_recovered=[]
        weekwise_deaths=[]
        w=1
        # print(list(datewise_india["WeekOfYear"].unique()))
        for i in list(datewise_india["WeekOfYear"].unique()):
            weekwise_confirmed.append(datewise_india[datewise_india["WeekOfYear"]==i]["Confirmed"].iloc[-1])
            weekwise_recovered.append(datewise_india[datewise_india["WeekOfYear"]==i]["Recovered"].iloc[-1])
            weekwise_deaths.append(datewise_india[datewise_india["WeekOfYear"]==i]["Deaths"].iloc[-1])
            week_num.append(w)
            w=w+1

        fig3=go.Figure()
        fig3.add_trace(go.Scatter(x=week_num, y=weekwise_confirmed,
                            mode='lines+markers',
                            name='Weekly Growth of Confirmed Cases'))
        fig3.add_trace(go.Scatter(x=week_num, y=weekwise_recovered,
                            mode='lines+markers',
                            name='Weekly Growth of Recovered Cases'))
        fig3.add_trace(go.Scatter(x=week_num, y=weekwise_deaths,
                            mode='lines+markers',
                            name='Weekly Growth of Death Cases'))
        fig3.update_layout(title="Weekly Growth of different types of Cases in India",
                        xaxis_title="Week Number",yaxis_title="Number of Cases",legend=dict(x=0,y=1,traceorder="normal")
                        ,paper_bgcolor="lightblue",font_color='blue')

        fig3.write_image("./static/all_visualizations/fig3.jpg")

        ######## Plotting Graph 4 ################
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=datewise.index, y=datewise["Confirmed"],
                                  mode='lines+markers',
                                  name='Confirmed Cases'))
        fig4.add_trace(go.Scatter(x=datewise.index, y=datewise["Recovered"],
                                  mode='lines+markers',
                                  name='Recovered Cases'))
        fig4.add_trace(go.Scatter(x=datewise.index, y=datewise["Deaths"],
                                  mode='lines+markers',
                                  name='Death Cases'))
        fig4.update_layout(title="Growth of different types of cases",
                           xaxis_title="Date", yaxis_title="Number of Cases", legend=dict(x=0, y=1, traceorder="normal")
                           ,paper_bgcolor="lightblue",font_color='blue')
        fig4.write_image("./static/all_visualizations/fig4.jpg")


        ######## Plotting Graph 5 ################
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=datewise.index, y=datewise["Confirmed"].diff().fillna(0), mode='lines+markers',
                                  name='Confirmed Cases'))
        fig5.add_trace(go.Scatter(x=datewise.index, y=datewise["Recovered"].diff().fillna(0), mode='lines+markers',
                                  name='Recovered Cases'))
        fig5.add_trace(go.Scatter(x=datewise.index, y=datewise["Deaths"].diff().fillna(0), mode='lines+markers',
                                  name='Death Cases'))
        fig5.update_layout(title="Daily increase in different types of Cases",
                           xaxis_title="Date", yaxis_title="Number of Cases", legend=dict(x=0, y=1, traceorder="normal")
                           ,paper_bgcolor="lightblue",font_color='blue')
        fig5.write_image("./static/all_visualizations/fig5.jpg")


        ######## Plotting Graph 6 ################
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=datewise.index, y=datewise["Confirmed"].diff().rolling(window=7).mean(), mode='lines+markers',
                                  name='Confirmed Cases'))
        fig6.add_trace(go.Scatter(x=datewise.index, y=datewise["Recovered"].diff().rolling(window=7).mean(), mode='lines+markers',
                                  name='Recovered Cases'))
        fig6.add_trace(go.Scatter(x=datewise.index, y=datewise["Deaths"].diff().rolling(window=7).mean(), mode='lines+markers',
                                  name='Death Cases'))
        fig6.update_layout(title="7 Days Rolling Mean of Daily Increase of Confirmed, Recovered and Death Cases",
                           xaxis_title="Date", yaxis_title="Number of Cases", legend=dict(x=0, y=1, traceorder="normal")
                           ,paper_bgcolor="lightblue",font_color='blue')
        fig6.write_image("./static/all_visualizations/fig6.jpg")


        ######## Plotting Graph 7 ################
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=datewise.index,
                                  y=(datewise["Confirmed"]-datewise["Recovered"]-datewise["Deaths"])/(
                                      datewise["Confirmed"]-datewise["Recovered"]-datewise["Deaths"]).shift(),
                                  mode='lines',
                                  name='Growth Factor of Active Cases'))
        fig7.add_trace(go.Scatter(x=datewise.index, y=(datewise["Recovered"]+datewise["Deaths"])/(datewise["Recovered"]+datewise["Deaths"]).shift(),
                                  mode='lines',
                                  name='Growth Factor of Closed Cases'))
        fig7.update_layout(title="Datewise Growth Factor of Active and Closed Cases",
                           xaxis_title="Date", yaxis_title="Growth Factor",
                           legend=dict(x=0, y=-0.4, traceorder="normal"),paper_bgcolor="lightblue",font_color='blue')

        fig7.write_image("./static/all_visualizations/fig7.jpg")


        ######## Plotting Graph 8 ################
        fig8 = go.Figure()
        countrywise = covid[covid["ObservationDate"] == covid["ObservationDate"].max()].groupby(
            ["Country/Region"]).agg({"Confirmed": 'sum', "Recovered": 'sum', "Deaths": 'sum'}).sort_values(["Confirmed"], ascending=False)
        countrywise["Mortality"] = (
            countrywise["Deaths"]/countrywise["Confirmed"])*100
        countrywise["Recovery"] = (
            countrywise["Recovered"]/countrywise["Confirmed"])*100

        country_last_24_confirmed = []
        country_last_24_recovered = []
        country_last_24_deaths = []
        for country in countrywise.index:
            country_last_24_confirmed.append(
                (grouped_country.loc[country].iloc[-1]-grouped_country.loc[country].iloc[-2])["Confirmed"])
            country_last_24_recovered.append(
                (grouped_country.loc[country].iloc[-1]-grouped_country.loc[country].iloc[-2])["Recovered"])
            country_last_24_deaths.append(
                (grouped_country.loc[country].iloc[-1]-grouped_country.loc[country].iloc[-2])["Deaths"])

        Last_24_Hours_country = pd.DataFrame(list(zip(countrywise.index, country_last_24_confirmed, country_last_24_recovered, country_last_24_deaths)),
                                             columns=["Country Name", "Last 24 Hours Confirmed", "Last 24 Hours Recovered", "Last 24 Hours Deaths"])

        Top_15_Confirmed_24hr = Last_24_Hours_country.sort_values(
            ["Last 24 Hours Confirmed"],ascending=False).head(15)
        Top_15_Recoverd_24hr = Last_24_Hours_country.sort_values(
            ["Last 24 Hours Recovered"],ascending=False).head(15)
        Top_15_Deaths_24hr = Last_24_Hours_country.sort_values(
            ["Last 24 Hours Deaths"],ascending=False).head(15)
        # print(Top_15_Confirmed_24hr)
        fig8 = px.bar(
            x=Top_15_Confirmed_24hr["Country Name"],y=Top_15_Confirmed_24hr["Last 24 Hours Confirmed"])
        fig8.update_layout(title="Top 15 Countries with Highest Number of Confirmed Cases in Last 24 Hours",
                           xaxis_title="Country Name",yaxis_title="Last 24 Hours Confirmed",
                           paper_bgcolor="lightblue",font_color='blue')
        fig8.write_image("./static/all_visualizations/fig8.jpg")


        ######## Plotting Graph 9 ################
        fig9 = go.Figure()
        fig9 = px.bar(
            x=Top_15_Deaths_24hr["Country Name"], y=Top_15_Confirmed_24hr["Last 24 Hours Deaths"])
        fig9.update_layout(title="Top 15 Countries with Highest Number of Deaths Cases in Last 24 Hours",
                           xaxis_title="Last 24 Hours Confirmed", yaxis_title="Country Name",paper_bgcolor="lightblue",font_color='blue')
        fig9.write_image("./static/all_visualizations/fig9.jpg")


        ####### Plotting Graph 10 ################
        fig10 = go.Figure()
        fig10 = px.bar(
            x=Top_15_Recoverd_24hr["Country Name"], y=Top_15_Confirmed_24hr["Last 24 Hours Recovered"])
        fig10.update_layout(title="Top 15 Countries with Highest Number of Recovered Cases in Last 24 Hours",
                            xaxis_title="Last 24 Hours Confirmed", yaxis_title="Country Name",paper_bgcolor="lightblue",font_color='blue')
        fig10.write_image("./static/all_visualizations/fig10.jpg")


        ######## Plotting Graph 11 ################
        datewise["Mortality Rate"] = (
            datewise["Deaths"]/datewise["Confirmed"])*100
        datewise["Recovery Rate"] = (
            datewise["Recovered"]/datewise["Confirmed"])*100
        datewise["Active Cases"] = datewise["Confirmed"] - \
            datewise["Recovered"]-datewise["Deaths"]
        datewise["Closed Cases"] = datewise["Recovered"]+datewise["Deaths"]

        # print("Average Mortality Rate",datewise["Mortality Rate"].mean())
        # print("Median Mortality Rate",datewise["Mortality Rate"].median())
        # print("Average Recovery Rate",datewise["Recovery Rate"].mean())
        # print("Median Recovery Rate",datewise["Recovery Rate"].median())

        ############## Plotting Mortality and Recovery Rate
        fig11 = make_subplots(rows=2, cols=1,
                              subplot_titles=("Recovery Rate", "Mortatlity Rate"))
        fig11.add_trace(
            go.Scatter(x=datewise.index, y=(
                datewise["Recovered"]/datewise["Confirmed"])*100, name="Recovery Rate"),
            row=1, col=1
        )
        fig11.add_trace(
            go.Scatter(x=datewise.index, y=(
                datewise["Deaths"]/datewise["Confirmed"])*100, name="Mortality Rate"),
            row=2, col=1
        )
        fig11.update_layout(height=1000, legend=dict(
            x=-0.1, y=1.2, traceorder="normal"),paper_bgcolor="lightblue",font_color='blue')
        fig11.update_xaxes(title_text="Date", row=1, col=1)
        fig11.update_yaxes(title_text="Recovery Rate", row=1, col=1)
        fig11.update_xaxes(title_text="Date", row=1, col=2)
        fig11.update_yaxes(title_text="Mortality Rate", row=1, col=2)
        fig11.write_image("./static/all_visualizations/fig11.jpg")
        return 1
    except Exception as e:
        print("Error in covid_viz_graphs", e)
        return 0

# print(covid_viz_graphs())
