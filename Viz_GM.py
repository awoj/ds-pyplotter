#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Packages
# in CMD - pip install seaborn
#        - pip install ttkthemes
#        - pip install pyqt5
# in Jupyter Notebook - !pip install ttkthemes

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from  matplotlib.ticker import PercentFormatter
import os
import warnings
warnings.filterwarnings(action='ignore')
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from distutils.util import strtobool
from ttkthemes import ThemedTk
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pathlib
from pandastable import Table, TableModel


# In[4]:


# GUI

#curr_options = ["SINGLEPULSE", "PULSEDDYNAMIC", "PULSED"]
#curr_amps = ["A", "mA"]
ordr = [1,2,3,4,5,6,7,8,9]
t_f = ['False', 'True']
#incs = [1,2,5,10]

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

root = ThemedTk(theme='adapta')
root.title("GUI")

# General Inputs
Label(root, text = "General Inputs", font=("Arial Bold", 12)).grid(row = 0, sticky = W)

Label(root, text = "Directory").grid(row = 1, sticky = W)
Label(root, text = "Filename(s) (Please have same first letters if multiple datasheets)").grid(row = 2, sticky = W)
Label(root, text = "Filetype").grid(row = 3, sticky = W)

# Output Info
Label(root, text = "Output Folder Location (If default - create gm_output folder inside directory)").grid(row = 10, sticky = W)
# Overwrite or no
Label(root, text = "Allow Overwriting Output Files?").grid(row = 11, sticky = W)

# Graph Options
Label(root, text = "Graph Options", font=("Arial Bold", 12)).grid(row = 12, sticky = W)

# What order
#Label(root, text = "Order (Ex: 1=Linear)").grid(row = 16, sticky = W)
# Show points or no
#Label(root, text = "Show Points?").grid(row = 17, sticky = W)
# Export or no as excel worksheet
Label(root, text = "Export as Excel Worksheet?").grid(row = 18, sticky = W)
Label(root, text = "Show Lambertain Graph?").grid(row = 19, sticky = W)
Label(root, text = "Show Fitted Line?").grid(row = 20, sticky = W) # Default == True

# Directory
folder_path = StringVar()
e0 = ttk.Entry(master=root,textvariable=folder_path)
#e0.insert(0, '')
dir_button = ttk.Button(text="Browse", command=browse_button)
# Filename(s)
e1 = ttk.Entry(root)
e1.insert(0, "30MILL-SANAM")
# Filetype
e2 = ttk.Entry(root)
e2.insert(0, ".xlsx")

# Output directory
e9 = ttk.Entry(root)
e9.insert(0, 'gm_output')
# Dropdown menu
e10 = StringVar(root)
e10.set(t_f[0])
e10x = OptionMenu(root,e10,*t_f)

# Dropdown menu
#g5 = StringVar(root)
#g5.set(ordr[2])
#g5x = OptionMenu(root,g5,*ordr)

# Dropdown menu
#g6 = StringVar(root)
#g6.set(t_f[0])
#g6x = OptionMenu(root,g6,*t_f)

# Dropdown menu
g7 = StringVar(root)
g7.set(t_f[0])
g7x = OptionMenu(root,g7,*t_f)

# Dropdown menu
g8 = StringVar(root)
g8.set(t_f[0])
g8x = OptionMenu(root,g8,*t_f)

# Dropdown menu
g9 = StringVar(root)
g9.set(t_f[0])
g9x = OptionMenu(root,g9,*t_f)

e0.grid(row = 1, column = 1)
dir_button.grid(row=1, column=2)
e1.grid(row = 2, column = 1)
e2.grid(row = 3, column = 1)
e9.grid(row = 10, column = 1)
e10x.grid(row = 11, column = 1)

#g5x.grid(row = 16, column = 1)
#g6x.grid(row = 17, column = 1)
g7x.grid(row = 18, column = 1)
g8x.grid(row = 19, column = 1)
g9x.grid(row = 20, column = 1)

def getInput():

    a = e0.get()
    b = e1.get()
    c = e2.get()
    j = e9.get()
    k = e10.get()
    #q = int(g5.get())
    #r = g6.get()
    s = g7.get()
    t = g8.get()
    u = g9.get()
    
    root.destroy()

    global overall
    overall = [a,b,c,j,k,s,t,u]

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
    
ttk.Button(root, text = "Submit",
           command = getInput).grid(sticky = E, row = 50)
mainloop()


# In[5]:


# Kill script if GUI has empty spots

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

if '' in overall:
    Mbox('Error!', 'At least one entry in the GUI is empty - please fix', 0)
    sys.exit() # Kill script


# In[6]:


# Input info
directory = pathlib.Path(overall[0])  # Provide the location of the excel files * Please use forward slashes
name = overall[1]  #*RA* Provide the model a.k.a. everything before the temperature (prob change here)
file_type = overall[2]  # If reading in multiple files - they all have to be the same file type

# Output info
output_f = overall[3]  # <- This is where the folder where you would like to put all the images of the graphs
                     # NOTE: Put the desired location of where the folder is located here
                     # If the file is in the same location as your directory, all you need to do is put the folder name here
                     # * NO backward slashes only forward
# Allow Overwriting or no? - Default=False
over = bool(strtobool(overall[4]))


# In[7]:


# Select the columns you want from the excel spreadsheet

select_cols = ['Filename', 'Number', 'Phi / °', 'Theta / °', 'Integration Time / ms', 'Source current - Currentsource / mA', 'Current - Currentsource / mA',
               'Voltage - Currentsource / V', 'Radiometric / W/m²', 'Photometric / lx', 'x - Color Coordinates',
              'y - Color Coordinates', 'u - Color Coordinates', 'v1976 - Color Coordinates', 'Peak Wavelength / nm', 
              'Centroid Wavelength / nm', 'Dominant Wavelength / nm', 'CRI', 'CRI09 - CRI'] 
               #'Partial luminous flux / lm', 'Partial radiant power / W'

# Add columns here for any calculations
# Calculated columns will be appended to the dataframe
#column_d = ['Voltage  - Currentsource / V', 'x - Color Coordinates', 'y - Color Coordinates', 'Peak Wavelength / nm', 
        #    'Dominant Wavelength / nm', 'Centroid Wavelength / nm'] # Change (-) columns
#column_p = ['Radiometric / W', 'Photometric / lm'] # Relative (%) columns

# Here: rename all selected columns & calculated columns - don't forget calculated columns are added towards the end
# Change columns first then relative columns

#column_rn = ['Serial Number', 'Δ Forward Voltage (Vf)', 'Δ CIEx', 'Δ CIEy', 'Δ Peak Wavelength (λp)', 'Δ Centroid Wavelength (λcen)', 
#             'Δ Dominant Wavelength (λd)', 'Δ CCT / K', 'Δ CRI', 'Δ R 9', 'Δ FWHM', 'Relative Radiant Power', 'Relative Luminous Flux', 'Tj (°C)', 'lf (A)' ]


# 'Last Dark Current (min)', 'Signal Level (counts)', 'Signal Level (%)', 'Scotopic Luminous Flux', 'UVA (W)', 'UVB (W)', 
# 'UVC (W)', 'VIS (W)', 'TRIx', 'TRIy', 'TRIz', 'CIEz', 'CIEu', 'v1960', 'v1976', 'Width (nm)', 'CRI', 'Red Effect (%)', 
# 'Vis Effect (%)', 'CCT',


# In[8]:


# IMPORTANT - OUTPUT
# Select columns here - this is what outputs the graphs
# Add more columns & titles here if necessary

# Renamed name of temperature and current column

y1 = 'x - Color Coordinates'
y2 = 'y - Color Coordinates'
y3 = 'u - Color Coordinates'
y4 = 'v1976 - Color Coordinates'
y5 = 'Peak Wavelength / nm'
y6 = 'Centroid Wavelength / nm'
y7 = 'Dominant Wavelength / nm'
y8 = 'CRI'
y9 = 'CRI09 - CRI'

# Show all of y variables (number of columns that we would like outputs for), only change if removing or adding columns
y_n = [y1,y2,y3,y4,y5,y6,y7,y8,y9]

row_size = 5 # Make sure row and column size can accomodate all the subplots
column_size = 2
ax_n = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1), (4,0)] # the axes for the subplots

# Graph order number - 1 = linear, 2 = quadratic, 3 = cubic, etc.
#ord_num = overall[4]

# Show points or no?
#show_pt = bool(strtobool(overall[5]))

# Export as Excel Worksheet or no?
exp = bool(strtobool(overall[5]))

# Show Lambersian Graph?
lamb = bool(strtobool(overall[6]))

# Show Fitted Line?
fitt = bool(strtobool(overall[7]))


# In[9]:


# Change directory
os.chdir(directory)
pathlib.Path.cwd()


# In[10]:


# Check whether the specified path exists or not
isExist = os.path.exists(output_f)

if not isExist:
  
  # Create output dir if doesn't exist
  os.makedirs(output_f)
  Mbox("Create output dir", "The output directory has been created: " + output_f, 0)


# In[11]:


# Identifies all filenames in the directory

filesnames = os.listdir()
filesnames = [f for f in filesnames if (f.startswith(name) and f.lower().endswith(file_type))]

# Read in excel files as dataframe

# Here we concat similarly named files together - nice for putting together different test datasets on the same chips

#df = pd.concat(map(pd.read_excel, filesnames)) # Change to read_csv for csv files

df = pd.DataFrame()

for file in filesnames:
    df_temp = pd.read_excel(file)
    df_temp['Filename'] = file
    df = df.append(df_temp)

df['Filename'] = df['Filename'].str.split('.').str.get(0)
df = df[ ['Filename'] + [ col for col in df.columns if col != 'Filename' ] ]
df


# In[12]:


# Double check if imported worksheets are not empty - if empty, script is killed

if df.empty:
    Mbox('Error!', 'Imported worksheets are empty', 0)
    sys.exit() # Kill script


# In[13]:


# Double check if expected columns are not missing

try:
    df = df[select_cols]
except KeyError as e:
    Mbox('Error!', repr(e) + '\n Fix then Restart & Run All', 0)
    sys.exit() # Kill script


# In[14]:


# Select columns needed - ADD OR REMOVE AS NEEDED

df = df.fillna(0)

#df = df[df[cols_puls] == pulse_width]
#df = df.drop([cols_puls], axis=1)
#df = df.dropna()
#df


# In[15]:


# Check for any zeros
'''
xdl = []
xd = df[(df.iloc[:,3:] == 0).any(axis=1)]
for i in xd['Number'].unique():
    xdl.append(i)

if xdl:
    Mbox('Warning!', 'Please double-check these numbers / rows - ' + str(xdl) + '\n The rows will be dropped.', 0)
    ''';


# In[16]:


# Drop any rows that have 0s
'''
indices = df.loc[(df.iloc[:,3:] == 0).any(axis=1), :].index.tolist()
for ind in indices:
    df = df.drop(ind)
''';


# In[17]:


# If Voltage above 200v, point out row and drop

df_200v = df[df['Voltage - Currentsource / V'] >= 200]
df = df[df['Voltage - Currentsource / V'] < 200]
if not df_200v.empty:
    class TestApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Observations above 200v which will be dropped')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            self.table = pt = Table(f, dataframe=df_200v,
                                    showtoolbar=True, showstatusbar=True)
            pt.show()
            return

    app = TestApp()
    #launch the app
    app.mainloop()
    #Mbox('Warning!', 'At least one observation has voltage above 200v \n they will be dropped', 0)


# In[18]:


# Function for version checking saved images for pngs

def version_png(fname):
    i = 0
    filename = fname
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}{:d}.png'.format(filename, i), bbox_inches='tight')


# In[19]:


# To change font specifically - fontname = 'provide font name'
# To change font globally - plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})

plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
plt.rc('xtick', labelsize=14) 
plt.rc('ytick', labelsize=14)
plt.rc('axes', labelsize=14)


# # Average of different parts

# In[20]:


dfs = df.groupby(['Phi / °', 'Theta / °']).max().reset_index()
dfs = dfs.drop(['Filename'], axis=1)


# In[21]:


# Calculations (one df for max normalization & another for theta = 0 normalization)

dfmax = dfs.groupby('Phi / °').max().reset_index()
dftheta = dfs[dfs['Theta / °'] == 0]

# Columns besides radiometric & photometric are normalized to theta = 0
test = (dfs.set_index('Phi / °').iloc[:,8:17]-dftheta.set_index('Phi / °').iloc[:,8:17]
        .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2 = (dfs.set_index('Phi / °').iloc[:,[6,7]] / dfmax.set_index('Phi / °').iloc[:,[6,7]]
                .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2.iloc[:,1:] = test2.iloc[:,1:].mul(100)

# Max normalized for radio & photo, rest are theta normalized
dfmaxz = pd.concat([dfs.iloc[:,0:7], test2.iloc[:,1:], test.iloc[:,1:]], axis=1)

# All theta normalized
test2 = (dfs.set_index('Phi / °').iloc[:,[6,7]] / dftheta.set_index('Phi / °').iloc[:,[6,7]]
                .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2.iloc[:,1:] = test2.iloc[:,1:].mul(100)
dfthetaz = pd.concat([dfs.iloc[:,0:7], test2.iloc[:,1:], test.iloc[:,1:]], axis=1)


# In[22]:


# Number vs Voltage
from matplotlib import rcParams

rcParams['figure.figsize'] = 15,5

sns.set_style("whitegrid")
sns.lineplot(x='Number', y='Voltage - Currentsource / V', data=dfs, ci=False, marker = 'o')
plt.title('Voltage - Currentsource / V', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Voltage_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Voltage.png', bbox_inches='tight');


# # Radiometric - By Phi

# In[23]:


# Theta vs Radiometric by Phi (Unnormalized)

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric / W/m² (Unnormalized)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Unnorm_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Unnorm.png', bbox_inches='tight');


# In[24]:


# Theta vs Radiometric by Phi (Normalized to the max)

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to the max)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Max_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Max.png', bbox_inches='tight');


# In[25]:


# Theta vs Radiometric by Phi (Normalized to theta = 0)

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to theta = 0)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Theta0_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Theta0.png', bbox_inches='tight');


# # Radiometric - Averaged

# In[26]:


# Theta vs Radiometric by Phi (Unnormalized) - Averaged by Theta

#dfs_all = dfs.groupby('Theta / °').mean().reset_index()

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfs, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric / W/m² (Unnormalized) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Unnorm_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Unnorm_Avg.png', bbox_inches='tight');


# In[27]:


# Theta vs Radiometric by Phi (Normalized to the max) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfmaxz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to the max) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Max_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Max_Avg.png', bbox_inches='tight');


# In[28]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfthetaz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to theta = 0) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Theta0_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Theta0_Avg.png', bbox_inches='tight');


# # Radiometric - Theta Absolute Values

# In[29]:


dfs['Theta_Abs'] = dfs['Theta / °'].abs()
dfmaxz['Theta_Abs'] = dfmaxz['Theta / °'].abs()
dfthetaz['Theta_Abs'] = dfthetaz['Theta / °'].abs()


# In[30]:


# Theta vs Radiometric by Phi (Unnormalized) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric / W/m² (Unnormalized) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Unnorm_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Unnorm_Abs.png', bbox_inches='tight');


# In[31]:


# Theta vs Radiometric by Phi (Normalized to the max) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to the max) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Max_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Max_Abs.png', bbox_inches='tight');


# In[32]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to theta = 0) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Theta0_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Theta0_Abs.png', bbox_inches='tight');


# # Radiometric - Averaged by Theta Absolute Values

# In[33]:


# Theta vs Radiometric by Phi (Unnormalized) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfs, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric / W/m² (Unnormalized) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Unnorm_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Unnorm_AvgAbs.png', bbox_inches='tight');


# In[34]:


# Theta vs Radiometric by Phi (Normalized to the max) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfmaxz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to the max) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Max_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Max_AvgAbs.png', bbox_inches='tight');


# In[35]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfthetaz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to theta = 0) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Radio_Theta0_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Radio_Theta0_AvgAbs.png', bbox_inches='tight');


# # Photometric - By Phi

# In[36]:


# Theta vs Photometric by Phi (Unnormalized)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric / lx (Unnormalized)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Unnorm_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Unnorm.png', bbox_inches='tight');


# In[37]:


# Theta vs Photometric by Phi (Normalized to the max)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to the max)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Max_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Max.png', bbox_inches='tight');


# In[38]:


# Theta vs Photometric by Phi (Normalized to theta = 0)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to theta = 0)', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Theta0_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Theta0.png', bbox_inches='tight');


# # Photometric - Averaged by Theta

# In[39]:


# Theta vs Photometric by Phi (Unnormalized) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfs, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric / lx (Unnormalized) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Unnorm_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Unnorm_Avg.png', bbox_inches='tight');


# In[40]:


# Theta vs Photometric by Phi (Normalized to the max) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfmaxz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to the max) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Max_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Max_Avg.png', bbox_inches='tight');


# In[41]:


# Theta vs Photometric by Phi (Normalized to theta = 0) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfthetaz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to theta = 0) \n Averaged by Theta', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Theta0_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Theta0_Avg.png', bbox_inches='tight');


# # Photometric - Theta Absolute Values

# In[42]:


# Theta vs Radiometric by Phi (Unnormalized) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric / lx (Unnormalized) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Unnorm_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Unnorm_Abs.png', bbox_inches='tight');


# In[43]:


# Theta vs Radiometric by Phi (Normalized to the max) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to the max) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Max_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Max_Abs.png', bbox_inches='tight');


# In[44]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to theta = 0) \n Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Theta0_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Theta0_Abs.png', bbox_inches='tight');


# # Photometric - Averaged by Theta Absolute Values

# In[45]:


# Theta vs Radiometric by Phi (Unnormalized) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfs, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric / lx (Unnormalized) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Unnorm_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Unnorm_AvgAbs.png', bbox_inches='tight');


# In[46]:


# Theta vs Radiometric by Phi (Normalized to the max) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfmaxz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to the max) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Max_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Max_AvgAbs.png', bbox_inches='tight');


# In[47]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfthetaz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to theta = 0) \n Averaged by Theta Absolute Values', fontsize = 14)

if over == False:
    fname = output_f + '/' + name + '_Photo_Theta0_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_Photo_Theta0_AvgAbs.png', bbox_inches='tight');


# # Polar Coordinates Plot

# In[48]:


# Function for version checking saved images for pngs

def version_pdf_p(fname):
    i = 0
    filename = fname
    while os.path.exists('{}{:d}.pdf'.format(filename, i)):
        i += 1
    fig.savefig('{}{:d}.pdf'.format(filename, i), dpi=1000, bbox_inches='tight')


# In[49]:


# For Polar Plot - Select either Radiometric or Photometric in pop-up box

sel_list = ['Radiometric / W/m²', 'Photometric / lx']

root = ThemedTk(theme='arc')
root.title("GUI for Polar Plot")

Label(root, text = "Select Radiometric or Photometric").grid(row = 1, sticky = W)

e7 = StringVar(root)
e7.set(sel_list[0])
drop = ttk.OptionMenu(root,e7,*sel_list)

drop.grid(row = 2)
    
def kill():
    global h
    h = e7.get()
    root.destroy()
    
ttk.Button(root, text = "Submit",
        command = kill).grid(row = 50)

root.mainloop()

sel = h # or Photometric


# In[50]:


# Groupby theta and take means - able to draw a nice curve

dfmaxz_mean = dfmaxz.groupby('Theta_Abs').mean().reset_index()
dfmaxz_mean[sel] = dfmaxz_mean[sel]/100


# In[51]:


import math  # Change degrees to radians for plotting
def deg_to_rad(dr):
    return (dr*math.pi)/180
theta = deg_to_rad(dfmaxz_mean['Theta_Abs'])
theta_abs = dfmaxz_mean['Theta_Abs']
r = dfmaxz_mean[sel]


# In[52]:


# Polar plot - Normalized to the max

from matplotlib.transforms import Affine2D
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.floating_axes import GridHelperCurveLinear, FloatingSubplot
import mpl_toolkits.axisartist.floating_axes as floating_axes
import mpl_toolkits.axisartist.grid_finder as gf
from matplotlib.ticker import EngFormatter, StrMethodFormatter

rcParams["font.weight"] = "bold"

def setup_axes0_max(fig, rect):
    tr_rotate = Affine2D().translate(1.57, 0)
    polar_trans = tr_rotate + PolarAxes.PolarTransform()

    # Setup the axis, here we map angles in degrees to angles in radius
    phi_degree = np.arange(0, 100, 10)
    a = list(phi_degree)
    al = [str(x) + f"\N{DEGREE SIGN}" for x in a] # List of angles with degree symbols
    tlocs = phi_degree * np.pi / 180
    gl1 = gf.FixedLocator(tlocs)  # Positions
    tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, al))))

    # Standard deviation axis extent
    radius_min = 0
    radius_max = 1.1+0.001
    
    majors = np.linspace(0, 1, 6)
    grid_locator2 = gf.FixedLocator(majors)

    # Set up the axes range in the parameter "extremes"
    grid_helper = GridHelperCurveLinear(polar_trans, extremes=(0, np.pi / 2,  # 1st quadrant
                                                           radius_min, radius_max),
                                    grid_locator1=gl1,
                                    grid_locator2=grid_locator2,
                                    tick_formatter1=tf1,
                                    )
    
    ax0 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax0, zorder=1)

    # Adjust axes
    ax0.axis["top"].set_axis_direction("bottom")  # "Angle axis"
    ax0.axis["top"].toggle(ticklabels=True, label=True)
    ax0.axis["top"].major_ticklabels.set_axis_direction("top")
    ax0.axis["top"].label.set_axis_direction("top")
    #ax0.axis["top"].label.set_text("angle (deg)")

    ax0.axis["left"].set_visible(False)
    #ax0.axis["left"].set_axis_direction("left")  # "X axis"
    #ax0.axis["left"].label.set_text("radius")

    ax0.axis["right"].set_axis_direction("top")  # "Y axis"
    ax0.axis["right"].toggle(ticklabels=True)
    ax0.axis["right"].major_ticklabels.set_axis_direction("bottom")
    ax0.axis["right"].line.set_linewidth(3.5)
    ax0.axis["right"].line.set_color('gray')

    ax0.axis["bottom"].set_visible(False)  # Useless

    # Contours along standard deviations
    ax0.grid(True)
    #ax0.set_title("Quarter polar plot")
    ax0.set_ylim(0, 1.1)

    data_ax = ax0.get_aux_axes(polar_trans)  # return the axes that can be plotted on
    
    # Add second subplot on right

    return ax0, data_ax


if __name__ == "__main__":
    
    fig = plt.figure(figsize=(15,8))
    fig.suptitle('Angular Distribution Graph (Normalized to the max) \n ' + sel.split(' ', 1)[0], fontsize = 14)
    fig.subplots_adjust(wspace=0, hspace=0)
    
    # Left - polar plot
    ax0, aux_ax0 = setup_axes0_max(fig, 121)
    aux_ax0.plot(theta, r, c='black', zorder=111, linewidth=3)
    p = np.polyfit(theta, r, 5) # 5th order fit
    yfit = np.polyval(p, theta)
    # The fit plot - not needed
    #if fitt == True:
    #    aux_ax0.plot(theta, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*0.5, color='gray', linestyle='dotted')
    # Add additional radial lines
    lin = [0.1,0.3,0.7,0.9]
    for i in lin:
        aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*i, color='0.9', linestyle='-', zorder = 0)
    # Add optional lambertian graph
    theta_op = np.arange(0, 2 * np.pi, .01)[1:]
    r_op = np.cos(theta_op)
    r_op = np.abs(r_op)
    if lamb == True:
        aux_ax0.plot(theta_op, r_op, c='blue', linestyle='dotted', zorder=11)
    
    # Right - normal plot
    ax1 = plt.subplot(122, sharey=ax0, zorder=2)
    ax1.tick_params(axis="y",direction="in", pad=-20)
    # Adjust thickness and color of axes
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['left'].set_color('gray')
    ax1.plot(theta_abs, r, c='black', zorder=111, linewidth=3)
    # Only show tick labels multiple of 20
    ax1.set_xticks([0,10,20,30,40,50,60,70,80,90])
    xticks = ax1.xaxis.get_major_ticks()
    xt = [0,1,3,5,7,9]
    for x in xt:
        xticks[x].label1.set_visible(False)
    ax1.yaxis.get_major_ticks()[0].label1.set_visible(False)
    p = np.polyfit(theta_abs, r, 5)
    yfit = np.polyval(p, theta_abs)
    # The fit plot
    #if fitt == True:
    #    ax1.plot(theta_abs, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    ax1.hlines(y=0.5, xmin = 0, xmax = 90, color='gray', linestyle='dotted')
    # Add additional radial lines
    for i in lin:
        ax1.hlines(y=i, xmin = 0, xmax = 90, color='0.9', linestyle='-')
    ax1.margins(x=0)
    # Show tick labels below ticks
    for tick in ax1.yaxis.get_majorticklabels():
        tick.set_verticalalignment("top")
    # Add degree symbol to x-axis
    ax1.xaxis.set_major_formatter(EngFormatter(unit=u"°"))

    # Add optional lambertian graph to other graph
    z = np.cos(theta)
    if lamb == True:
        ax1.plot(theta_abs, z, c='blue', linestyle='dotted', zorder=11)
    box = ax1.get_position()
    box.x0 = box.x0 - 0.005
    box.y0 = box.y0 + 0.001
    ax1.set_position(box)
    # Manually add 0 degree symbol since it randomly disappeared
    plt.text(-1, 1.11, f"0\N{DEGREE SIGN}", fontsize = 14) #10
    if over == False:
        fname = output_f + '/' + name + '_Polar_Max_' + sel[:5] + '_'
        version_pdf_p(fname)
    else:
        fig.savefig(output_f + '/' + name + '_Polar_Max_' + sel[:5] + '.pdf', dpi=1000, bbox_inches='tight')
    plt.show();


# In[51]:


# Groupby theta and take means - able to draw a nice curve

dfthetaz_mean = dfthetaz.groupby('Theta_Abs').mean().reset_index()
dfthetaz_mean[sel] = dfthetaz_mean[sel]/100


# In[52]:


import math  # Change degrees to radians for plotting
def deg_to_rad(dr):
    return (dr*math.pi)/180
theta = deg_to_rad(dfthetaz_mean['Theta_Abs'])
theta_abs = dfthetaz_mean['Theta_Abs']
r = dfthetaz_mean[sel]


# In[53]:


# Polar plot - Normalized to theta = 0

rcParams["font.weight"] = "bold"

def setup_axes0_theta(fig, rect):
    tr_rotate = Affine2D().translate(1.57, 0)
    polar_trans = tr_rotate + PolarAxes.PolarTransform()

    # Setup the axis, here we map angles in degrees to angles in radius
    phi_degree = np.arange(0, 100, 10)
    a = list(phi_degree)
    al = [str(x) + f"\N{DEGREE SIGN}" for x in a] # List of angles with degree symbols
    tlocs = phi_degree * np.pi / 180
    gl1 = gf.FixedLocator(tlocs)  # Positions
    tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, al))))

    # Standard deviation axis extent
    radius_min = 0
    radius_max = 1.3+0.001
    
    majors = np.linspace(0, 1.2, 7)
    grid_locator2 = gf.FixedLocator(majors)

    # Set up the axes range in the parameter "extremes"
    grid_helper = GridHelperCurveLinear(polar_trans, extremes=(0, np.pi / 2,  # 1st quadrant
                                                           radius_min, radius_max),
                                    grid_locator1=gl1,
                                    grid_locator2=grid_locator2,
                                    tick_formatter1=tf1,
                                    )
    
    ax0 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax0, zorder=1)

    # Adjust axes
    ax0.axis["top"].set_axis_direction("bottom")  # "Angle axis"
    ax0.axis["top"].toggle(ticklabels=True, label=True)
    ax0.axis["top"].major_ticklabels.set_axis_direction("top")
    ax0.axis["top"].label.set_axis_direction("top")
    #ax0.axis["top"].label.set_text("angle (deg)")

    ax0.axis["left"].set_visible(False)
    #ax0.axis["left"].set_axis_direction("left")  # "X axis"
    #ax0.axis["left"].label.set_text("radius")

    ax0.axis["right"].set_axis_direction("top")  # "Y axis"
    ax0.axis["right"].toggle(ticklabels=True)
    ax0.axis["right"].major_ticklabels.set_axis_direction("bottom")
    ax0.axis["right"].line.set_linewidth(3.5)
    ax0.axis["right"].line.set_color('gray')

    ax0.axis["bottom"].set_visible(False)  # Useless

    # Contours along standard deviations
    ax0.grid(True)
    #ax0.set_title("Quarter polar plot")
    ax0.set_ylim(0, 1.3)

    data_ax = ax0.get_aux_axes(polar_trans)  # return the axes that can be plotted on
    
    # Add second subplot on right

    return ax0, data_ax


if __name__ == "__main__":
    
    fig = plt.figure(figsize=(15,8))
    fig.suptitle('Angular Distribution Graph (Normalized to theta = 0) \n ' + sel.split(' ', 1)[0], fontsize = 14)
    fig.subplots_adjust(wspace=0, hspace=0)
    
    # Left - polar plot
    ax0, aux_ax0 = setup_axes0_theta(fig, 121)
    aux_ax0.plot(theta, r, c='black', zorder=111, linewidth=3)
    p = np.polyfit(theta, r, 5) # 5th order fit
    yfit = np.polyval(p, theta)
    # The fit plot - not needed
    #if fitt == True:
    #    aux_ax0.plot(theta, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*0.5, color='gray', linestyle='dotted')
    # Add additional radial lines
    lin = [0.1,0.3,0.7,0.9,1.1]
    for i in lin:
        aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*i, color='0.9', linestyle='-')
    # Add optional lambertian graph
    theta_op = np.arange(0, 2 * np.pi, .01)[1:]
    r_op = np.cos(theta_op)
    r_op = np.abs(r_op)
    if lamb == True:
        aux_ax0.plot(theta_op, r_op, c='blue', linestyle='dotted', zorder=11)
    
    # Right - normal plot
    ax1 = plt.subplot(122, sharey=ax0, zorder=0)
    ax1.tick_params(axis="y",direction="in", pad=-20)
    # Adjust thickness and color of axes
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['left'].set_color('gray')
    ax1.plot(theta_abs, r, c='black', zorder=111, linewidth=3)
    # Only show tick labels multiple of 20
    ax1.set_xticks([0,10,20,30,40,50,60,70,80,90])
    xticks = ax1.xaxis.get_major_ticks()
    xt = [0,1,3,5,7,9]
    for x in xt:
        xticks[x].label1.set_visible(False)
    ax1.yaxis.get_major_ticks()[0].label1.set_visible(False)
    p = np.polyfit(theta_abs, r, 5)
    yfit = np.polyval(p, theta_abs)
    # The fit plot
    #if fitt == True:
    #    ax1.plot(theta_abs, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    ax1.hlines(y=0.5, xmin = 0, xmax = 90, color='gray', linestyle='dotted')
    # Add additional radial lines
    for i in lin:
        ax1.hlines(y=i, xmin = 0, xmax = 90, color='0.9', linestyle='-')
    ax1.margins(x=0)
    # Show tick labels below ticks
    for tick in ax1.yaxis.get_majorticklabels():
        tick.set_verticalalignment("top")
    # Add degree symbol to x-axis
    ax1.xaxis.set_major_formatter(EngFormatter(unit=u"°"))

    # Add optional lambertian graph to other graph
    z = np.cos(theta)
    if lamb == True:
        ax1.plot(theta_abs, z, c='blue', linestyle='dotted', zorder=11)
    box = ax1.get_position()
    box.x0 = box.x0 - 0.005
    box.y0 = box.y0 + 0.001
    ax1.set_position(box)
    # Manually add 0 degree symbol since it randomly disappeared
    plt.text(-1, 1.31, f"0\N{DEGREE SIGN}", fontsize = 14) #10
    if over == False:
        fname = output_f + '/' + name + '_Polar_Theta0_' + sel[:5] + '_'
        version_pdf_p(fname)
    else:
        fig.savefig(output_f + '/' + name + '_Polar_Theta0_' + sel[:5] + '.pdf', dpi=1000, bbox_inches='tight')
    plt.show();


# In[54]:


# Function for popup window
class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        title = name + ' - By Serial Number'
        self.setWindowTitle(title)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        self.qapp.exec_()


# In[55]:


# Function for version checking saved images for pngs

def version_png_f(fname):
    i = 0
    filename = fname
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    f.savefig('{}{:d}.png'.format(filename, i))


# In[56]:


# Rest of the columns

sns.set_style("whitegrid")
f, axes = plt.subplots(row_size, column_size, figsize = (15,25))
plt.subplots_adjust(hspace = 0.6)
plt.subplots_adjust(top=0.92)
f.suptitle('GM Graphs', fontsize = 24, fontweight = 'bold')

# Change palette here
sns.set_palette("husl", 9)

for (a,b) in zip(y_n, ax_n):

    c = sns.lineplot(ax=axes[b], x='Theta / °', y=a, hue='Phi / °', data=dfthetaz, ci=False, legend=False, marker='o')

    axes[b].set_title(a, fontweight = 'bold', fontsize = 14)
    c.set(xticks=np.arange(-90, 90+0.01, 30))
 
 # Re-added c1 for legend
c1 = sns.lineplot(ax=axes[0,0], x='Theta / °', y=y1, hue='Phi / °', data=dfthetaz, ci=False, marker='o')

axes[0,0].set_title(y1, fontweight = 'bold', fontsize = 14)
c1.legend(loc='right', bbox_to_anchor=(2.45, 0), ncol=1).set_title('Phi / °') # , prop={'size': 6} <- increase legend size
c1.set_zorder(1)

c5 = sns.lineplot(ax=axes[2,0], x='Theta / °', y=y5, hue='Phi / °', data=dfthetaz, ci=False, marker='o')

axes[2,0].set_title(y5, fontweight = 'bold', fontsize = 14)
c5.legend(loc='right', bbox_to_anchor=(2.45, 0), ncol=1).set_title('Phi / °') # , prop={'size': 6} <- increase legend size
c5.set_zorder(1)

# pass the figure to the custom window
# a = ScrollableWindow(f);


# In[57]:


if over == False:
    fname = output_f + '/' + name + '_GM_Graphs_'
    version_png_f(fname)
else:
    f.savefig(output_f + '/' + name + '_GM_Graphs.png')


# In[58]:


zero = dfthetaz[dfthetaz['Theta / °'] == 0]
zero = zero[['Phi / °', 'x - Color Coordinates', 'y - Color Coordinates']]
df_cols = ["Phi / °", 
           "delta x",
           "delta y"]
zero.columns = df_cols


# In[59]:


new = dfthetaz.merge(zero) # Change if wrong
new['delta x'] = (new['x - Color Coordinates'] - new['delta x']).fillna('-')
new['delta y'] = (new['y - Color Coordinates'] - new['delta y']).fillna('-')
new = new[["Theta / °", "delta x", "delta y"]]
new_df = pd.melt(new, id_vars=['Theta / °'], var_name='Legend', value_name='Δ x, Δ y')


# In[60]:


new_df = new_df[new_df['Δ x, Δ y'] < 1000] # Remove datapoints above 1000


# In[61]:


# Plot delta x and y

sns.lineplot(x='Theta / °', y='Δ x, Δ y', hue="Legend", data=new_df, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Δ x, Δ y \n ' + name, fontsize = 14)
if over == False:
    fname = output_f + '/' + name + '_deltaxy_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + name + '_deltaxy.png', bbox_inches='tight');


# In[62]:


# Export as Excel Worksheet if needed

if exp == True:
    with pd.ExcelWriter(output_f + '/' + name + '_ALL_output.xlsx') as writer:
        dfs.to_excel(writer, sheet_name='Original Data', index=False)
        dfmaxz.to_excel(writer, sheet_name='Normalized to Theta Max', index=False)
        dfthetaz.to_excel(writer, sheet_name='Normalized to Theta = 0', index=False)
else:
    pass


# In[63]:


# View outliers of all the parts

from scipy import stats

cols = list(df.select_dtypes(include=[np.number]).columns)
colsn = cols[4:]

for i in colsn:
    dfsn = df[(np.abs(stats.zscore(df[i])) > 3)]
    if dfsn.empty:
        pass
    else:
        print(i)
        display(dfsn)


# # Dropdown Box for Selecting Specific Part

# In[64]:


fn = list(df['Filename'].unique())

root = ThemedTk(theme='arc')
root.title("GUI for Selecting Specific Part")

Label(root, text = "Select Specific Part").grid(row = 1, sticky = W)

e7 = StringVar(root)
e7.set(fn[0])
drop = ttk.OptionMenu(root,e7,*fn)

drop.grid(row = 2)
    
def kill():
    global h
    h = e7.get()
    root.destroy()
    
ttk.Button(root, text = "Submit",
        command = kill).grid(row = 50)

root.mainloop()
    
dfn = df[df['Filename'] == h]


# In[65]:


# Check if source current is close to actual current

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
diff = abs(dfn['Source current - Currentsource / mA'].iloc[0] - dfn['Current - Currentsource / mA'].mean())

if diff <= 0.5:
    pass
else:
    Mbox('Warning!', 'Mean current and source current difference is larger than 0.5', 0)


# In[66]:


# View outliers of the specific part

from scipy import stats

cols = list(dfn.select_dtypes(include=[np.number]).columns)
colsn = cols[4:]

for i in colsn:
    dfsn = dfn[(np.abs(stats.zscore(dfn[i])) > 3)]
    if dfsn.empty:
        pass
    else:
        print(i)
        display(dfsn)
        
dfn = dfn.drop(['Filename'], axis=1)


# In[67]:


dfs = dfn.groupby(['Phi / °', 'Theta / °']).max().reset_index()

# Calculations (one df for max normalization & another for theta = 0 normalization)

dfmax = dfs.groupby('Phi / °').max().reset_index()
dftheta = dfs[dfs['Theta / °'] == 0]

# Columns besides radiometric & photometric are normalized to theta = 0
test = (dfs.set_index('Phi / °').iloc[:,8:17]-dftheta.set_index('Phi / °').iloc[:,8:17]
        .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2 = (dfs.set_index('Phi / °').iloc[:,[6,7]] / dfmax.set_index('Phi / °').iloc[:,[6,7]]
                .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2.iloc[:,1:] = test2.iloc[:,1:].mul(100)

# Max normalized for radio & photo, rest are theta normalized
dfmaxz = pd.concat([dfs.iloc[:,0:7], test2.iloc[:,1:], test.iloc[:,1:]], axis=1)

# All theta normalized
test2 = (dfs.set_index('Phi / °').iloc[:,[6,7]] / dftheta.set_index('Phi / °').iloc[:,[6,7]]
                .reindex(dfs['Phi / °'])).dropna(axis=0).reset_index()
test2.iloc[:,1:] = test2.iloc[:,1:].mul(100)
dfthetaz = pd.concat([dfs.iloc[:,0:7], test2.iloc[:,1:], test.iloc[:,1:]], axis=1)


# In[68]:


# Number vs Voltage
from matplotlib import rcParams

rcParams['figure.figsize'] = 15,5

sns.set_style("whitegrid")
sns.lineplot(x='Number', y='Voltage - Currentsource / V', data=dfs, ci=False, marker = 'o')
plt.title('Voltage - Currentsource / V \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Voltage_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Voltage.png', bbox_inches='tight');


# # Radiometric - By Phi

# In[69]:


# Theta vs Radiometric by Phi (Unnormalized)

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric / W/m² (Unnormalized) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Unnorm_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Unnorm.png', bbox_inches='tight');


# In[70]:


# Theta vs Radiometric by Phi (Normalized to the max)

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to the max) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Max_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Max.png', bbox_inches='tight');


# In[71]:


# Theta vs Radiometric by Phi (Normalized to theta = 0)

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to theta = 0) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Theta0_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Theta0.png', bbox_inches='tight');


# # Radiometric - Averaged by Theta

# In[72]:


# Theta vs Radiometric by Phi (Unnormalized) - Averaged by Theta

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfs, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric / W/m² (Unnormalized) \n Averaged by Theta \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Unnorm_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Unnorm_Avg.png', bbox_inches='tight');


# In[73]:


# Theta vs Radiometric by Phi (Normalized to the max) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfmaxz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to the max) \n Averaged by Theta \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Max_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Max_Avg.png', bbox_inches='tight');


# In[74]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Radiometric / W/m²', data=dfthetaz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Radiometric (Normalized to theta = 0) \n Averaged by Theta \n' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Theta0_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Theta0_Avg.png', bbox_inches='tight');


# # Radiometric - Theta Absolute Values

# In[75]:


dfs['Theta_Abs'] = dfs['Theta / °'].abs()
dfmaxz['Theta_Abs'] = dfmaxz['Theta / °'].abs()
dfthetaz['Theta_Abs'] = dfthetaz['Theta / °'].abs()


# In[76]:


# Theta vs Radiometric by Phi (Unnormalized) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric / W/m² (Unnormalized) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Unnorm_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Unnorm_Abs.png', bbox_inches='tight');


# In[77]:


# Theta vs Radiometric by Phi (Normalized to the max) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to the max) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Max_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Max_Abs.png', bbox_inches='tight');


# In[78]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to theta = 0) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Theta0_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Theta0_Abs.png', bbox_inches='tight');


# # Radiometric - Averaged by Theta Absolute Values

# In[79]:


# Theta vs Radiometric by Phi (Unnormalized) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfs, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric / W/m² (Unnormalized) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Unnorm_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Unnorm_AvgAbs.png', bbox_inches='tight');


# In[80]:


# Theta vs Radiometric by Phi (Normalized to the max) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfmaxz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to the max) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Max_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Max_AvgAbs.png', bbox_inches='tight');


# In[81]:


# Theta vs Radiometric by Phi (Normalized to theta = 0) - Averaged by Theta Absolute Values

rcParams['figure.figsize'] = 15,8

sns.lineplot(x='Theta_Abs', y='Radiometric / W/m²', data=dfthetaz, marker='o').set_ylabel("Radiometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Radiometric (Normalized to theta = 0) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Radio_Theta0_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Radio_Theta0_AvgAbs.png', bbox_inches='tight');


# # Photometric - By Phi

# In[82]:


# Theta vs Photometric by Phi (Unnormalized)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric / lx (Unnormalized) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Unnorm_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Unnorm.png', bbox_inches='tight');


# In[83]:


# Theta vs Photometric by Phi (Normalized to the max)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to the max) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Max_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Max.png', bbox_inches='tight');


# In[84]:


# Theta vs Photometric by Phi (Normalized to theta = 0)

sns.lineplot(x='Theta / °', y='Photometric / lx', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to theta = 0) \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Theta0_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Theta0.png', bbox_inches='tight');


# # Photometric - Averaged by Theta

# In[85]:


# Theta vs Photometric by Phi (Unnormalized) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfs, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric / lx (Unnormalized) \n Averaged by Theta \n' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Unnorm_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Unnorm_Avg.png', bbox_inches='tight');


# In[86]:


# Theta vs Photometric by Phi (Normalized to the max) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfmaxz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to the max) \n Averaged by Theta \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Max_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Max_Avg.png', bbox_inches='tight');


# In[87]:


# Theta vs Photometric by Phi (Normalized to theta = 0) - Averaged by Theta

sns.lineplot(x='Theta / °', y='Photometric / lx', data=dfthetaz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Photometric (Normalized to theta = 0) \n Averaged by Theta \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Theta0_Avg_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Theta0_Avg.png', bbox_inches='tight');


# # Photometric - Theta Absolute Values

# In[88]:


# Theta vs Photometric by Phi (Unnormalized) - Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfs, ci=False, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric / lx (Unnormalized) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Unnorm_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Unnorm_Abs.png', bbox_inches='tight');


# In[89]:


# Theta vs Photometric by Phi (Normalized to the max) - Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfmaxz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to the max) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Max_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Max_Abs.png', bbox_inches='tight');


# In[90]:


# Theta vs Photometric by Phi (Normalized to theta = 0) - Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', hue = 'Phi / °', data=dfthetaz, ci=False, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to theta = 0) \n Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Theta0_Abs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Theta0_Abs.png', bbox_inches='tight');


# # Photometric - Averaged by Theta Absolute Values

# In[91]:


# Theta vs Photometric by Phi (Unnormalized) - Averaged by Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfs, marker='o')
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric / lx (Unnormalized) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Unnorm_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Unnorm_AvgAbs.png', bbox_inches='tight');


# In[92]:


# Theta vs Photometric by Phi (Normalized to the max) - Averaged by Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfmaxz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to the max) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Max_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Max_AvgAbs.png', bbox_inches='tight');


# In[93]:


# Theta vs Photometric by Phi (Normalized to theta = 0) - Averaged by Theta Absolute Values

sns.lineplot(x='Theta_Abs', y='Photometric / lx', data=dfthetaz, marker='o').set_ylabel("Photometric")
plt.xticks(np.arange(0, 90+0.01, 15))
plt.title('Photometric (Normalized to theta = 0) \n Averaged by Theta Absolute Values \n ' + h, fontsize = 14)

if over == False:
    fname = output_f + '/' + h + '_Photo_Theta0_AvgAbs_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_Photo_Theta0_AvgAbs.png', bbox_inches='tight');


# # Polar Coordinates Plot

# In[94]:


# Groupby theta and take means - able to draw a nice curve

dfmaxz_mean = dfmaxz.groupby('Theta_Abs').mean().reset_index()
dfmaxz_mean[sel] = dfmaxz_mean[sel]/100


# In[95]:


import math  # Change degrees to radians for plotting
def deg_to_rad(dr):
    return (dr*math.pi)/180
theta = deg_to_rad(dfmaxz_mean['Theta_Abs'])
theta_abs = dfmaxz_mean['Theta_Abs']
r = dfmaxz_mean[sel]


# In[96]:


# Polar plot - Normalized to the max

rcParams["font.weight"] = "bold"

if __name__ == "__main__":
    
    fig = plt.figure(figsize=(15,8))
    fig.suptitle('Angular Distribution Graph (Normalized to the max) \n ' + sel.split(' ', 1)[0], fontsize = 14)
    fig.subplots_adjust(wspace=0, hspace=0)
    
    # Left - polar plot
    ax0, aux_ax0 = setup_axes0_max(fig, 121)
    aux_ax0.plot(theta, r, c='black', zorder=111, linewidth=3)
    p = np.polyfit(theta, r, 5) # 5th order fit
    yfit = np.polyval(p, theta)
    # The fit plot - not needed
    #if fitt == True:
    #    aux_ax0.plot(theta, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*0.5, color='gray', linestyle='dotted')
    # Add additional radial lines
    lin = [0.1,0.3,0.7,0.9]
    for i in lin:
        aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*i, color='0.9', linestyle='-')
    # Add optional lambertian graph
    theta_op = np.arange(0, 2 * np.pi, .01)[1:]
    r_op = np.cos(theta_op)
    r_op = np.abs(r_op)
    if lamb == True:
        aux_ax0.plot(theta_op, r_op, c='blue', linestyle='dotted', zorder=11)
    
    # Right - normal plot
    ax1 = plt.subplot(122, sharey=ax0, zorder=0)
    ax1.tick_params(axis="y",direction="in", pad=-20)
    # Adjust thickness and color of axes
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['left'].set_color('gray')
    ax1.plot(theta_abs, r, c='black', zorder=111, linewidth=3)
    # Only show tick labels multiple of 20
    ax1.set_xticks([0,10,20,30,40,50,60,70,80,90])
    xticks = ax1.xaxis.get_major_ticks()
    xt = [0,1,3,5,7,9]
    for x in xt:
        xticks[x].label1.set_visible(False)
    ax1.yaxis.get_major_ticks()[0].label1.set_visible(False)
    p = np.polyfit(theta_abs, r, 5)
    yfit = np.polyval(p, theta_abs)
    # The fit plot
    #if fitt == True:
    #    ax1.plot(theta_abs, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    ax1.hlines(y=0.5, xmin = 0, xmax = 90, color='gray', linestyle='dotted')
    # Add additional radial lines
    for i in lin:
        ax1.hlines(y=i, xmin = 0, xmax = 90, color='0.9', linestyle='-')
    ax1.margins(x=0)
    # Show tick labels below ticks
    for tick in ax1.yaxis.get_majorticklabels():
        tick.set_verticalalignment("top")
    # Add degree symbol to x-axis
    ax1.xaxis.set_major_formatter(EngFormatter(unit=u"°"))

    # Add optional lambertian graph to other graph
    z = np.cos(theta)
    if lamb == True:
        ax1.plot(theta_abs, z, c='blue', linestyle='dotted', zorder=11)
    box = ax1.get_position()
    box.x0 = box.x0 - 0.005
    box.y0 = box.y0 + 0.001
    ax1.set_position(box)
    # Manually add 0 degree symbol since it randomly disappeared
    plt.text(-1, 1.11, f"0\N{DEGREE SIGN}", fontsize = 14) #10
    if over == False:
        fname = output_f + '/' + h + '_Polar_Max_' + sel[:5] + '_'
        version_pdf_p(fname)
    else:
        fig.savefig(output_f + '/' + h + '_Polar_Max_' + sel[:5] + '.pdf', dpi=1000, bbox_inches='tight')
    plt.show();


# In[97]:


# Groupby theta and take means - able to draw a nice curve

dfthetaz_mean = dfthetaz.groupby('Theta_Abs').mean().reset_index()
dfthetaz_mean[sel] = dfthetaz_mean[sel]/100


# In[98]:


import math  # Change degrees to radians for plotting
def deg_to_rad(dr):
    return (dr*math.pi)/180
theta = deg_to_rad(dfthetaz_mean['Theta_Abs'])
theta_abs = dfthetaz_mean['Theta_Abs']
r = dfthetaz_mean[sel]


# In[99]:


# Polar plot - Normalized to theta = 0

rcParams["font.weight"] = "bold"

if __name__ == "__main__":
    
    fig = plt.figure(figsize=(15,8))
    fig.suptitle('Angular Distribution Graph (Normalized to theta = 0) \n ' + sel.split(' ', 1)[0], fontsize = 14)
    fig.subplots_adjust(wspace=0, hspace=0)
    
    # Left - polar plot
    ax0, aux_ax0 = setup_axes0_theta(fig, 121)
    aux_ax0.plot(theta, r, c='black', zorder=111, linewidth=3)
    p = np.polyfit(theta, r, 5) # 5th order fit
    yfit = np.polyval(p, theta)
    # The fit plot
    #if fitt == True:
    #    aux_ax0.plot(theta, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*0.5, color='gray', linestyle='dotted')
    # Add additional radial lines
    lin = [0.1,0.3,0.7,0.9,1.1]
    for i in lin:
        aux_ax0.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*i, color='0.9', linestyle='-')
    # Add optional lambertian graph
    theta_op = np.arange(0, 2 * np.pi, .01)[1:]
    r_op = np.cos(theta_op)
    r_op = np.abs(r_op)
    if lamb == True:
        aux_ax0.plot(theta_op, r_op, c='blue', linestyle='dotted', zorder=11)
    
    # Right - normal plot
    ax1 = plt.subplot(122, sharey=ax0, zorder=0)
    ax1.tick_params(axis="y",direction="in", pad=-20)
    # Adjust thickness and color of axes
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['left'].set_color('gray')
    ax1.plot(theta_abs, r, c='black', zorder=111, linewidth=3)
    # Only show tick labels multiple of 20
    ax1.set_xticks([0,10,20,30,40,50,60,70,80,90])
    xticks = ax1.xaxis.get_major_ticks()
    xt = [0,1,3,5,7,9]
    for x in xt:
        xticks[x].label1.set_visible(False)
    ax1.yaxis.get_major_ticks()[0].label1.set_visible(False)
    p = np.polyfit(theta_abs, r, 5)
    yfit = np.polyval(p, theta_abs)
    # The fit plot
    #if fitt == True:
    #    ax1.plot(theta_abs, yfit, '-', zorder=11)
    # Radial = 0.5 plot
    ax1.hlines(y=0.5, xmin = 0, xmax = 90, color='gray', linestyle='dotted')
    # Add additional radial lines
    for i in lin:
        ax1.hlines(y=i, xmin = 0, xmax = 90, color='0.9', linestyle='-')
    ax1.margins(x=0)
    # Show tick labels below ticks
    for tick in ax1.yaxis.get_majorticklabels():
        tick.set_verticalalignment("top")
    # Add degree symbol to x-axis
    ax1.xaxis.set_major_formatter(EngFormatter(unit=u"°"))

    # Add optional lambertian graph to other graph
    z = np.cos(theta)
    if lamb == True:
        ax1.plot(theta_abs, z, c='blue', linestyle='dotted', zorder=11)
    box = ax1.get_position()
    box.x0 = box.x0 - 0.005
    box.y0 = box.y0 + 0.001
    ax1.set_position(box)
    # Manually add 0 degree symbol since it randomly disappeared
    plt.text(-1, 1.31, f"0\N{DEGREE SIGN}", fontsize = 14) #10
    if over == False:
        fname = output_f + '/' + h + '_Polar_Theta0_' + sel[:5] + '_'
        version_pdf_p(fname)
    else:
        fig.savefig(output_f + '/' + h + '_Polar_Theta0_' + sel[:5] + '.pdf', dpi=1000, bbox_inches='tight')
    plt.show();


# In[100]:


# Rest of the columns

# To change font specifically - fontname = 'provide font name'
# To change font globally - plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})

plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
plt.rc('xtick', labelsize=14) 
plt.rc('ytick', labelsize=14)
plt.rc('axes', labelsize=14)

sns.set_style("whitegrid")
f, axes = plt.subplots(row_size, column_size, figsize = (15,25))
plt.subplots_adjust(hspace = 0.6)
plt.subplots_adjust(top=0.92)
f.suptitle('GM Graphs \n' + h, fontsize = 24, fontweight = 'bold')

# Change palette here
sns.set_palette("husl", 9)

for (a,b) in zip(y_n, ax_n):

    c = sns.lineplot(ax=axes[b], x='Theta / °', y=a, hue='Phi / °', data=dfthetaz, ci=False, legend=False, marker='o')

    axes[b].set_title(a, fontweight = 'bold', fontsize = 14)
    c.set(xticks=np.arange(-90, 90+0.01, 30))
 
 # Re-added c1 for legend
c1 = sns.lineplot(ax=axes[0,0], x='Theta / °', y=y1, hue='Phi / °', data=dfthetaz, ci=False, marker='o')

axes[0,0].set_title(y1, fontweight = 'bold', fontsize = 14)
c1.legend(loc='right', bbox_to_anchor=(2.45, 0), ncol=1).set_title('Phi / °') # , prop={'size': 6} <- increase legend size
c1.set_zorder(1)

c5 = sns.lineplot(ax=axes[2,0], x='Theta / °', y=y5, hue='Phi / °', data=dfthetaz, ci=False, marker='o')

axes[2,0].set_title(y5, fontweight = 'bold', fontsize = 14)
c5.legend(loc='right', bbox_to_anchor=(2.45, 0), ncol=1).set_title('Phi / °') # , prop={'size': 6} <- increase legend size
c5.set_zorder(1)

# pass the figure to the custom window
#a = ScrollableWindow(f);


# In[101]:


if over == False:
    fname = output_f + '/' + h + '_GM_Graphs_'
    version_png_f(fname)
else:
    f.savefig(output_f + '/' + h + '_GM_Graphs.png')


# In[102]:


zero = dfthetaz[dfthetaz['Theta / °'] == 0]
zero = zero[['Phi / °', 'x - Color Coordinates', 'y - Color Coordinates']]
df_cols = ["Phi / °", 
           "delta x",
           "delta y"]
zero.columns = df_cols


# In[103]:


new = dfthetaz.merge(zero) # Change if wrong
new['delta x'] = (new['x - Color Coordinates'] - new['delta x']).fillna('-')
new['delta y'] = (new['y - Color Coordinates'] - new['delta y']).fillna('-')
new = new[["Theta / °", "delta x", "delta y"]]
new_df = pd.melt(new, id_vars=['Theta / °'], var_name='Legend', value_name='Δ x, Δ y')


# In[104]:


# Plot delta x and y

sns.lineplot(x='Theta / °', y='Δ x, Δ y', hue="Legend", data=new_df, ci=False, marker='o')
plt.xticks(np.arange(-90, 90+0.01, 30))
plt.title('Δ x, Δ y \n ' + h, fontsize = 14)
if over == False:
    fname = output_f + '/' + h + '_deltaxy_'
    version_png(fname)
else:
    plt.savefig(output_f + '/' + h + '_deltaxy.png', bbox_inches='tight');


# In[105]:


# Export as Excel Worksheet if needed

if exp == True:
    with pd.ExcelWriter(output_f + '/' + h + '_output.xlsx') as writer:
        dfs.to_excel(writer, sheet_name='Original Data', index=False)
        dfmaxz.to_excel(writer, sheet_name='Normalized to Theta Max', index=False)
        dfthetaz.to_excel(writer, sheet_name='Normalized to Theta = 0', index=False)
else:
    pass


# In[106]:


# Kills script so appendix doesn't run
sys.exit()

