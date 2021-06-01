# Covid_Dashboard

Data visualization is the graphical representation of information and data. By using visual elements like charts, graphs, and maps, data visualization tools provide an accessible way to see and understand trends, outliers, and patterns in data.

It is very important to collect good information in order to build these charts. If we don´t gather the proper information, we won´t be able to have useful charts that represent meaningful information.

This repo presents information previously filtered, on graphs you can access and see the different graphs of Covid cases in Mexico during 2020.

This repo is divided into 2 parts. The first part belongs to the data filtering, where you can see the information and create your own JSON files to make your graphs.

The second part belongs to data visualization of the information previously filtered.


## Information Filtering:

In order to be able to filter the information to create graphs, type on your terminal:

```
$ pip install numpy
$ pip install pandas
$ pip install openpyxl
$ pip install djangorestframework
$ pip install django-import-export
$ pip install django-url-filter
```

Go to the `filter.py` file on the `DataFilter` folder. This file allows you to filter the information from the `export_dataframe.xlsx` file that has all the informationo of Covid cases during 2020. For now, the file creates 4 different json files and exports them on the `covid_data` folder. You can check this file and make your own filters.

## Data Visualization:

### Before Starting:

You need to run a local server. 


Open the local server and click on the `Covid_Dashboard` folder. There you will be able to see the visualize the data of the Covid cases in Mexico during 2020.

![image](https://github.com/majohdezo/Covid_Dashboard/blob/main/Gif/Chart1.gif)

![image](https://github.com/majohdezo/Covid_Dashboard/blob/main/Gif/Chart2.gif)

![image](https://github.com/majohdezo/Covid_Dashboard/blob/main/Gif/Chart3.gif)

![image](https://github.com/majohdezo/Covid_Dashboard/blob/main/Gif/Chart4.gif)


## References:
This code was based on this [repo] (https://github.com/gcastillo56/com139-class/tree/master/COVID) 