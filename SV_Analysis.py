import pandas as pd
import sys
from pybedtools import BedTool
import  pybedtools
import os 

wdir = sys.argv[1] # Path to cnv folder end with /
strain = sys.argv[2]
outdir = wdir + "svmu/" + strain + "/Filtering"
try:
    os.makedirs(outdir)
except:
    print(outdir,"Directory already exist")

genome_path = wdir + "Assemblies/" + strain + ".fa"
# Load euchromatin regions
euchromatin_file = wdir + "Boundaries/euchromatic_boundaries_" + strain + ".bed"

df_euchromatin = pd.read_table(euchromatin_file,sep="\t",header=None,names=["chromosome","start","end"])

# Load SV regions

sv_file = wdir  + "svmu/" + strain + "/sv." + strain + ".txt"

df_sv = pd.read_table(sv_file,sep="\t",header=0)

df_sv = df_sv.dropna()


tempdict = df_euchromatin.to_dict()
euchromatin_dict = {}

for x in range(0,5):
    euchromatin_dict[tempdict["chromosome"][x]] = [tempdict["start"][x],tempdict["end"][x]]


rows=[]
for index,row in df_sv.iterrows():
    if str(row.Q_CHROM) not in ["2L","2R","3L","3R","X"] or  str(row.REF_CHROM) not in ["2L","2R","3L","3R","X"]:
        pass
    else:
        if euchromatin_dict[row.Q_CHROM][0] > row.Q_START or euchromatin_dict[row.Q_CHROM][1] < row.Q_END:
            euchromatin = False
        else:
            euchromatin = True
        rows.append(row.tolist() + [euchromatin])


df_sv = pd.DataFrame(rows,columns=df_sv.columns.tolist()+["Euchromatin"])

# There are coordinate where START > END:

# So in case when is in REF we found that is an error, when cov-r is 0. Solo encontramos valor 0.

# En ese caso son sospechoso así que los filtro:

df_sv = df_sv[~((df_sv["REF_END"]>=df_sv["REF_START"]) & (df_sv["COV_REF"]==0))]


# Posteriormente y por comentarios de mahul, los casos donde COV-R y COV-Q son iguales probablemente sean erroneos, por lo que
# tambien lo filtro.

"for CNVs that have equal coverage in both, the CNVs are not likely to be true. This is why I added the coverage information. They act as additional information that can help you to pull out questionable calls . Having said that, that is a bug. If you are running the latest version from GitHub, I can take a look to see what the bug is."

rows = []
for index,row in df_sv.iterrows():
    flag = True
    if row.COV_REF == row.COV_Q:
        if row.SV_TYPE in ["CNV-Q","nCNV-Q","CNV-R","nCNV-R"]:
            flag = False
    if flag:
        rows.append(row.tolist())

df_sv = pd.DataFrame(rows,columns=df_sv.columns.tolist())
df_sv["ID"] = [ x for x in range(1,len(df_sv)+1)]
df_sv["ID"] = df_sv["ID"].astype(int)

## When SV TYPE is CNV-R but  COV-R > COV-Q, we change assignments we change sv type to CNV-Q. And viceversa.
# Mahul said:

"I think this is a bug too. In complex genomic regions, where you may have repetitive DNA in both genomes, the approach  I use to call CNVs may sometimes misassign the CNV-R as CNV-Q and vice versa. As before, you can use the coverage to change these assignments."


rows = []
for index,row in df_sv.iterrows():
    invert_assigment = "NO"
    if row.SV_TYPE in ["CNV-Q","nCNV-Q","CNV-R","nCNV-R"]:
        if row.SV_TYPE == "CNV-Q" and row.COV_Q > row.COV_REF:
            invert_assigment = "YES"
        elif row.SV_TYPE == "nCNV-Q" and row.COV_Q > row.COV_REF:
            invert_assigment = "YES"
        elif row.SV_TYPE == "CNV-R" and row.COV_REF > row.COV_Q:
            invert_assigment = "YES"
        elif row.SV_TYPE == "nCNV-R" and row.COV_REF > row.COV_Q:
            invert_assigment = "YES"
    if invert_assigment == "YES":
        pass # todos los casos que analizamos son falsos
    else:
        rows.append(row.tolist())

df_sv = pd.DataFrame(rows,columns=df_sv.columns.tolist())

temp_sv_file = outdir + "/SV_temp.bed"
df_sv.to_csv(temp_sv_file,sep="\t",index=False,header=False)


## Ahora separo en dos uno para REF y otro para QUERY


df_sv_query = df_sv[["Q_CHROM","Q_START","Q_END","SV_TYPE","ID"]]

rows = []
for index,row in df_sv_query.iterrows():
    if row.Q_END < row.Q_START:
        row.Q_END,row.Q_START = row.Q_START,row.Q_END
    rows.append(row.tolist())

df_sv_query = pd.DataFrame(rows,columns=df_sv_query.columns.tolist())


df_sv_query = df_sv_query.sort_values(["Q_CHROM","Q_START","Q_END"])

df_sv_ref = df_sv[["REF_CHROM","REF_START","REF_END","SV_TYPE","ID"]]
df_sv_ref = df_sv_ref.sort_values(["REF_CHROM","REF_START","REF_END"])

temp_qsv_file = outdir + "/QSV_temp.bed"
df_sv_query.to_csv(temp_qsv_file,sep="\t",index=False,header=False)

temp_rsv_file = outdir + "/RSV_temp.bed"
df_sv_ref.to_csv(temp_rsv_file,sep="\t",index=False,header=False)

# OVERLAP QUERY SV and QUERY TE

teq_file = wdir + "TEAnnot/" + strain + ".GenesAllClosestGenes.bed.bed"


qsv = BedTool(temp_qsv_file)
qtes = BedTool(teq_file)

sv_and_tes_query = qsv.intersect(qtes,wao =True)

df_q_sv_te = sv_and_tes_query.to_dataframe(header=None,names=df_sv_query.columns.tolist() + ["TE_CHROM","TE_START","TE_END","QTE_NAME","QTE_SIZE","TE_STRAND","QTE_OVERLAP"])[["ID","QTE_NAME","QTE_SIZE","QTE_OVERLAP"]]


rows = []
for name,grp in df_q_sv_te.groupby("ID"):
    QTE_NAME = ";".join(grp.QTE_NAME.tolist())
    QTE_OVERLAP = ";".join(map(str,grp.QTE_OVERLAP.tolist()))
    ID = name
    QTE_SIZE = ";".join(map(str,grp.QTE_SIZE.tolist()))
    rows.append([ID,QTE_NAME,QTE_SIZE,QTE_OVERLAP])

df_q_sv_te = pd.DataFrame(rows,columns=["ID","QTE_NAME","QTE_SIZE","QTE_OVERLAP"])


# OVERLAP REF SV and REF TE


# ter_file = "/homes/users/sradio/scratch/eQTL_Dros/TEs_genomes_annotation/minimap2/TE_Annotation/ISO1_TE_FlyBase_Repet.bed"
#
# df_te_ref = pd.read_table(ter_file,sep="\t",header=None,names=["TE_CHROM","TE_START","TE_END","RTE_NAME","RTE_SIZE","TE_STRAND"])
#
# df_te_ref["RTE_SIZE"] = df_te_ref["TE_END"]-df_te_ref["TE_START"]
#
# df_te_ref.to_csv(wdir + "refrence_TE.bed",sep="\t",index=False,header=False)


ter_file = wdir + "reference_TE.bed"

rsv = BedTool(temp_rsv_file)
rtes = BedTool(ter_file)

sv_and_tes_ref = rsv.intersect(rtes,wao = True)

df_r_sv_te = sv_and_tes_ref.to_dataframe(header=None,names=df_sv_ref.columns.tolist() + ["TE_CHROM","TE_START","TE_END","RTE_NAME","RTE_SIZE","TE_STRAND","RTE_OVERLAP"])[["ID","RTE_NAME","RTE_SIZE","RTE_OVERLAP"]]

rows = []
for name,grp in df_r_sv_te.groupby("ID"):
    RTE_NAME = ";".join(grp.RTE_NAME.tolist())
    RTE_OVERLAP = ";".join(map(str,grp.RTE_OVERLAP.tolist()))
    ID = name
    RTE_SIZE = ";".join(map(str,grp.RTE_SIZE.tolist()))
    rows.append([ID,RTE_NAME,RTE_SIZE,RTE_OVERLAP])

df_r_sv_te = pd.DataFrame(rows,columns=["ID","RTE_NAME","RTE_SIZE","RTE_OVERLAP"])



### OVERLAP QUERY SV and QUERY GENE

geneq_file = wdir + "liftoff/" + strain + "/" + strain +  "_liftoff"

df_gene_q = pd.read_table(geneq_file,sep="\t",header=None,names=["GENE_CHR","source","feature","GENE_START","GENE_END","frame","strand","score","attribute"])

df_gene_q = df_gene_q[df_gene_q.feature=="gene"]

df_gene_q["GENE_ID"] = df_gene_q.attribute.str.split(";").str[0].str.replace("gene_id=","")
df_gene_q["GENE_NAME"] = df_gene_q.attribute.str.split(";").str[1].str.replace("gene_symbol=","")
df_gene_q["GENE_SIZE"] = df_gene_q["GENE_END"] - df_gene_q["GENE_START"]

df_gene_q = df_gene_q[["GENE_CHR","GENE_START","GENE_END","GENE_SIZE","GENE_ID","GENE_NAME"]]


df_gene_q.to_csv(wdir + "liftoff/" + strain + "/"  + strain + "_gene_mapped_features.bed",sep="\t",index=False,header=False)

# BEDTOOLS INTERESECT

geneq_file = wdir + "liftoff/" + strain + "/"  + strain + "_gene_mapped_features.bed"


qsv = BedTool(temp_qsv_file)
qgenes = BedTool(geneq_file)

sv_and_genes_query = qsv.intersect(qgenes,wao =True)

df_q_sv_gene = sv_and_genes_query.to_dataframe(header=None,names=df_sv_query.columns.tolist() + ["GENE_CHR","GENE_START","GENE_END","QGENE_SIZE","QGENE_ID","QGENE_NAME","QGENE_OVERLAP"])[["ID","QGENE_ID","QGENE_NAME","QGENE_SIZE","QGENE_OVERLAP"]]

rows = []
for name,grp in df_q_sv_gene.groupby("ID"):
    QGENE_NAME = ";".join(map(str,grp.QGENE_NAME.tolist()))
    QGENE_OVERLAP = ";".join(map(str,grp.QGENE_OVERLAP.tolist()))
    ID = name
    QGENE_ID = ";".join(map(str,grp.QGENE_ID.tolist()))
    QGENE_SIZE = ";".join(map(str,grp.QGENE_SIZE.tolist()))
    rows.append([ID,QGENE_ID,QGENE_NAME,QGENE_SIZE,QGENE_OVERLAP])

df_q_sv_gene = pd.DataFrame(rows,columns=["ID","QGENE_ID","QGENE_NAME","QGENE_SIZE","QGENE_OVERLAP"])


### OVERLAP REF SV and REF GENE

### EDIT REF GFF


# gener_file = "/homes/users/sradio/scratch/eQTL_Dros/TEs_genomes_annotation/minimap2/Annotation_Files/dmel-all-r6.31.gtf"

# df_gene_r = pd.read_table(gener_file,sep="\t",header=None,names=["GENE_CHR","source","feature","GENE_START","GENE_END","frame","strand","score","attribute"])

# df_gene_r = df_gene_r[df_gene_r.feature=="gene"]

# df_gene_r["GENE_ID"] = df_gene_r.attribute.str.split(";").str[0].str.replace('gene_id ',"").str.replace('"','')
# df_gene_r["GENE_NAME"] = df_gene_r.attribute.str.split(";").str[1].str.replace('gene_symbol ',"").str.replace('"','')
# df_gene_r["GENE_SIZE"] = df_gene_r["GENE_END"] - df_gene_r["GENE_START"]

# df_gene_r = df_gene_r[["GENE_CHR","GENE_START","GENE_END","GENE_SIZE","GENE_ID","GENE_NAME"]]


# df_gene_r.to_csv(wdir  + "gene_reference.bed",sep="\t",index=False,header=False)

## INTERSECT

gener_file = wdir  + "gene_reference.bed"


rsv = BedTool(temp_rsv_file)
rgenes = BedTool(gener_file)

sv_and_genes_ref = rsv.intersect(rgenes,wao =True)

df_r_sv_gene = sv_and_genes_ref.to_dataframe(header=None,names=df_sv_ref.columns.tolist() + ["GENE_CHR","GENE_START","GENE_END","RGENE_SIZE","RGENE_ID","RGENE_NAME","RGENE_OVERLAP"])[["ID","RGENE_ID","RGENE_NAME","RGENE_SIZE","RGENE_OVERLAP"]]

rows = []
for name,grp in df_r_sv_gene.groupby("ID"):
    RGENE_NAME = ";".join(grp.RGENE_NAME.tolist())
    RGENE_OVERLAP = ";".join(map(str,grp.RGENE_OVERLAP.tolist()))
    ID = name
    RGENE_ID = ";".join(map(str,grp.RGENE_ID.tolist()))
    RGENE_SIZE = ";".join(map(str,grp.RGENE_SIZE.tolist()))
    rows.append([ID,RGENE_ID,RGENE_NAME,RGENE_SIZE,RGENE_OVERLAP])

df_r_sv_gene = pd.DataFrame(rows,columns=["ID","RGENE_ID","RGENE_NAME","RGENE_SIZE","RGENE_OVERLAP"])


### Now I will merge all datasets

df_sv = df_sv.merge(df_q_sv_te,on="ID")
df_sv = df_sv.merge(df_r_sv_te,on="ID")

df_sv = df_sv.merge(df_q_sv_gene,on="ID")
df_sv = df_sv.merge(df_r_sv_gene,on="ID")


# Elimino aquellos determinaciones con longitud menor a 100.


df_sv = df_sv[abs(df_sv["LEN"])>=100]

# Elimino los nCNV ya que no aportan info 

df_sv = df_sv[~df_sv["SV_TYPE"].isin(["nCNV-R","nCNV-Q"])]

# Elimino la region HC 

df_sv = df_sv[df_sv["Euchromatin"]==True]


# Veo las interacciones entre TE para saber cual le creo o no. Primero las veo desde la referencia:

rows = []
for index,row in df_sv.iterrows():
    QTE_SIZE_OVERLAP = 0
    RTE_SIZE_OVERLAP = 0
    if row.SV_TYPE in ["INS","CNV-Q"] and row.QTE_OVERLAP != "0":
        if ";" in row.QTE_OVERLAP:
            ov_te = []
            for i,te_size in enumerate(row.QTE_SIZE.split(";")):
                ov_te +=[round(int(row.QTE_OVERLAP.split(";")[i])*100/int(te_size),1)]
            if max(ov_te) >50:
                QTE_SIZE_OVERLAP = ";".join(map(str,ov_te))
        else:
            if int(row.QTE_OVERLAP)*100/int(row.QTE_SIZE) < 50:
                row.QTE_SIZE = -1
                row.QTE_NAME = "."
                row.QTE_OVERLAP = 0
            else:
                QTE_SIZE_OVERLAP = round(int(row.QTE_OVERLAP)*100/int(row.QTE_SIZE),1)  
    elif row.SV_TYPE in ["DEL","CNV-R"] and row.RTE_OVERLAP != "0":
        if ";" in row.RTE_OVERLAP:
            ov_te = []
            for i,te_size in enumerate(row.RTE_SIZE.split(";")):
                ov_te +=[round(int(row.RTE_OVERLAP.split(";")[i])*100/int(te_size),1)]
            if max(ov_te) >50:
                RTE_SIZE_OVERLAP = ";".join(map(str,ov_te))
            else:
                row.RTE_SIZE = -1
                row.RTE_NAME = "."
                row.RTE_OVERLAP = 0
        else:
            if int(row.RTE_OVERLAP)*100/int(row.RTE_SIZE) < 50:
                pass
            else:
                RTE_SIZE_OVERLAP = round(int(row.RTE_OVERLAP)*100/int(row.RTE_SIZE),1)      
    rows.append(row.tolist() + [QTE_SIZE_OVERLAP,RTE_SIZE_OVERLAP])

df_sv_ = pd.DataFrame(rows,columns=df_sv.columns.tolist() + ["QTE_SIZE_OVERLAP","RTE_SIZE_OVERLAP"])

## Save results

sv_file = outdir + "/" + strain + "_SV_info.tsv"

df_sv_.to_csv(sv_file,sep="\t",index=False,header=True)

## Now I will define count table for three conditions: total, eucrhromatin, heterochromatin

# TOTAL COUNT:

total_ins = len(df_sv[df_sv["SV_TYPE"]=="INS"])
total_del = len(df_sv[df_sv["SV_TYPE"]=="DEL"])
total_qCNV = len(df_sv[df_sv["SV_TYPE"]=="CNV-Q"])
total_rCNV = len(df_sv[df_sv["SV_TYPE"]=="CNV-R"])
total_inv = len(df_sv[df_sv["SV_TYPE"]=="INV"])/2 # En general veo que una inversion se define con dos puntos 


# total count overlap Q TE

QTE_ins   = len(df_sv[(df_sv["SV_TYPE"]=="INS") & (df_sv["QTE_NAME"]!=".")])
QTE_qCNV  = len(df_sv[(df_sv["SV_TYPE"]=="CNV-Q") & (df_sv["QTE_NAME"]!=".")])


# total count overlap REF TE

RTE_del   = len(df_sv[(df_sv["SV_TYPE"]=="DEL") & (df_sv["RTE_NAME"]!=".")])
RTE_rCNV  = len(df_sv[(df_sv["SV_TYPE"]=="CNV-R") & (df_sv["RTE_NAME"]!=".")])


INSERTIONS = total_ins - QTE_ins
DELETION = total_del - RTE_del
INDEL = INSERTIONS + DELETION
TEINS =QTE_ins
TEDEL = RTE_del
QCNV = total_qCNV
RCNV = total_rCNV
CNV = QCNV + RCNV
INV = int(total_inv)


rows = [[INSERTIONS,DELETION,INDEL,TEINS,TEDEL,QCNV,RCNV,CNV,INV]]

colnames = ["INSERTION","DELETION","INDEL","TEINS","TEDEL","CNV_Q","CNV_R","CNV","INV"]

df_SUMMARY = pd.DataFrame(rows,columns=colnames)

### Save Results

sv_file = outdir + "/" + strain + "_SV_PLAN_NACIONAL_summary.tsv"

df_SUMMARY.to_csv(sv_file,sep="\t",index=False,header=True)
