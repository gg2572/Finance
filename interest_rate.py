import requests
import zipfile
import StringIO
import pandas as pd

from matplotlib import pyplot as plt
# from matplotlib.text import TextWithDash as text
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import quandl

with open('/Users/ggao/.quandl_api_key', 'r') as input_file:
    quandl.ApiConfig.api_key = input_file.read()

# For instance, if you are searching for the Quandl codes for the End of Day US Stock Prices (EOD) dataset, your API call would be structured as follows:
#
# https://www.quandl.com/api/v3/databases/EOD/codes?api_key=YOURAPIKEY
# This api returns a zipped file containing the dataset and the explanactions
response = requests.get('https://www.quandl.com/api/v3/databases/USTREASURY/codes?api_key={api_key}'.format(api_key=quandl.ApiConfig.api_key), stream=True)

# Get the readable zip file
z = zipfile.ZipFile(StringIO.StringIO(response.content), 'r')

columns = ['dataset', 'comments']
data = pd.DataFrame(columns=columns)
for filename in z.namelist():
    data = pd.concat([data, pd.read_csv(StringIO.StringIO(z.read(filename)), names=columns)])

yield_curve = quandl.get('USTREASURY/YIELD', start_date='1984-05-09', end_date='2018-05-09')

yield_curve['10-2 yield spread'] = yield_curve['10 YR'] - yield_curve['2 YR']


plt.plot_date(yield_curve.index, yield_curve['10-2 yield spread'], 'g-', label='10-2 yield spread', markersize=1)
plt.plot_date(yield_curve.index, yield_curve['2 YR'], 'r-', label='2 YR', markersize=1, linewidth=1)
plt.plot_date(yield_curve.index, yield_curve['10 YR'], 'b-', label='10 YR', markersize=1, linewidth=1)

vlines = {'title': ['Junk Bond Crash in 10/1989', 'Tequila Crisis 12/20/1994', 'Dot-com Bubble Crash 03/11/2000', 'Global Financial Crisis 08/09/2007', 'Today'],
          'date': ['1990-01-01', '1994-12-20', '2000-03-11', '2007-08-09', '2018-05-09']}

for i in range(len(vlines['title'])):
    plt.text(datetime.strptime(vlines['date'][i], '%Y-%m-%d') + timedelta(days=5), plt.gca().axes.get_ylim()[1] / 2, vlines['title'][i], rotation=90, fontsize=6, color='k', verticalalignment='center')
    plt.vlines(x=datetime.strptime(vlines['date'][i], '%Y-%m-%d'), ymin=plt.gca().axes.get_ylim()[0], ymax=plt.gca().axes.get_ylim()[1], color='k', linestyles='dashed', linewidth=0.5)

plt.xlabel('Date')
plt.ylabel('Rate / %')
plt.title('Yield Curve / Spread since 1990')
plt.legend()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))
plt.gca().xaxis.set_tick_params(which='major', labelsize=3)
plt.gcf().autofmt_xdate()
plt.savefig('yield_curve_spread_since_1990.png', format='png', dpi=300)
plt.clf()

