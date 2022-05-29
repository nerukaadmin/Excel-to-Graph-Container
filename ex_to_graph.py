import datetime
import os
import sys
import traceback
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

stamp=datetime.datetime.now()
date=stamp.strftime("%Y-%m-%d")
time=stamp.strftime("%X")

path="./IN"
out_path="./OUT/"
tmp="./tmp/"
files=os.listdir(path)
files_xlsx = [i for i in files if i.endswith('.xlsx')]
if len(files_xlsx) == 0 or len(files_xlsx) > 1:
	print("Oops..! IN DIR error Please check. IN DIR contains either 0 or more than 1 .xlsx file,Please place only latets .xlsx")
else:
	try:
		arg=sys.argv[1]
		if arg == "a":
			print(files_xlsx)
			xl_path=path+"/"+files_xlsx[0]
			read_file=pd.read_excel(xl_path,engine="openpyxl", sheet_name="Data")
			read_file.to_csv (tmp+date+"_temp_.csv",index = None,header=True)
			df = pd.read_csv(tmp+date+"_temp_.csv")
			os.remove(tmp+date+"_temp_.csv")
			inc_count=df[["Assigned to","Priority"]].value_counts()
			total_inc_count=df[["Assigned to"]].value_counts()
			total_inc_count.to_csv(tmp+date+"_total_interm.csv", sep=',', encoding='utf-8',header=False)
			inc_count.to_csv(tmp+date+"_interm.csv", sep=',', encoding='utf-8',header=False)
			col_name_change=['Engieer_Name','Priority','Count']
			tfpd=pd.read_csv(tmp+date+'_interm.csv',sep=',', encoding='utf-8',names=col_name_change)
			
			fpd=tfpd.sort_values('Engieer_Name')
			p1_fdp=fpd[fpd['Priority'] == '1 - Critical']
			p2_fdp=fpd[fpd['Priority'] == '2 - High']
			p3_fdp=fpd[fpd['Priority'] == '3 - Moderate']
			p4_fdp=fpd[fpd['Priority'] == '4 - Low']
			p5_fdp=fpd[fpd['Priority'] == '5 - Planning']
			sheet_list=['Total','1 - Critical','2 - High','3 - Moderate','4 - Low','5 - Planning',]
			df_list=[tfpd,p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
			if not os.path.exists(out_path+date):
				os.makedirs(out_path+date)
			out_dir=out_path+date+"/All/"
			if not os.path.exists(out_dir):
				os.makedirs(out_dir)	
			writer = pd.ExcelWriter(out_dir+date+"_final.xlsx",engine='xlsxwriter')
			for dataframe, sheet in zip(df_list, sheet_list):
				dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
			writer.save()
			fpd.to_csv(out_dir+date+"_final.csv", sep=',', encoding='utf-8',index=False)

			for df_name,plot_name in zip (df_list,sheet_list):
				fig,ax =plt.subplots(figsize=(15, 5))
				plt.rcParams["figure.autolayout"] = True
				bl=ax.bar(df_name['Engieer_Name'],df_name['Count'])
				plt.xticks(rotation='vertical',fontsize ='xx-small')
				ax.set_xlabel('Incident Count')
				ax.set_title('Engineer VS '+plot_name+' Incident')
				ax.bar_label(bl, label_type="edge", padding=3,fontsize ='small')
				plt.savefig(out_dir+plot_name+"-"+date+".png",bbox_inches='tight',dpi=500)
			print("All anaysis reoprt created at %s",out_dir)
			os.remove(tmp+date+"_interm.csv")
			os.remove(tmp+date+"_total_interm.csv")
			os.chmod(out_dir, 0o777)	
		else:
			print(files_xlsx)
			xl_path=path+"/"+files_xlsx[0]
			read_file=pd.read_excel(xl_path,engine="openpyxl", sheet_name="Data")
			read_file.to_csv (tmp+date+"_temp_.csv",index = None,header=True)
			df = pd.read_csv(tmp+date+"_temp_.csv")
			os.remove(tmp+date+"_temp_.csv")
			inc_count=df[["Assigned to","Priority"]].value_counts()
			total_inc_count=df[["Assigned to"]].value_counts()
			total_inc_count.to_csv(tmp+date+"_total_interm.csv", sep=',', encoding='utf-8',header=False)
			inc_count.to_csv(tmp+date+"_interm.csv", sep=',', encoding='utf-8',header=False)
			col_name_change=['Engieer_Name','Priority','Count']
			tfpd=pd.read_csv(tmp+date+'_interm.csv',sep=',', encoding='utf-8',names=col_name_change)
			total_view=['Engieer_Name',"Count"]
			totalfpd=pd.read_csv(tmp+date+'_total_interm.csv',sep=',', encoding='utf-8',names=total_view)
			totalfpd.sort_values('Engieer_Name')
			total_df_list=[totalfpd]
			fpd=tfpd.sort_values('Engieer_Name')
			p1_fdp=fpd[fpd['Priority'] == '1 - Critical']
			p2_fdp=fpd[fpd['Priority'] == '2 - High']
			p3_fdp=fpd[fpd['Priority'] == '3 - Moderate']
			p4_fdp=fpd[fpd['Priority'] == '4 - Low']
			p5_fdp=fpd[fpd['Priority'] == '5 - Planning']
			df_list=[p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
			team=[line.rstrip('\n') for line in open('./team_member_list.txt','r')]
			if len(team) == 0:
				print("Oops..! team_member_list.txt is Empty!")
			else:	
				team_totaL_sort_list=[]
				team_sort_df_list=[]
				print(team)
				for tnm in team:
					for dfl in df_list:
						name=str(tnm)
						sfdp=dfl[dfl['Engieer_Name'] == name ]
						team_sort_df_list.append(sfdp)
				for tnm in team:
					for tdfl in total_df_list:
						name=str(tnm)
						sfdp=tdfl[tdfl['Engieer_Name'] == name ]
						team_totaL_sort_list.append(sfdp)	

				fdft = pd.concat(team_sort_df_list)
				fdfttotal=pd.concat(team_totaL_sort_list)
				print(fdfttotal)
				fpdtf=fdft.sort_values('Engieer_Name')
				p1_fdp=fpdtf[fpdtf['Priority'] == '1 - Critical']
				p2_fdp=fpdtf[fpdtf['Priority'] == '2 - High']
				p3_fdp=fpdtf[fpdtf['Priority'] == '3 - Moderate']
				p4_fdp=fpdtf[fpdtf['Priority'] == '4 - Low']
				p5_fdp=fpdtf[fpdtf['Priority'] == '5 - Planning']
				sheet_list=['Total','1 - Critical','2 - High','3 - Moderate','4 - Low','5 - Planning',]
				df_list=[fdfttotal,p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
				if not os.path.exists(out_path+date):
					os.makedirs(out_path+date)
				out_dir=out_path+date+"/Team/"
				if not os.path.exists(out_dir):
					os.makedirs(out_dir)	
				writer = pd.ExcelWriter(out_dir+date+"_team_final.xlsx",engine='xlsxwriter')
				for dataframe, sheet in zip(df_list, sheet_list):
					dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
				writer.save()
				fpdtf.to_csv(out_dir+date+"_final.csv", sep=',', encoding='utf-8',index=False)
				for df_name,plot_name in zip (df_list,sheet_list):
					y_pos=np.arange(len(df_name['Engieer_Name']))
					fig,ax = plt.subplots(figsize=(10, 5))
					bl=ax.barh(df_name['Engieer_Name'],df_name['Count'],color='#fdaa48')
					#ax.set_yticks(rotation='vertical',fontsize = 'xx-small')
					ax.set_yticks(y_pos, labels=df_name['Engieer_Name'],fontsize ='large')
					ax.invert_yaxis()  # labels read top-to-bottom
					ax.set_xlabel('Incident Count')
					ax.set_title('Engineer VS '+plot_name+' Incident')
					ax.bar_label(bl, label_type="edge", padding=3)
					plt.savefig(out_dir+plot_name+"-"+date+"_team.png",bbox_inches='tight',dpi=500)
				print("Team anaysis reoprt created at %s",out_dir)
				os.remove(tmp+date+"_interm.csv")
				os.remove(tmp+date+"_total_interm.csv")
				os.chmod(out_dir, 0o777)


	except Exception as e:
		#print(e)
		#traceback.print_exc()
		print("Please pass args as for all report -a , for team report -t")		