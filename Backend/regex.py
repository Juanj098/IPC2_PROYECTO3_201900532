import re

regex = r"\d+\/\d+\/\d+"

txt = 'Guatemala, 15/01/2023, 15:23hrs'

x = re.search(regex,txt).group()
print(x)


