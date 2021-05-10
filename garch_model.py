from arch import arch_model
from matplotlib import pyplot
import pandas, os, math

def process(asset):
  df = pandas.read_csv('normalized/{0}'.format(asset), index_col='Date')
  split_date = '2021-02-01'
  train, test = df[:split_date], df[split_date:]

  asset_names = asset.split('.')[0].split('-')
  exchange = asset_names[0]
  ticker = asset_names[1]
  train = list(map(lambda x: x * 10, train[ticker].values.tolist()))
  training_model = arch_model(train, mean='Zero', vol='GARCH', p=1, q=1)
  training_model_fit = training_model.fit(update_freq=0)
  forecast = training_model_fit.forecast(horizon=29, reindex=False)

  test = list(map(lambda x: x * 10, test[ticker].values.tolist()))
  test_model = arch_model(test, mean='Zero', vol='GARCH', p=1, q=1)
  test_model_fit = test_model.fit(update_freq=0)

  forecast_values = list(map(lambda x: math.sqrt(x / 10), forecast.variance.values[-1]))
  test_values = list(map(lambda x: math.sqrt(x / 10), test_model_fit.conditional_volatility))
  pyplot.plot(forecast_values, label="Projected")
  pyplot.plot(test_values, label="Actual")
  pyplot.xlabel("Days")
  pyplot.ylabel("Standard Deviation")
  pyplot.legend()
  pyplot.savefig('models/{0}-{1}.png'.format(exchange, ticker))
  pyplot.close()

for asset in os.listdir('normalized'):
  process(asset)

