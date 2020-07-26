import pandas as pd
import numpy as np
import microdf as mdf
import matplotlib.pyplot as plt
import ipywidgets as widgets
import plotly.express as px
from ipywidgets import interact, interactive, fixed, interact_manual

person_raw = pd.read_csv('https://github.com/ngpsu22/2016-2018-ASEC-/raw/master/cps_00004.csv.gz')

person = person_raw.copy(deep=True)
person.columns = person.columns.str.lower()
person = person.drop(['serial', 'month', 'pernum', 'cpsidp', 'asecwth'], axis=1)
person = person.rename(columns={'asecwt':'weight','statefip': 'state'})

person['state'] = person['state'].astype(str)
person['state'].replace({'1':'Alabama','2':'Alaska', '4': 'Arizona','5':'Arkansas',
                         '6': 'California', '8': 'Colorado', '9': 'Connecticut',
                         '10':'Delaware', '11': 'DC', '12':'Florida',
                         '13': 'Georgia','15':'Hawaii', '16':'Idaho','17':'Illinois',
                         '18':'Indiana', '19':'Iowa','20':'Kansas', '21': 'Kentucky',
                         '22':'Louisiana', '23': 'Maine', '24': 'Maryland',
                         '25':'Massachusetts', '26':'Michigan', '27': 'Minnesota',
                         '28':'Mississippi','29':'Missouri', '30': 'Montana',
                         '31': 'Nebraska', '32':'Nevada', '33': 'New Hampshire',
                         '34': 'New Jersey', '35': 'New Mexico', '36':'New York',
                         '37':'North Carolina', '38':'North Dakota', '39': 'Ohio',
                         '40':'Oklahoma', '41': 'Oregon', '42':'Pennslyvania',
                         '44':'Rhode Island','45':'South Carolina', '46':'South Dakota',
                         '47': 'Tennessee', '48':'Texas','49':'Utah','50':'Vermont',
                         '51':'Virginia', '53':'Washington', '54':'West Virginia',
                         '55':'Wisconsin', '56':'Wyoming'},inplace=True)

person['child'] = person.age < 18
person['adult'] = person.age >= 18
ages = person.groupby(['spmfamunit', 'year'])[['child','adult']].sum()
ages.columns = ['total_children', 'total_adults']
person = person.merge(ages,left_on=['spmfamunit', 'year'], right_index=True)
person['total_people'] = person.total_children + person.total_adults
mdf.add_weighted_metrics(person, ['child', 'adult'], 'weight')
child_pop = person.groupby('state')[['child']].sum()/3

def ca_pov(state, age_group, ca_monthly=0):
  target_persons = person[person.state==state].copy(deep=True)
  total_population = target_persons.weight.sum()
  adult_population = (target_persons.weight * target_persons.adult).sum()
  child_population = (target_persons.weight * target_persons.child).sum()

  if age_group == 'child':
    target_persons = target_persons[target_persons.child]
  if age_group == 'adult':
    target_persons = target_persons[target_persons.adult]


  spending = child_pop/(ca_monthly * 12)
  target_persons['total_ca'] = target_persons.total_children * ca_monthly * 12
  target_persons['new_spm_resources'] = target_persons.spmtotres + target_persons.total_ca
  target_persons['poor'] = target_persons.new_spm_resources < target_persons.spmthresh
  target_pop = (target_persons.weight.sum())
  total_poor = ((target_persons.weight * target_persons.poor).sum())

  return (total_poor/target_pop * 100).round(1)

def pov_row(row):
  return ca_pov(row.state, row.age_group, row.ca_monthly)

summary = mdf.cartesian_product({'state':person.state.unique(),
                       'ca_monthly': np.arange(0,501,100),
                       'age_group': ['child', 'adult', 'all']})

summary['poverty_rate'] = summary.apply(pov_row, axis=1)
summary.to_csv('stateCAsummary.csv')
print('State CA Summary Completed')












