import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from urllib.error import URLError

# Author: Jiao Ma

@st.cache_data
def load_data():
  data = pd.read_excel('cancer patient data sets.xlsx')
  return data

# Load data at start  
df = load_data()

# Function definitions
def intro():
  st.header('Welcome to the Cancer Patient Analysis App')
  st.write('This is the home page of the app.')
  st.snow()
  
  #Author:Jin Yan & Xinwen Liu
def query1():
    st.header('Query 1: Impact of external environment ')
    st.sidebar.header('External Factor')

    category_names = ['degree8', 'degree7',
                  'degree6','degree5','degree4','degree3','degree2','degree1']
    results = {
        'Low': [0,0,3.3,3.3,6.6,36.9,36.6,13.2],
        'Medium': [0,0,21.1,3,6.1,18.3,21.1,30.4],
        'High': [5.2,8.2,67.4,0,13.7,0,5.5,0],}
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small')
    #
    page=st.sidebar.radio('Select an external factor',['Air Pollution','OccuPational Hazards'])
    if page == 'Air Pollution':  
        st.write('You Chose Air Pollution')  
        st.title('Air Pollution Data Analysis')  # 设置页面标题 
        st.pyplot(fig)# 显示预先准备好的图表  

    elif page == 'OccuPational Hazards':  
        st.write('You Chose OccuPational Hazards')  
        st.title('OccuPational Hazards Data Analysis')  # 设置页面标题  
        # 在这里添加你为 OccuPational Hazards 准备的图表代码
        #
        category_names = ['degree8', 'degree7',
                        'degree6','degree5','degree4','degree3','degree2','degree1']
        results2 = {
            'Low': [0,7,0,3,23,27,23,17],
            'Medium': [0,18,6,14,11,17,20,14],
            'High': [5,0,5,37,22,31,0,0]

        }
        labels = list(results2.keys())
        data = np.array(list(results2.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.colormaps['RdYlGn'](
            np.linspace(0.15, 0.85, data.shape[1]))

        fig2, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
                                label=colname, color=color)

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='small')
        st.pyplot(fig2)
        #
 

    else:  
        st.write('error')

    
    
    
    

    

# Author: Jiao Ma & Zixin Ye & Zijun Fu 
def query2():

  min_age = int(df['Age'].min())
  max_age = int(df['Age'].max())

  st.header('Query 2: Lifestyle Factors')

  st.sidebar.header('Filters')
  age_range = st.sidebar.slider('Age Range', min_value=min_age, max_value=max_age, value=[min_age,max_age])
  gender = st.sidebar.radio('Gender', df['Gender'].unique())

  df_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) & (df['Gender'] == gender)]

  cols = ['Smoking', 'Alcohol use', 'Passive Smoker', 'Balanced Diet', 'Obesity','Weight Loss']
  selected_cols = st.multiselect('Select lifestyle factors', cols, default=cols)

  g = sns.PairGrid(df_filtered[selected_cols])
  g.map(plt.scatter)
  st.pyplot(g)

  st.markdown("**Observations:**")
  if 'Smoking' in selected_cols:
      st.write("- Over 60% patients are smokers or passive smokers")
  if 'Alcohol use' in selected_cols:
      st.write("- Majority of patients do not consume alcohol")
  if 'Balanced Diet' in selected_cols:
      st.write("- Most patients do not have a balanced diet")
  if 'Obesity' in selected_cols:
      st.write("- About 30% patients are obese")
  if 'Weight Loss' in selected_cols:
      st.write("- Lung cancer has little to do with weight loss")
     
      
  with st.expander("See data"):
      st.dataframe(df_filtered[selected_cols])

# Author: Xinyue Yv & Xinyv Song    
def query3():
   
    st.title('Query 3: The Impact of Underlying Diseases on Cancer ')
    st.write(
    """Underlying diseases, also known as comorbidities, can affect cancer significantly. The information below shows different Underlying diseases' effect on cancer."""
)
  
    @st.cache_data 
    def load_data():
        df = pd.read_excel('114514(2).xlsx')

        return df.set_index("Level")

    df = load_data()
    try:
        df = load_data()      
        # streamlit的滑动条(年龄数据)
        ages = df['Age'].unique().tolist()

    # 滑动条, 最大值、最小值、区间值
        age_selection = st.slider('Age:',
                            min_value=min(ages),
                            max_value=max(ages),
                            value=(min(ages), max(ages)))
    
  
        level = st.multiselect(
            "Choose level", list(df.index.unique()), ["Low"]
    )

    # 根据选择过滤数据
        mask = (df['Age'].between(*age_selection)) & (df['Age'])
        number_of_result = df[mask].shape[0]

        if not level:
            st.error("Please select at least one option.")
        else:
            data = df.loc[mask].loc[level]
            st.write("### Level of Cancer", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "level of cancer", "value": "level of underlying diseases"}
        )
    
            data=pd.read_excel("114514(2).xlsx")
            list1=data.columns.tolist()
            list1.pop(0)
            list1.pop(-1)
            x=st.selectbox('',list1)
            data=data[['Level',x]]
            d_tg=data.groupby('Level')
            s=sns.catplot(x='Level',y=x,kind='box',data=data)
            st.pyplot(s)
          
    except URLError as e:
        st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
            % e.reason)


# Author: Jiao Ma
# Navigation
st.sidebar.title('Navigation')
selected_page = st.sidebar.radio('Select a page:', ['Introduction', 'Query 1', 'Query 2', 'Query 3'])

# Page router 
if selected_page == 'Introduction':
    intro()
elif selected_page == 'Query 1':
    query1()
elif selected_page == 'Query 2':
    query2()  
elif selected_page == 'Query 3':
    query3()
