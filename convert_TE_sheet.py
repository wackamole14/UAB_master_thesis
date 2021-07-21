{
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  },
  "orig_nbformat": 2,
  "kernelspec": {
   "name": "python3710jvsc74a57bd0dca0ade3e726a953b501b15e8e990130d2b7799f14cfd9f4271676035ebe5511",
   "display_name": "Python 3.7.10 64-bit ('base': conda)"
  },
  "metadata": {
   "interpreter": {
    "hash": "aee8b7b246df8f9039afb4144a1f6fd8d2ca17a180786b69acc140d282b71a49"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2,
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Convert the 5 Long genome results to be able to be concatenated to the other results. You \n",
    "#must add the name of each genome to the list of genomes, if the TE family is the same. \n",
    "\n",
    "-------\n",
    "# if you dont have the file \"tmp_Long_TE_files\" already, you need to make the file, take each new TE_annotate file, and combine them into one file like this: \n",
    "cut -f1,2,3,4  ZH26_TE_transferred_2_ISO_info.tsv > ZH26_file\n",
    "cat ZH26_file >> tmp_Long_TE_files\n",
    "-------\n",
    "#this causes the \"headers\" to be added to the list, and causes one other small error, get rid of them in the following \"FIX\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 293,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import os\n",
    "import sys"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 294,
   "metadata": {},
   "outputs": [],
   "source": [
    "# get rid of possible headers in the concatenated Long files if you haven't done so\n",
    "df1 = pd.read_csv(f'tmp_Long_TE_files', sep='\\t', header=None)\n",
    "df1['family']= df1[3].str.split('_')\n",
    "df1['len']= [len(x) for x in df1['family']]\n",
    "df1.drop(df1[df1['len'] == 1].index, inplace=True)\n",
    "df1['family']= df1[3].apply(lambda col: col.split('_')[-1])\n",
    "df1['sample']= df1[3].apply(lambda col: col.split('_')[0])\n",
    "df1= df1.drop(columns='len')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 296,
   "metadata": {},
   "outputs": [],
   "source": [
    "df1.to_csv('tmp_Long_TE_files_fix' , index=False,  sep='\\t', header=False)"
   ]
  },
  {
   "source": [
    "# Start combining the new samples and the old shee passed by Santi"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 297,
   "metadata": {},
   "outputs": [],
   "source": [
    "fixed_space_columns=['TE_name', 'Chromosome', 'Start', 'End', 'Strand', 'Class', 'Order',\\\n",
    "       'SuperFamily', 'Family', 'TE_present_in_REF','Number_of_genomes_present', 'Genomes', 'TE_name_in_strain',\\\n",
    "       'TE_length_c', 'TE_ratio','Recombination_rate_Comeron_2012',\\\n",
    "       'Recombination_rate_Fiston_2011','Recombination_classification', 'TE_used_in_SFS_analysis', 'Europe',\\\n",
    "       'North_America', 'Other']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 298,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.ExcelFile('SuppTables_v5_Santi.tsv.xlsx').parse('S10', skiprows=1, names=fixed_space_columns)"
   ]
  },
  {
   "source": [
    "# Rearange the old file so it can be used with bed tools (format chrom, start, end...)"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 299,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "      Chromosome     Start       End                        TE_name Strand  \\\n",
       "0             2L   2933354   2935475                    FBti0019112      +   \n",
       "1             2L   7579255   7579380                    FBti0019133      +   \n",
       "2             2L  11215132  11218743                    FBti0059794      -   \n",
       "3             2L  11315294  11317659                    FBti0019149      +   \n",
       "4             2L  11897168  11900029                    FBti0019153      +   \n",
       "...          ...       ...       ...                            ...    ...   \n",
       "28942          X  21319389  21319389  X_21319389_21319389_P-element      -   \n",
       "28943          X  21322782  21322803       X_21322782_21322803_Doc6      -   \n",
       "28944          X  21328226  21328226      X_21328226_21328226_Bari1      +   \n",
       "28945          X  21329021  21329155               ISO1_2059_Kepler      +   \n",
       "28946          X  21329937  21329937        X_21329937_21329937_Doc      -   \n",
       "\n",
       "      Class Order SuperFamily     Family TE_present_in_REF  ...  \\\n",
       "0       DNA   TIR  TcMar-Pogo       pogo               YES  ...   \n",
       "1       RNA  LINE      Jockey         BS               YES  ...   \n",
       "2       RNA  LINE      Jockey        Doc               YES  ...   \n",
       "3       RNA  LINE      Jockey         G2               YES  ...   \n",
       "4       RNA  LINE      Jockey        BS2               YES  ...   \n",
       "...     ...   ...         ...        ...               ...  ...   \n",
       "28942   DNA   TIR           P  P-element                NO  ...   \n",
       "28943   RNA  LINE      Jockey       Doc6                NO  ...   \n",
       "28944   DNA   TIR   TcMar-Tc1      Bari1                NO  ...   \n",
       "28945   RNA  TRIM       Gypsy     Kepler               YES  ...   \n",
       "28946   RNA  LINE      Jockey        Doc                NO  ...   \n",
       "\n",
       "                                       TE_name_in_strain  \\\n",
       "0      ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...   \n",
       "1      ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...   \n",
       "2                                            FBti0059794   \n",
       "3                                            FBti0019149   \n",
       "4      ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...   \n",
       "...                                                  ...   \n",
       "28942                             MUN-013_2268_P-element   \n",
       "28943  A6_2230_Doc6;MUN-013_2269_Doc6;AKA-018_2198_Do...   \n",
       "28944                                 JUT-008_2026_Bari1   \n",
       "28945  ORE_2050_Kepler;A6_2231_Kepler;B6_2089_Kepler;...   \n",
       "28946                                        B2_2211_Doc   \n",
       "\n",
       "                                             TE_length_c  \\\n",
       "0      2122;2122;2122;2118;2120;2123;2122;2122;2127;2...   \n",
       "1      125;126;125;125;125;125;124;125;126;124;125;12...   \n",
       "2                                                   3611   \n",
       "3                                                   2365   \n",
       "4      2806;2872;2871;2872;2872;2872;2869;2869;2872;2...   \n",
       "...                                                  ...   \n",
       "28942                                               1800   \n",
       "28943    220;220;220;220;220;220;136;219;220;220;220;220   \n",
       "28944                                               1733   \n",
       "28945  134;134;130;134;134;134;134;134;134;134;126;13...   \n",
       "28946                                               4723   \n",
       "\n",
       "                                                TE_ratio  \\\n",
       "0      0.95;0.95;0.95;0.948;0.949;0.951;0.95;0.95;0.9...   \n",
       "1      0.023;0.024;0.023;0.023;0.023;0.023;0.023;0.02...   \n",
       "2                                                      .   \n",
       "3                                                      .   \n",
       "4      0.583;0.597;0.597;0.597;0.597;0.597;0.596;0.59...   \n",
       "...                                                  ...   \n",
       "28942                                              0.494   \n",
       "28943  0.05;0.05;0.05;0.05;0.05;0.05;0.031;0.05;0.05;...   \n",
       "28944                                              0.982   \n",
       "28945  0.076;0.076;0.07400000000000001;0.076;0.076;0....   \n",
       "28946                                              0.987   \n",
       "\n",
       "      Recombination_rate_Comeron_2012 Recombination_rate_Fiston_2011  \\\n",
       "0                            0.938201                           3.26   \n",
       "1                            2.580052                           4.24   \n",
       "2                                   .                              .   \n",
       "3                                   .                              .   \n",
       "4                            1.993676                           3.55   \n",
       "...                               ...                            ...   \n",
       "28942                        0.723341                           0.84   \n",
       "28943                        0.723341                           0.84   \n",
       "28944                        0.723341                           0.84   \n",
       "28945                        1.085012                           0.79   \n",
       "28946                        1.085012                           0.79   \n",
       "\n",
       "      Recombination_classification TE_used_in_SFS_analysis Europe  \\\n",
       "0                              HRR                     YES      9   \n",
       "1                              HRR                     YES      7   \n",
       "2                                .                     YES      1   \n",
       "3                                .                     YES      1   \n",
       "4                              HRR                     YES      6   \n",
       "...                            ...                     ...    ...   \n",
       "28942                          HRR                     YES      0   \n",
       "28943                          HRR                     YES      3   \n",
       "28944                          HRR                     YES      0   \n",
       "28945                          HRR                     YES      8   \n",
       "28946                          HRR                     YES      0   \n",
       "\n",
       "      North_America  Other  \n",
       "0                16      3  \n",
       "1                13      4  \n",
       "2                 0      0  \n",
       "3                 0      0  \n",
       "4                 6      1  \n",
       "...             ...    ...  \n",
       "28942             1      0  \n",
       "28943             9      0  \n",
       "28944             1      0  \n",
       "28945            10      4  \n",
       "28946             0      1  \n",
       "\n",
       "[28947 rows x 22 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>Chromosome</th>\n      <th>Start</th>\n      <th>End</th>\n      <th>TE_name</th>\n      <th>Strand</th>\n      <th>Class</th>\n      <th>Order</th>\n      <th>SuperFamily</th>\n      <th>Family</th>\n      <th>TE_present_in_REF</th>\n      <th>...</th>\n      <th>TE_name_in_strain</th>\n      <th>TE_length_c</th>\n      <th>TE_ratio</th>\n      <th>Recombination_rate_Comeron_2012</th>\n      <th>Recombination_rate_Fiston_2011</th>\n      <th>Recombination_classification</th>\n      <th>TE_used_in_SFS_analysis</th>\n      <th>Europe</th>\n      <th>North_America</th>\n      <th>Other</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2L</td>\n      <td>2933354</td>\n      <td>2935475</td>\n      <td>FBti0019112</td>\n      <td>+</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>TcMar-Pogo</td>\n      <td>pogo</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...</td>\n      <td>2122;2122;2122;2118;2120;2123;2122;2122;2127;2...</td>\n      <td>0.95;0.95;0.95;0.948;0.949;0.951;0.95;0.95;0.9...</td>\n      <td>0.938201</td>\n      <td>3.26</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>9</td>\n      <td>16</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2L</td>\n      <td>7579255</td>\n      <td>7579380</td>\n      <td>FBti0019133</td>\n      <td>+</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...</td>\n      <td>125;126;125;125;125;125;124;125;126;124;125;12...</td>\n      <td>0.023;0.024;0.023;0.023;0.023;0.023;0.023;0.02...</td>\n      <td>2.580052</td>\n      <td>4.24</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>7</td>\n      <td>13</td>\n      <td>4</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2L</td>\n      <td>11215132</td>\n      <td>11218743</td>\n      <td>FBti0059794</td>\n      <td>-</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>FBti0059794</td>\n      <td>3611</td>\n      <td>.</td>\n      <td>.</td>\n      <td>.</td>\n      <td>.</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>0</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>2L</td>\n      <td>11315294</td>\n      <td>11317659</td>\n      <td>FBti0019149</td>\n      <td>+</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>G2</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>FBti0019149</td>\n      <td>2365</td>\n      <td>.</td>\n      <td>.</td>\n      <td>.</td>\n      <td>.</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>0</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>2L</td>\n      <td>11897168</td>\n      <td>11900029</td>\n      <td>FBti0019153</td>\n      <td>+</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS2</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...</td>\n      <td>2806;2872;2871;2872;2872;2872;2869;2869;2872;2...</td>\n      <td>0.583;0.597;0.597;0.597;0.597;0.597;0.596;0.59...</td>\n      <td>1.993676</td>\n      <td>3.55</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>6</td>\n      <td>6</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>28942</th>\n      <td>X</td>\n      <td>21319389</td>\n      <td>21319389</td>\n      <td>X_21319389_21319389_P-element</td>\n      <td>-</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>P</td>\n      <td>P-element</td>\n      <td>NO</td>\n      <td>...</td>\n      <td>MUN-013_2268_P-element</td>\n      <td>1800</td>\n      <td>0.494</td>\n      <td>0.723341</td>\n      <td>0.84</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>0</td>\n      <td>1</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>28943</th>\n      <td>X</td>\n      <td>21322782</td>\n      <td>21322803</td>\n      <td>X_21322782_21322803_Doc6</td>\n      <td>-</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc6</td>\n      <td>NO</td>\n      <td>...</td>\n      <td>A6_2230_Doc6;MUN-013_2269_Doc6;AKA-018_2198_Do...</td>\n      <td>220;220;220;220;220;220;136;219;220;220;220;220</td>\n      <td>0.05;0.05;0.05;0.05;0.05;0.05;0.031;0.05;0.05;...</td>\n      <td>0.723341</td>\n      <td>0.84</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>3</td>\n      <td>9</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>28944</th>\n      <td>X</td>\n      <td>21328226</td>\n      <td>21328226</td>\n      <td>X_21328226_21328226_Bari1</td>\n      <td>+</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>TcMar-Tc1</td>\n      <td>Bari1</td>\n      <td>NO</td>\n      <td>...</td>\n      <td>JUT-008_2026_Bari1</td>\n      <td>1733</td>\n      <td>0.982</td>\n      <td>0.723341</td>\n      <td>0.84</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>0</td>\n      <td>1</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>28945</th>\n      <td>X</td>\n      <td>21329021</td>\n      <td>21329155</td>\n      <td>ISO1_2059_Kepler</td>\n      <td>+</td>\n      <td>RNA</td>\n      <td>TRIM</td>\n      <td>Gypsy</td>\n      <td>Kepler</td>\n      <td>YES</td>\n      <td>...</td>\n      <td>ORE_2050_Kepler;A6_2231_Kepler;B6_2089_Kepler;...</td>\n      <td>134;134;130;134;134;134;134;134;134;134;126;13...</td>\n      <td>0.076;0.076;0.07400000000000001;0.076;0.076;0....</td>\n      <td>1.085012</td>\n      <td>0.79</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>8</td>\n      <td>10</td>\n      <td>4</td>\n    </tr>\n    <tr>\n      <th>28946</th>\n      <td>X</td>\n      <td>21329937</td>\n      <td>21329937</td>\n      <td>X_21329937_21329937_Doc</td>\n      <td>-</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc</td>\n      <td>NO</td>\n      <td>...</td>\n      <td>B2_2211_Doc</td>\n      <td>4723</td>\n      <td>0.987</td>\n      <td>1.085012</td>\n      <td>0.79</td>\n      <td>HRR</td>\n      <td>YES</td>\n      <td>0</td>\n      <td>0</td>\n      <td>1</td>\n    </tr>\n  </tbody>\n</table>\n<p>28947 rows × 22 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 299
    }
   ],
   "source": [
    "df_TE_Sheet= df[['Chromosome', 'Start', 'End', 'TE_name','Strand', 'Class', 'Order',\n",
    "       'SuperFamily', 'Family', 'TE_present_in_REF',\n",
    "       'Number_of_genomes_present', 'Genomes', 'TE_name_in_strain',\n",
    "       'TE_length_c', 'TE_ratio',\n",
    "       'Recombination_rate_Comeron_2012',\n",
    "       'Recombination_rate_Fiston_2011',\n",
    "       'Recombination_classification', 'TE_used_in_SFS_analysis', 'Europe',\n",
    "       'North_America', 'Other']].copy()\n",
    "df_TE_Sheet"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 300,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_TE_Sheet.to_csv('SuppTables_v5_Santi.tsv' , index=False,  sep='\\t', header=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 301,
   "metadata": {},
   "outputs": [],
   "source": [
    "#df_TE_sheet = pd.read_csv(f'TE_sheet.txt', sep='\\t', header=None)\n",
    "df1 = pd.read_csv(f'tmp_Long_TE_files_fix', sep='\\t', header=None)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 253,
   "metadata": {},
   "outputs": [],
   "source": [
    "#os.system('intersectBed -F 0.8 -a SuppTables_v5_Santi.tsv -b tmp_Long_TE_files_fix -loj > Long_TE_intersect.bed') #get the overlapping TEs\n",
    "#os.system('intersectBed -F 0.8 -a tmp_Long_TE_files_fix -b SuppTables_v5_Santi.tsv-v > unique_Long_TEs.bed')  # Get the unique Long TEs\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 254,
   "metadata": {},
   "outputs": [],
   "source": [
    "df2 = pd.read_csv(f'Long_TE_intersect.bed', sep='\\t', header=None)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 255,
   "metadata": {},
   "outputs": [],
   "source": [
    "def shared_TEs(df2):\n",
    "    if df2[26] != '.':\n",
    "        if df2[8] == df2[26]:\n",
    "            new_sample_list= True\n",
    "            return new_sample_list\n",
    "    else:\n",
    "        return np.nan"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 256,
   "metadata": {},
   "outputs": [],
   "source": [
    "df2['new_te']= df2.apply(shared_TEs, axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 257,
   "metadata": {},
   "outputs": [],
   "source": [
    "df2.loc[(df2['new_te']!= True), 27] = np.nan"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 258,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "                               3  27\n",
       "0          2L_10020779_10020779_H   \n",
       "1  2L_10026392_10026392_I-element   \n",
       "2          2L_10030857_10030857_H   "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>3</th>\n      <th>27</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2L_10020779_10020779_H</td>\n      <td></td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2L_10026392_10026392_I-element</td>\n      <td></td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2L_10030857_10030857_H</td>\n      <td></td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 258
    }
   ],
   "source": [
    "df_new_tes= df2.groupby([3]).agg({27:lambda x: ';'.join(x.dropna())}).reset_index()\n",
    "df_new_tes.head(3)"
   ]
  },
  {
   "source": [
    "#\n",
    "# You already read in the original TE sheet, it is called \"df_TE_sheet\", merge it here \n",
    "#"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 279,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_TE = pd.merge(df_TE_Sheet, df_new_tes.rename(columns={3:'TE_name'}), how=\"left\", on=['TE_name'])"
   ]
  },
  {
   "source": [
    "def New_TE_List(df_TE):\n",
    "    if df_TE[27] != '':\n",
    "        new_te_list= df_TE['Genomes']+';'+ df_TE[27] \n",
    "        return new_te_list\n",
    "    else:\n",
    "        return df_TE['Genomes']"
   ],
   "cell_type": "code",
   "metadata": {},
   "execution_count": 280,
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": 281,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_TE['Genomes']= df_TE.apply(New_TE_List, axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 282,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "0        31\n",
       "1        27\n",
       "2         1\n",
       "3         1\n",
       "4        14\n",
       "         ..\n",
       "28942     1\n",
       "28943    13\n",
       "28944     1\n",
       "28945    25\n",
       "28946     1\n",
       "Name: Number_of_genomes_present, Length: 28947, dtype: int64"
      ]
     },
     "metadata": {},
     "execution_count": 282
    }
   ],
   "source": [
    "df_TE['Number_of_genomes_present']= [len(x) for x in df_TE['Genomes'].str.split(';').tolist()]\n",
    "df_TE['Number_of_genomes_present']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 283,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_TE= df_TE.drop(columns={27})"
   ]
  },
  {
   "source": [
    "# Massively reduce columns here, if you are looking for dropped data its probably here!"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 284,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "      Chromosome     Start       End                        TE_name Class  \\\n",
       "0             2L   2933354   2935475                    FBti0019112   DNA   \n",
       "1             2L   7579255   7579380                    FBti0019133   RNA   \n",
       "2             2L  11215132  11218743                    FBti0059794   RNA   \n",
       "3             2L  11315294  11317659                    FBti0019149   RNA   \n",
       "4             2L  11897168  11900029                    FBti0019153   RNA   \n",
       "...          ...       ...       ...                            ...   ...   \n",
       "28942          X  21319389  21319389  X_21319389_21319389_P-element   DNA   \n",
       "28943          X  21322782  21322803       X_21322782_21322803_Doc6   RNA   \n",
       "28944          X  21328226  21328226      X_21328226_21328226_Bari1   DNA   \n",
       "28945          X  21329021  21329155               ISO1_2059_Kepler   RNA   \n",
       "28946          X  21329937  21329937        X_21329937_21329937_Doc   RNA   \n",
       "\n",
       "      Order SuperFamily     Family TE_present_in_REF  \\\n",
       "0       TIR  TcMar-Pogo       pogo               YES   \n",
       "1      LINE      Jockey         BS               YES   \n",
       "2      LINE      Jockey        Doc               YES   \n",
       "3      LINE      Jockey         G2               YES   \n",
       "4      LINE      Jockey        BS2               YES   \n",
       "...     ...         ...        ...               ...   \n",
       "28942   TIR           P  P-element                NO   \n",
       "28943  LINE      Jockey       Doc6                NO   \n",
       "28944   TIR   TcMar-Tc1      Bari1                NO   \n",
       "28945  TRIM       Gypsy     Kepler               YES   \n",
       "28946  LINE      Jockey        Doc                NO   \n",
       "\n",
       "       Number_of_genomes_present  \\\n",
       "0                             31   \n",
       "1                             27   \n",
       "2                              1   \n",
       "3                              1   \n",
       "4                             14   \n",
       "...                          ...   \n",
       "28942                          1   \n",
       "28943                         13   \n",
       "28944                          1   \n",
       "28945                         25   \n",
       "28946                          1   \n",
       "\n",
       "                                                 Genomes  \\\n",
       "0      ORE;B6;B4;JUT-008;MUN-008;AB8;A3;B2;GIM-012;AK...   \n",
       "1      ORE;B3;JUT-008;AB8;MUN-013;A3;B2;JUT-011;TEN-0...   \n",
       "2                                                  ISO-1   \n",
       "3                                                  ISO-1   \n",
       "4      RAL-426;COR-023;AKA-018;ORE;A6;B6;B4;MUN-008;S...   \n",
       "...                                                  ...   \n",
       "28942                                            MUN-013   \n",
       "28943  RAL-426;COR-023;AKA-018;GIM-024;A6;TOM-008;TOM...   \n",
       "28944                                            JUT-008   \n",
       "28945  ORE;A6;B6;B3;MUN-008;AKA-017;A3;B2;GIM-012;JUT...   \n",
       "28946                                                 B2   \n",
       "\n",
       "                                       TE_name_in_strain  \\\n",
       "0      ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...   \n",
       "1      ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...   \n",
       "2                                            FBti0059794   \n",
       "3                                            FBti0019149   \n",
       "4      ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...   \n",
       "...                                                  ...   \n",
       "28942                             MUN-013_2268_P-element   \n",
       "28943  A6_2230_Doc6;MUN-013_2269_Doc6;AKA-018_2198_Do...   \n",
       "28944                                 JUT-008_2026_Bari1   \n",
       "28945  ORE_2050_Kepler;A6_2231_Kepler;B6_2089_Kepler;...   \n",
       "28946                                        B2_2211_Doc   \n",
       "\n",
       "                                             TE_length_c  \n",
       "0      2122;2122;2122;2118;2120;2123;2122;2122;2127;2...  \n",
       "1      125;126;125;125;125;125;124;125;126;124;125;12...  \n",
       "2                                                   3611  \n",
       "3                                                   2365  \n",
       "4      2806;2872;2871;2872;2872;2872;2869;2869;2872;2...  \n",
       "...                                                  ...  \n",
       "28942                                               1800  \n",
       "28943    220;220;220;220;220;220;136;219;220;220;220;220  \n",
       "28944                                               1733  \n",
       "28945  134;134;130;134;134;134;134;134;134;134;126;13...  \n",
       "28946                                               4723  \n",
       "\n",
       "[28947 rows x 13 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>Chromosome</th>\n      <th>Start</th>\n      <th>End</th>\n      <th>TE_name</th>\n      <th>Class</th>\n      <th>Order</th>\n      <th>SuperFamily</th>\n      <th>Family</th>\n      <th>TE_present_in_REF</th>\n      <th>Number_of_genomes_present</th>\n      <th>Genomes</th>\n      <th>TE_name_in_strain</th>\n      <th>TE_length_c</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2L</td>\n      <td>2933354</td>\n      <td>2935475</td>\n      <td>FBti0019112</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>TcMar-Pogo</td>\n      <td>pogo</td>\n      <td>YES</td>\n      <td>31</td>\n      <td>ORE;B6;B4;JUT-008;MUN-008;AB8;A3;B2;GIM-012;AK...</td>\n      <td>ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...</td>\n      <td>2122;2122;2122;2118;2120;2123;2122;2122;2127;2...</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2L</td>\n      <td>7579255</td>\n      <td>7579380</td>\n      <td>FBti0019133</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS</td>\n      <td>YES</td>\n      <td>27</td>\n      <td>ORE;B3;JUT-008;AB8;MUN-013;A3;B2;JUT-011;TEN-0...</td>\n      <td>ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...</td>\n      <td>125;126;125;125;125;125;124;125;126;124;125;12...</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2L</td>\n      <td>11215132</td>\n      <td>11218743</td>\n      <td>FBti0059794</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>ISO-1</td>\n      <td>FBti0059794</td>\n      <td>3611</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>2L</td>\n      <td>11315294</td>\n      <td>11317659</td>\n      <td>FBti0019149</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>G2</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>ISO-1</td>\n      <td>FBti0019149</td>\n      <td>2365</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>2L</td>\n      <td>11897168</td>\n      <td>11900029</td>\n      <td>FBti0019153</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS2</td>\n      <td>YES</td>\n      <td>14</td>\n      <td>RAL-426;COR-023;AKA-018;ORE;A6;B6;B4;MUN-008;S...</td>\n      <td>ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...</td>\n      <td>2806;2872;2871;2872;2872;2872;2869;2869;2872;2...</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>28942</th>\n      <td>X</td>\n      <td>21319389</td>\n      <td>21319389</td>\n      <td>X_21319389_21319389_P-element</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>P</td>\n      <td>P-element</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>MUN-013</td>\n      <td>MUN-013_2268_P-element</td>\n      <td>1800</td>\n    </tr>\n    <tr>\n      <th>28943</th>\n      <td>X</td>\n      <td>21322782</td>\n      <td>21322803</td>\n      <td>X_21322782_21322803_Doc6</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc6</td>\n      <td>NO</td>\n      <td>13</td>\n      <td>RAL-426;COR-023;AKA-018;GIM-024;A6;TOM-008;TOM...</td>\n      <td>A6_2230_Doc6;MUN-013_2269_Doc6;AKA-018_2198_Do...</td>\n      <td>220;220;220;220;220;220;136;219;220;220;220;220</td>\n    </tr>\n    <tr>\n      <th>28944</th>\n      <td>X</td>\n      <td>21328226</td>\n      <td>21328226</td>\n      <td>X_21328226_21328226_Bari1</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>TcMar-Tc1</td>\n      <td>Bari1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>JUT-008</td>\n      <td>JUT-008_2026_Bari1</td>\n      <td>1733</td>\n    </tr>\n    <tr>\n      <th>28945</th>\n      <td>X</td>\n      <td>21329021</td>\n      <td>21329155</td>\n      <td>ISO1_2059_Kepler</td>\n      <td>RNA</td>\n      <td>TRIM</td>\n      <td>Gypsy</td>\n      <td>Kepler</td>\n      <td>YES</td>\n      <td>25</td>\n      <td>ORE;A6;B6;B3;MUN-008;AKA-017;A3;B2;GIM-012;JUT...</td>\n      <td>ORE_2050_Kepler;A6_2231_Kepler;B6_2089_Kepler;...</td>\n      <td>134;134;130;134;134;134;134;134;134;134;126;13...</td>\n    </tr>\n    <tr>\n      <th>28946</th>\n      <td>X</td>\n      <td>21329937</td>\n      <td>21329937</td>\n      <td>X_21329937_21329937_Doc</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>B2</td>\n      <td>B2_2211_Doc</td>\n      <td>4723</td>\n    </tr>\n  </tbody>\n</table>\n<p>28947 rows × 13 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 284
    }
   ],
   "source": [
    "df_TE_reduced= df_TE[['Chromosome', 'Start', 'End', 'TE_name','Class', 'Order','SuperFamily','Family', 'TE_present_in_REF',\n",
    "       'Number_of_genomes_present', 'Genomes', 'TE_name_in_strain','TE_length_c']].copy()\n",
    "df_TE_reduced"
   ]
  },
  {
   "source": [
    "# here add in all the TEs that are only present in Long genomes!!! The result of the intersect above"
   ],
   "cell_type": "markdown",
   "metadata": {}
  },
  {
   "cell_type": "code",
   "execution_count": 285,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_long_TEs = pd.read_csv(f'unique_Long_TEs.bed', sep='\\t', header=None, names=['Chromosome','Start','End','TE_name', 'Family','Genomes'])\n",
    "df_long_TEs= df_long_TEs.drop_duplicates()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 286,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_long_TEs['Class']= np.nan\n",
    "df_long_TEs['Order']= np.nan\n",
    "df_long_TEs['SuperFamily']= np.nan\n",
    "df_long_TEs['TE_present_in_REF']= 'NO'\n",
    "df_long_TEs['Number_of_genomes_present']= 1\n",
    "df_long_TEs['TE_name_in_strain']= np.nan\n",
    "df_long_TEs['TE_length_c']= ((df_long_TEs['End']) - (df_long_TEs['Start'])).abs()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 287,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_long_TEs = df_long_TEs[['Chromosome','Start','End','TE_name','Class','Order','SuperFamily','Family','TE_present_in_REF','Number_of_genomes_present','Genomes',\\\n",
    "     'TE_name_in_strain','TE_length_c']].copy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 288,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "     Chromosome     Start       End             TE_name  Class  Order  \\\n",
       "0            2L    955585    956077         I23_22_LARD    NaN    NaN   \n",
       "1            2L   1119341   1119341    I23_25_P-element    NaN    NaN   \n",
       "2            2L   1140703   1140703    I23_26_Quasimodo    NaN    NaN   \n",
       "3            2L   1179769   1179769          I23_27_Doc    NaN    NaN   \n",
       "4            2L   1346790   1346790         I23_31_Rt1b    NaN    NaN   \n",
       "...         ...       ...       ...                 ...    ...    ...   \n",
       "6066          X  22641316  22641395       ZH26_5715_Tc1    NaN    NaN   \n",
       "6067          X  22641419  22641569      ZH26_5716_Tom1    NaN    NaN   \n",
       "6068          X  22642074  22642451     ZH26_5717_INE-1    NaN    NaN   \n",
       "6069          X  22644337  22644928    ZH26_5718_jockey    NaN    NaN   \n",
       "6070          X  22645829  22646208  ZH26_5719_Invader3    NaN    NaN   \n",
       "\n",
       "      SuperFamily     Family TE_present_in_REF  Number_of_genomes_present  \\\n",
       "0             NaN       LARD                NO                          1   \n",
       "1             NaN  P-element                NO                          1   \n",
       "2             NaN  Quasimodo                NO                          1   \n",
       "3             NaN        Doc                NO                          1   \n",
       "4             NaN       Rt1b                NO                          1   \n",
       "...           ...        ...               ...                        ...   \n",
       "6066          NaN        Tc1                NO                          1   \n",
       "6067          NaN       Tom1                NO                          1   \n",
       "6068          NaN      INE-1                NO                          1   \n",
       "6069          NaN     jockey                NO                          1   \n",
       "6070          NaN   Invader3                NO                          1   \n",
       "\n",
       "     Genomes  TE_name_in_strain  TE_length_c  \n",
       "0        I23                NaN          492  \n",
       "1        I23                NaN            0  \n",
       "2        I23                NaN            0  \n",
       "3        I23                NaN            0  \n",
       "4        I23                NaN            0  \n",
       "...      ...                ...          ...  \n",
       "6066    ZH26                NaN           79  \n",
       "6067    ZH26                NaN          150  \n",
       "6068    ZH26                NaN          377  \n",
       "6069    ZH26                NaN          591  \n",
       "6070    ZH26                NaN          379  \n",
       "\n",
       "[5795 rows x 13 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>Chromosome</th>\n      <th>Start</th>\n      <th>End</th>\n      <th>TE_name</th>\n      <th>Class</th>\n      <th>Order</th>\n      <th>SuperFamily</th>\n      <th>Family</th>\n      <th>TE_present_in_REF</th>\n      <th>Number_of_genomes_present</th>\n      <th>Genomes</th>\n      <th>TE_name_in_strain</th>\n      <th>TE_length_c</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2L</td>\n      <td>955585</td>\n      <td>956077</td>\n      <td>I23_22_LARD</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>LARD</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>I23</td>\n      <td>NaN</td>\n      <td>492</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2L</td>\n      <td>1119341</td>\n      <td>1119341</td>\n      <td>I23_25_P-element</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>P-element</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>I23</td>\n      <td>NaN</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2L</td>\n      <td>1140703</td>\n      <td>1140703</td>\n      <td>I23_26_Quasimodo</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Quasimodo</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>I23</td>\n      <td>NaN</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>2L</td>\n      <td>1179769</td>\n      <td>1179769</td>\n      <td>I23_27_Doc</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Doc</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>I23</td>\n      <td>NaN</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>2L</td>\n      <td>1346790</td>\n      <td>1346790</td>\n      <td>I23_31_Rt1b</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Rt1b</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>I23</td>\n      <td>NaN</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>6066</th>\n      <td>X</td>\n      <td>22641316</td>\n      <td>22641395</td>\n      <td>ZH26_5715_Tc1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Tc1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>79</td>\n    </tr>\n    <tr>\n      <th>6067</th>\n      <td>X</td>\n      <td>22641419</td>\n      <td>22641569</td>\n      <td>ZH26_5716_Tom1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Tom1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>150</td>\n    </tr>\n    <tr>\n      <th>6068</th>\n      <td>X</td>\n      <td>22642074</td>\n      <td>22642451</td>\n      <td>ZH26_5717_INE-1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>INE-1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>377</td>\n    </tr>\n    <tr>\n      <th>6069</th>\n      <td>X</td>\n      <td>22644337</td>\n      <td>22644928</td>\n      <td>ZH26_5718_jockey</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>jockey</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>591</td>\n    </tr>\n    <tr>\n      <th>6070</th>\n      <td>X</td>\n      <td>22645829</td>\n      <td>22646208</td>\n      <td>ZH26_5719_Invader3</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Invader3</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>379</td>\n    </tr>\n  </tbody>\n</table>\n<p>5795 rows × 13 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 288
    }
   ],
   "source": [
    "df_long_TEs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 289,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_ALL_TEs= pd.concat([df_TE_reduced,df_long_TEs], axis=0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 290,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "     Chromosome     Start       End             TE_name Class Order  \\\n",
       "0            2L   2933354   2935475         FBti0019112   DNA   TIR   \n",
       "1            2L   7579255   7579380         FBti0019133   RNA  LINE   \n",
       "2            2L  11215132  11218743         FBti0059794   RNA  LINE   \n",
       "3            2L  11315294  11317659         FBti0019149   RNA  LINE   \n",
       "4            2L  11897168  11900029         FBti0019153   RNA  LINE   \n",
       "...         ...       ...       ...                 ...   ...   ...   \n",
       "6066          X  22641316  22641395       ZH26_5715_Tc1   NaN   NaN   \n",
       "6067          X  22641419  22641569      ZH26_5716_Tom1   NaN   NaN   \n",
       "6068          X  22642074  22642451     ZH26_5717_INE-1   NaN   NaN   \n",
       "6069          X  22644337  22644928    ZH26_5718_jockey   NaN   NaN   \n",
       "6070          X  22645829  22646208  ZH26_5719_Invader3   NaN   NaN   \n",
       "\n",
       "     SuperFamily    Family TE_present_in_REF  Number_of_genomes_present  \\\n",
       "0     TcMar-Pogo      pogo               YES                         31   \n",
       "1         Jockey        BS               YES                         27   \n",
       "2         Jockey       Doc               YES                          1   \n",
       "3         Jockey        G2               YES                          1   \n",
       "4         Jockey       BS2               YES                         14   \n",
       "...          ...       ...               ...                        ...   \n",
       "6066         NaN       Tc1                NO                          1   \n",
       "6067         NaN      Tom1                NO                          1   \n",
       "6068         NaN     INE-1                NO                          1   \n",
       "6069         NaN    jockey                NO                          1   \n",
       "6070         NaN  Invader3                NO                          1   \n",
       "\n",
       "                                                Genomes  \\\n",
       "0     ORE;B6;B4;JUT-008;MUN-008;AB8;A3;B2;GIM-012;AK...   \n",
       "1     ORE;B3;JUT-008;AB8;MUN-013;A3;B2;JUT-011;TEN-0...   \n",
       "2                                                 ISO-1   \n",
       "3                                                 ISO-1   \n",
       "4     RAL-426;COR-023;AKA-018;ORE;A6;B6;B4;MUN-008;S...   \n",
       "...                                                 ...   \n",
       "6066                                               ZH26   \n",
       "6067                                               ZH26   \n",
       "6068                                               ZH26   \n",
       "6069                                               ZH26   \n",
       "6070                                               ZH26   \n",
       "\n",
       "                                      TE_name_in_strain  \\\n",
       "0     ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...   \n",
       "1     ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...   \n",
       "2                                           FBti0059794   \n",
       "3                                           FBti0019149   \n",
       "4     ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...   \n",
       "...                                                 ...   \n",
       "6066                                                NaN   \n",
       "6067                                                NaN   \n",
       "6068                                                NaN   \n",
       "6069                                                NaN   \n",
       "6070                                                NaN   \n",
       "\n",
       "                                            TE_length_c  \n",
       "0     2122;2122;2122;2118;2120;2123;2122;2122;2127;2...  \n",
       "1     125;126;125;125;125;125;124;125;126;124;125;12...  \n",
       "2                                                  3611  \n",
       "3                                                  2365  \n",
       "4     2806;2872;2871;2872;2872;2872;2869;2869;2872;2...  \n",
       "...                                                 ...  \n",
       "6066                                                 79  \n",
       "6067                                                150  \n",
       "6068                                                377  \n",
       "6069                                                591  \n",
       "6070                                                379  \n",
       "\n",
       "[34742 rows x 13 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>Chromosome</th>\n      <th>Start</th>\n      <th>End</th>\n      <th>TE_name</th>\n      <th>Class</th>\n      <th>Order</th>\n      <th>SuperFamily</th>\n      <th>Family</th>\n      <th>TE_present_in_REF</th>\n      <th>Number_of_genomes_present</th>\n      <th>Genomes</th>\n      <th>TE_name_in_strain</th>\n      <th>TE_length_c</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2L</td>\n      <td>2933354</td>\n      <td>2935475</td>\n      <td>FBti0019112</td>\n      <td>DNA</td>\n      <td>TIR</td>\n      <td>TcMar-Pogo</td>\n      <td>pogo</td>\n      <td>YES</td>\n      <td>31</td>\n      <td>ORE;B6;B4;JUT-008;MUN-008;AB8;A3;B2;GIM-012;AK...</td>\n      <td>ORE_28_pogo;B6_27_pogo;B4_21_pogo;JUT-008_24_p...</td>\n      <td>2122;2122;2122;2118;2120;2123;2122;2122;2127;2...</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2L</td>\n      <td>7579255</td>\n      <td>7579380</td>\n      <td>FBti0019133</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS</td>\n      <td>YES</td>\n      <td>27</td>\n      <td>ORE;B3;JUT-008;AB8;MUN-013;A3;B2;JUT-011;TEN-0...</td>\n      <td>ORE_80_BS;B3_68_BS;JUT-008_72_BS;AB8_87_BS;MUN...</td>\n      <td>125;126;125;125;125;125;124;125;126;124;125;12...</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2L</td>\n      <td>11215132</td>\n      <td>11218743</td>\n      <td>FBti0059794</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>Doc</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>ISO-1</td>\n      <td>FBti0059794</td>\n      <td>3611</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>2L</td>\n      <td>11315294</td>\n      <td>11317659</td>\n      <td>FBti0019149</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>G2</td>\n      <td>YES</td>\n      <td>1</td>\n      <td>ISO-1</td>\n      <td>FBti0019149</td>\n      <td>2365</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>2L</td>\n      <td>11897168</td>\n      <td>11900029</td>\n      <td>FBti0019153</td>\n      <td>RNA</td>\n      <td>LINE</td>\n      <td>Jockey</td>\n      <td>BS2</td>\n      <td>YES</td>\n      <td>14</td>\n      <td>RAL-426;COR-023;AKA-018;ORE;A6;B6;B4;MUN-008;S...</td>\n      <td>ORE_133_BS2;A6_158_BS2;B6_133_BS2;B4_123_BS2;M...</td>\n      <td>2806;2872;2871;2872;2872;2872;2869;2869;2872;2...</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>6066</th>\n      <td>X</td>\n      <td>22641316</td>\n      <td>22641395</td>\n      <td>ZH26_5715_Tc1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Tc1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>79</td>\n    </tr>\n    <tr>\n      <th>6067</th>\n      <td>X</td>\n      <td>22641419</td>\n      <td>22641569</td>\n      <td>ZH26_5716_Tom1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Tom1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>150</td>\n    </tr>\n    <tr>\n      <th>6068</th>\n      <td>X</td>\n      <td>22642074</td>\n      <td>22642451</td>\n      <td>ZH26_5717_INE-1</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>INE-1</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>377</td>\n    </tr>\n    <tr>\n      <th>6069</th>\n      <td>X</td>\n      <td>22644337</td>\n      <td>22644928</td>\n      <td>ZH26_5718_jockey</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>jockey</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>591</td>\n    </tr>\n    <tr>\n      <th>6070</th>\n      <td>X</td>\n      <td>22645829</td>\n      <td>22646208</td>\n      <td>ZH26_5719_Invader3</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>Invader3</td>\n      <td>NO</td>\n      <td>1</td>\n      <td>ZH26</td>\n      <td>NaN</td>\n      <td>379</td>\n    </tr>\n  </tbody>\n</table>\n<p>34742 rows × 13 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 290
    }
   ],
   "source": [
    "df_ALL_TEs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 292,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_ALL_TEs.to_csv('All_TE_sheet.tsv' , index=False,  sep='\\t', header= False)\n",
    "#df_TE_full_columns.to_csv('TE_sheet_full.tsv' , index=False,  sep='\\t', header=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#df_new_tes= df2.groupby([3]).agg({7 :lambda x: ';'.join(x.dropna()), 18 :lambda x: ';'.join(x.dropna()), 16:lambda x: ';'.join(x.dropna())}).reset_index()\n",
    "#df_new_tes.loc[df_new_tes[3]== 'FBti0019372']\n",
    "#df_new_tes= df2.groupby([3]).agg({18:lambda x: ';'.join(x.dropna()), 'new_te':'count'}).reset_index()\n",
    "#df_new_tes = df2.groupby(3)[18].apply(lambda x: list(x) if pd.notna(x[1]) else x ).reset_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 230,
   "metadata": {},
   "outputs": [],
   "source": [
    "def Add_Num_TE(df2):\n",
    "    num_te= df2['new_te'] + df2[9]\n",
    "    return num_te"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 224,
   "metadata": {},
   "outputs": [
    {
     "output_type": "error",
     "ename": "KeyError",
     "evalue": "18",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyError\u001b[0m                                  Traceback (most recent call last)",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/indexes/base.py\u001b[0m in \u001b[0;36mget_loc\u001b[0;34m(self, key, method, tolerance)\u001b[0m\n\u001b[1;32m   3079\u001b[0m             \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 3080\u001b[0;31m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_engine\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_loc\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcasted_key\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   3081\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0merr\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32mpandas/_libs/index.pyx\u001b[0m in \u001b[0;36mpandas._libs.index.IndexEngine.get_loc\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;32mpandas/_libs/index.pyx\u001b[0m in \u001b[0;36mpandas._libs.index.IndexEngine.get_loc\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;32mpandas/_libs/hashtable_class_helper.pxi\u001b[0m in \u001b[0;36mpandas._libs.hashtable.Int64HashTable.get_item\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;32mpandas/_libs/hashtable_class_helper.pxi\u001b[0m in \u001b[0;36mpandas._libs.hashtable.Int64HashTable.get_item\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;31mKeyError\u001b[0m: 18",
      "\nThe above exception was the direct cause of the following exception:\n",
      "\u001b[0;31mKeyError\u001b[0m                                  Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-224-f9e4443c883a>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mdf_TE\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'NEW'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m=\u001b[0m \u001b[0mdf2\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mNew_TE_List\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0maxis\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0mdf_TE\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'NEW-1'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m=\u001b[0m \u001b[0mdf2\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mAdd_Num_TE\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0maxis\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0mdf_TE\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/frame.py\u001b[0m in \u001b[0;36mapply\u001b[0;34m(self, func, axis, raw, result_type, args, **kwds)\u001b[0m\n\u001b[1;32m   7766\u001b[0m             \u001b[0mkwds\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mkwds\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   7767\u001b[0m         )\n\u001b[0;32m-> 7768\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mop\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_result\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   7769\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   7770\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mapplymap\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mfunc\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mna_action\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mOptional\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mstr\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m->\u001b[0m \u001b[0mDataFrame\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/apply.py\u001b[0m in \u001b[0;36mget_result\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    183\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply_raw\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    184\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 185\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply_standard\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    186\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    187\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mapply_empty_result\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/apply.py\u001b[0m in \u001b[0;36mapply_standard\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    274\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    275\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mapply_standard\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 276\u001b[0;31m         \u001b[0mresults\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mres_index\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapply_series_generator\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    277\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    278\u001b[0m         \u001b[0;31m# wrap results\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/apply.py\u001b[0m in \u001b[0;36mapply_series_generator\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    288\u001b[0m             \u001b[0;32mfor\u001b[0m \u001b[0mi\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mv\u001b[0m \u001b[0;32min\u001b[0m \u001b[0menumerate\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mseries_gen\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    289\u001b[0m                 \u001b[0;31m# ignore SettingWithCopy here in case the user mutates\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 290\u001b[0;31m                 \u001b[0mresults\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mf\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mv\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    291\u001b[0m                 \u001b[0;32mif\u001b[0m \u001b[0misinstance\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mresults\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mABCSeries\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    292\u001b[0m                     \u001b[0;31m# If we have a view on v, we need to make a copy because\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m<ipython-input-223-c15a567c0afc>\u001b[0m in \u001b[0;36mNew_TE_List\u001b[0;34m(df2)\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mdef\u001b[0m \u001b[0mNew_TE_List\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mdf2\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m     \u001b[0;32mif\u001b[0m \u001b[0mdf\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m18\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m!=\u001b[0m \u001b[0;34m''\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m         \u001b[0mnew_te_list\u001b[0m\u001b[0;34m=\u001b[0m \u001b[0;34m';'\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0mdf2\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m18\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mnew_te_list\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/frame.py\u001b[0m in \u001b[0;36m__getitem__\u001b[0;34m(self, key)\u001b[0m\n\u001b[1;32m   3022\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolumns\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mnlevels\u001b[0m \u001b[0;34m>\u001b[0m \u001b[0;36m1\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   3023\u001b[0m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_getitem_multilevel\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 3024\u001b[0;31m             \u001b[0mindexer\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolumns\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_loc\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   3025\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mis_integer\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mindexer\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   3026\u001b[0m                 \u001b[0mindexer\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mindexer\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/indexes/base.py\u001b[0m in \u001b[0;36mget_loc\u001b[0;34m(self, key, method, tolerance)\u001b[0m\n\u001b[1;32m   3080\u001b[0m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_engine\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_loc\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcasted_key\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   3081\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0merr\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 3082\u001b[0;31m                 \u001b[0;32mraise\u001b[0m \u001b[0mKeyError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0merr\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   3083\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   3084\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mtolerance\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mKeyError\u001b[0m: 18"
     ]
    }
   ],
   "source": [
    "df_TE['NEW']= df2.apply(New_TE_List, axis=1)\n",
    "df_TE['NEW-1']= df2.apply(Add_Num_TE, axis=1)\n",
    "df_TE"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 187,
   "metadata": {},
   "outputs": [
    {
     "output_type": "error",
     "ename": "ValueError",
     "evalue": "'lambda x: ';'.join(x)' is not a valid function name for transform(name)",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-187-610f4f31fa1f>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mdf2\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'new_te_sample_list'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdf2\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mgroupby\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m3\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m18\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtransform\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"lambda x: ';'.join(x)\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m/opt/anaconda3/lib/python3.7/site-packages/pandas/core/groupby/generic.py\u001b[0m in \u001b[0;36mtransform\u001b[0;34m(self, func, engine, engine_kwargs, *args, **kwargs)\u001b[0m\n\u001b[1;32m    509\u001b[0m         \u001b[0;32melif\u001b[0m \u001b[0mfunc\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mbase\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtransform_kernel_allowlist\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    510\u001b[0m             \u001b[0mmsg\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34mf\"'{func}' is not a valid function name for transform(name)\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 511\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mValueError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmsg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    512\u001b[0m         \u001b[0;32melif\u001b[0m \u001b[0mfunc\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mbase\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcythonized_kernels\u001b[0m \u001b[0;32mor\u001b[0m \u001b[0mfunc\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mbase\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtransformation_kernels\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    513\u001b[0m             \u001b[0;31m# cythonized transform or canned \"agg+broadcast\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mValueError\u001b[0m: 'lambda x: ';'.join(x)' is not a valid function name for transform(name)"
     ]
    }
   ],
   "source": [
    "#df2['new_te_sample_list']=df2.groupby(3)[18].transform(\"lambda x: ';'.join(x)\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 186,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "                                                 18  new_te\n",
       "3                                                          \n",
       "2L_10176485_10176487_Idefix                     B59       1\n",
       "2L_11126167_11126167_pogo                      T29A       1\n",
       "2L_11792426_11792426_mdg1                      T29A       1\n",
       "2L_12351194_12351194_Rt1b                       N25       1\n",
       "2L_13317534_13317536_BS2                        B59       1\n",
       "2L_13606470_13606470_G2                         B59       1\n",
       "2L_13742399_13742399_Bari1                     T29A       1\n",
       "2L_1379990_1379990_Ivk                          B59       1\n",
       "2L_13931970_13932024_jockey                     N25       1\n",
       "2L_14723046_14723062_F-element                  N25       1\n",
       "2L_14723046_14723062_F-element.t1               N25       1\n",
       "2L_15142274_15142293_BS                         N25       1\n",
       "2L_15220259_15220261_Invader4                  T29A       1\n",
       "2L_15604201_15604201_mdg1                       N25       1\n",
       "2L_15819760_15819777_gypsy1                     N25       1\n",
       "2L_15833047_15833058_H                          B59       1\n",
       "2L_16067118_16067120_HMS-Beagle2                I23       1\n",
       "2L_16138750_16138823_jockey                     B59       1\n",
       "2L_16636204_16636204_Quasimodo                  N25       1\n",
       "2L_17129562_17129562_Blastopia                 T29A       1\n",
       "2L_17176361_17176361_Copia                      B59       1\n",
       "2L_17574423_17574426_hopper                     I23       1\n",
       "2L_17889370_17889381_accord                     N25       1\n",
       "2L_17932225_17932228_Rt1b                       I23       1\n",
       "2L_2014776_2014799_jockey                      T29A       1\n",
       "2L_2621545_2621550_BS                   I23;B59;N25       3\n",
       "2L_2621545_2621550_BS.t1                I23;B59;N25       3\n",
       "2L_2808074_2808161_P-element                   T29A       1\n",
       "2L_2855406_2855408_jockey                       I23       1\n",
       "2L_4019946_4020014_jockey                       N25       1\n",
       "2L_4179713_4179811_jockey                       N25       1\n",
       "2L_5790910_5790915_FB4                          N25       1\n",
       "2L_5790910_5790915_FB4.t1                       N25       1\n",
       "2L_5800191_5800191_P-element                    B59       1\n",
       "2L_7576633_7576642_P-element                    B59       1\n",
       "2L_779337_779337_Stalker4                       B59       1\n",
       "2L_833286_833289_BS                             N25       1\n",
       "2L_8965416_8965438_Doc6                        T29A       1\n",
       "2L_8965416_8965438_Doc6.t1                     T29A       1\n",
       "2L_8993998_8994000_pogo                         I23       1\n",
       "2L_9376208_9376211_mdg1                         I23       1\n",
       "2R_23329346_23329348_17-6                      T29A       1\n",
       "3R_28951834_28951838_jockey                     I23       1\n",
       "FBti0018880                                 I23;N25       2\n",
       "FBti0018937                                     N25       1\n",
       "FBti0018940                        I23;B59;N25;T29A       4\n",
       "FBti0019056                                 I23;N25       2\n",
       "FBti0019065                                    T29A       1\n",
       "FBti0019079                                     I23       1\n",
       "FBti0019081                                    T29A       1\n",
       "FBti0019082                            B59;N25;T29A       3\n",
       "FBti0019112                            B59;N25;T29A       3\n",
       "FBti0019114                                     I23       1\n",
       "FBti0019124                        I23;B59;N25;T29A       4\n",
       "FBti0019127                        I23;B59;N25;T29A       4\n",
       "FBti0019133                            B59;N25;T29A       3\n",
       "FBti0019134                                B59;T29A       2\n",
       "FBti0019153                                     B59       1\n",
       "FBti0019158                                     B59       1\n",
       "FBti0019164                            B59;N25;T29A       3"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>18</th>\n      <th>new_te</th>\n    </tr>\n    <tr>\n      <th>3</th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>2L_10176485_10176487_Idefix</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_11126167_11126167_pogo</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_11792426_11792426_mdg1</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_12351194_12351194_Rt1b</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_13317534_13317536_BS2</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_13606470_13606470_G2</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_13742399_13742399_Bari1</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_1379990_1379990_Ivk</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_13931970_13932024_jockey</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_14723046_14723062_F-element</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_14723046_14723062_F-element.t1</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_15142274_15142293_BS</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_15220259_15220261_Invader4</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_15604201_15604201_mdg1</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_15819760_15819777_gypsy1</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_15833047_15833058_H</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_16067118_16067120_HMS-Beagle2</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_16138750_16138823_jockey</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_16636204_16636204_Quasimodo</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_17129562_17129562_Blastopia</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_17176361_17176361_Copia</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_17574423_17574426_hopper</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_17889370_17889381_accord</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_17932225_17932228_Rt1b</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_2014776_2014799_jockey</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_2621545_2621550_BS</th>\n      <td>I23;B59;N25</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>2L_2621545_2621550_BS.t1</th>\n      <td>I23;B59;N25</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>2L_2808074_2808161_P-element</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_2855406_2855408_jockey</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_4019946_4020014_jockey</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_4179713_4179811_jockey</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_5790910_5790915_FB4</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_5790910_5790915_FB4.t1</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_5800191_5800191_P-element</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_7576633_7576642_P-element</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_779337_779337_Stalker4</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_833286_833289_BS</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_8965416_8965438_Doc6</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_8965416_8965438_Doc6.t1</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_8993998_8994000_pogo</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2L_9376208_9376211_mdg1</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>2R_23329346_23329348_17-6</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>3R_28951834_28951838_jockey</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0018880</th>\n      <td>I23;N25</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <th>FBti0018937</th>\n      <td>N25</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0018940</th>\n      <td>I23;B59;N25;T29A</td>\n      <td>4</td>\n    </tr>\n    <tr>\n      <th>FBti0019056</th>\n      <td>I23;N25</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <th>FBti0019065</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019079</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019081</th>\n      <td>T29A</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019082</th>\n      <td>B59;N25;T29A</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>FBti0019112</th>\n      <td>B59;N25;T29A</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>FBti0019114</th>\n      <td>I23</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019124</th>\n      <td>I23;B59;N25;T29A</td>\n      <td>4</td>\n    </tr>\n    <tr>\n      <th>FBti0019127</th>\n      <td>I23;B59;N25;T29A</td>\n      <td>4</td>\n    </tr>\n    <tr>\n      <th>FBti0019133</th>\n      <td>B59;N25;T29A</td>\n      <td>3</td>\n    </tr>\n    <tr>\n      <th>FBti0019134</th>\n      <td>B59;T29A</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <th>FBti0019153</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019158</th>\n      <td>B59</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>FBti0019164</th>\n      <td>B59;N25;T29A</td>\n      <td>3</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 186
    }
   ],
   "source": [
    "df_view.head(60)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ]
}