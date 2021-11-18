import pandas as pd
from pysradb import sraweb
import json
import subprocess
import os



#Function for appending metadata
def get_metadata(id,list,studytype):
     #Retrieve metadata
        df = db.sra_metadata(id,detailed=True)
        df = df.loc[df['run_accession'] == id.replace("\n", "")]
       
        df.insert(len(df.columns),"Title",[title],True)
        df.insert(len(df.columns),"Abstract",[abstract],True)
        df.insert(len(df.columns),"LIBRARY_CONSTRUCTION_PROTOCOL",[lib_info],True)
        df.insert(len(df.columns),"DESIGN_DESCRIPTION",[design],True)
        df.reset_index(drop=True, inplace=True)
        df = pd.concat([df, sample_df], axis=1)
        df.insert(len(df.columns),"SAMPLE_DESCRIPTION",[sample_desc],True)
        df.insert(len(df.columns),"Study Type",[studytype],True)
        ##This will remove duplicate columns. Sometimes SRA outputs these. If not removed will stop concat later.  
        df=df.loc[:,~df.columns.duplicated()]
        list.append(df)               
      
        os.remove("json_temp")



#Read in study_accession IDs
ids=open("SAids",'r')
#Make a list to store run_accession IDs
ra_out=[]
#A temp list
ra=[]
#Load SRA database
db = sraweb.SRAweb()
#Sometimes SRA has issues with data retrieval so this gets around that.
#Make list from ids
for i in ids:
     ra.append(i.replace("\n", ""))
for i in ra:
     try:   
         df = db.sra_metadata(i)
         ra_out.append(df[['run_accession']])
     except:
          ra.append(i)
          continue

ra_out = pd.concat(ra_out)
ra_out = ra_out['run_accession'].to_list()





##Make a list to store metadata
metadata_single_cell=[]
metadata_bulk=[]
metadata_BCR=[]
single_end=[]

#For each RA id
for i in ra_out:
    try:
        #Gather metadata
        outfile=open("json_temp",'w')
        cmd=('efetch -db sra -id ' + i  + ' -format native -json').replace("\n", "")
        result = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = result.communicate()
        out=out.decode("utf-8")
        outfile.write(out+'\n')
        outfile.close()
        with open('json_temp') as json_file:
           data = json.load(json_file)
           try:
               #Title
               title = (data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['STUDY']['DESCRIPTOR']['STUDY_TITLE'])
           except:
               title="none"
           try:
               #Source
               source = (data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['EXPERIMENT']['DESIGN']['LIBRARY_DESCRIPTOR']['LIBRARY_SOURCE'])
           except:
               source="none"            
           try:
               #study abstract
               abstract = (data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['STUDY']['DESCRIPTOR']['STUDY_ABSTRACT'])
           except:
               abstract = "none"
           try:
               #LIBRARY_CONSTRUCTION_PROTOCOL
               lib_info = (data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['EXPERIMENT']['DESIGN']['LIBRARY_DESCRIPTOR']['LIBRARY_CONSTRUCTION_PROTOCOL'])
               if type(lib_info) is dict:
                   lib_info = "none"
           except:
               lib_info="none"

           try:
               #Sample Description
               sample_df = pd.DataFrame()
               sample_data=(data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['SAMPLE']['SAMPLE_ATTRIBUTES']['SAMPLE_ATTRIBUTE'])       
               for x in sample_data:
                   sample_df.insert(len(sample_df.columns),x['TAG'],[x['VALUE']],True)

           except:
               sample_df.insert(len(sample_df.columns),"Sample Info",["None"],True)

           try:
               sample_desc=(data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['SAMPLE']['DESCRIPTION'])
           except:
               sample_desc="none"
           #Study Design
           design = str(data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['EXPERIMENT']['DESIGN']['DESIGN_DESCRIPTION'])
           if design == "{}":
               design = "none"


           #Places to seach key words
           check=design+lib_info+abstract+title+source
           ##Single-Cell RNA-Seq
           sc_words=["Chromium","Single Cell","single-cell","single cell","Single-cell","Single cell","SINGLE CELL"]
           if any(word in check for word in sc_words):
               get_metadata(i, metadata_single_cell,"Single-Cell RNA-Seq")
           ##Other
           elif "BCR" in check:
               get_metadata(i, metadata_BCR,"BCR RNA-Seq")

           ##Bulk RNA-Seq
           else:
                 get_metadata(i, metadata_bulk,"Bulk RNA-Seq")
    #If eftech doesnt work for some unknown reason, whitch it often does, append the id to bottom of list so that it will be ran through again.             
    except:          
          ra_out.append(i)
          continue



try:
    metadata_single_cell = pd.concat(metadata_single_cell)
    metadata_single_cell.to_csv("single_cell.metadata.tsv",mode="w", header=True,index=False,sep="\t")

except: pass
try:
    metadata_bulk = pd.concat(metadata_bulk)
    metadata_bulk.to_csv("bulk.metadata.tsv",mode="w", header=True,index=False,sep="\t")
except: pass
try:
    metadata_BCR = pd.concat(metadata_BCR)
    metadata_BCR.to_csv("BCR.metadata.tsv",mode="w", header=True,index=False,sep="\t")
except: pass
