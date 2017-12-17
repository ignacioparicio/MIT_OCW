# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name:  Ignacio Paricio
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    # Ignacio: Built to test data structure
    def get_raw_data(self):
        return self.rawdata
        
    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""
# Ignacio: Test data structure
# d = Climate('data.csv').get_raw_data()

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for deg in degs:
        models.append(pylab.polyfit(x, y, deg))
    return models
   
# Test generate_models
#print(generate_models(pylab.array([1961, 1962, 1963]), 
#                      pylab.array([-4.4, -5.5, -6.6]),
#                      [1, 2]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    r_squared = 1 - sum((y-estimated) ** 2) / sum((y-pylab.average(y)) ** 2)
    return r_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        degree = len(model) - 1
        
        # Get estimated values according to model
        est_pol = pylab.poly1d(model)
        est = est_pol(x)
     
        pylab.figure()
        # Actual data
        pylab.plot(x, y, marker = '.', linestyle = 'None', markersize = 10)
        # Model
        pylab.plot(x, est, color = 'r')
        title = 'Model degree = ' + str(degree) + '\n' \
                + 'R^2 = ' + str(round(r_squared(y, est),2))
        if degree == 1:
            title += '\n' + 'SE / Slope = ' + \
                      str(round(se_over_slope(x, y, est, model),2))
        pylab.title(title)
        pylab.xlabel('Year')
        pylab.ylabel('Temperature [Celsius]')

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # list_cities_avg is a list of lists; inner lists contain avg city temp by year
    list_cities_avg = []
    
    for city in multi_cities:
        city_temps = [pylab.average(climate.get_yearly_temp(city, year)) \
                     for year in years]
        list_cities_avg.append(city_temps)
                
    # pylab.mean(x, axis = 0) returns the avg of multiple lists by list index   
    cities_avg = pylab.average(list_cities_avg, axis = 0)
    return cities_avg

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg = []
    for i in range(len(y)):
        if i < (window_length - 1):
            moving_avg.append(pylab.average(y[0 : i + 1]))
        else:
            moving_avg.append(pylab.average(y[(i - window_length + 1):i + 1]))
    return moving_avg
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return pylab.sqrt(sum((y - estimated) ** 2) / len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # This is a list that gives, per year, the st.dev of the average of 
    # different daily temperatures in all cities (st.dev of 365 daily avg temps)
    stdev_by_year = []
    for year in years:
        cities_daily_temps = []
        for city in multi_cities:
            city_daily_temps = climate.get_yearly_temp(city, year)
            cities_daily_temps.append(city_daily_temps)
        
        daily_averages = pylab.average(cities_daily_temps, axis = 0)
        stdev_by_year.append(pylab.std(daily_averages, axis = 0, ddof = 0))    
            
    return stdev_by_year
    
def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        degree = len(model) - 1
        
        # Get estimated values according to model
        est_pol = pylab.poly1d(model)
        est = est_pol(x)
            
        pylab.figure()
        # Actual data
        pylab.plot(x, y, marker = '.', linestyle = 'None', markersize = 10)
        # Model
        pylab.plot(x, est, color = 'r')
        title = 'Model degree = ' + str(degree) + '\n' \
                + 'RMSE = ' + str(round(rmse(y, est), 2))
        pylab.title(title)
        pylab.xlabel('Year')
        pylab.ylabel('Temperature [Celsius]')

if __name__ == '__main__':
    
    # Close all pre-open figures on execution
    pylab.close("all")
    
    cl = Climate('data.csv')

    # Part A.4

    # Jan 11 in New York every year
    x = pylab.array([year for year in TRAINING_INTERVAL])
    y = pylab.array([cl.get_daily_temp('NEW YORK', 1, 10, year) \
                     for year in TRAINING_INTERVAL])                   
    models = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, models)
    
    # Average temperature in New York every year
    y = gen_cities_avg(cl, ['NEW YORK'], TRAINING_INTERVAL)           
    models = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, models)   
    
    # Part B
    y = gen_cities_avg(cl, CITIES, TRAINING_INTERVAL)                
    models = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, models)   

    # Part C
    w_length = 5
    y = moving_average(gen_cities_avg(cl, CITIES, TRAINING_INTERVAL), w_length)             
    models = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, models) 

    # Part D.2
    x = pylab.array([year for year in TRAINING_INTERVAL])
    y = moving_average(gen_cities_avg(cl, CITIES, TRAINING_INTERVAL), w_length)
    models = generate_models(x, y, [1, 2, 20])
    evaluate_models_on_training(x, y, models) 
    
    x = pylab.array([year for year in TESTING_INTERVAL])
    y = moving_average(gen_cities_avg(cl, CITIES, TESTING_INTERVAL), w_length)
    evaluate_models_on_testing(x, y, models) 
    
    # Part E
    x = pylab.array([year for year in TRAINING_INTERVAL])
    y = moving_average(gen_std_devs(cl, CITIES, TRAINING_INTERVAL),
                       w_length)
    models = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, models) 
                       
