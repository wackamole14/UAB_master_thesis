##############
# CNV2VCF.py 
##############

##  Anthony D Long, UC Irvine, July 2018

## Modified by H. Lindstadt and S.Radio, May 2021

from __future__ import print_function
import os
import subprocess
import sys


#  module load samtools
#  module load enthought_python/7.3.2
#  module load R/3.4.1
#     cutree.R in path
#     install.packages("seqinr") in R
#  symlinks to fasta files for each assembly in "data/"
#  output folder locusseq
#  "clustalo-1.2.4-Ubuntu-x86_64/" directory or path in bin

# sys.argv[1] path to the comSplitter.out file (complete path)
# sys.argv[2] path to the id_file.txt (complete path)
# sys.argv[3] path to the locusseq folder (complete path)
# sys.argv[4] path to the cutTree.R script (complete path)


def extractFasta(strain, chromosome, start, stop):
    # strain = a1,...,b1,...,ab8,ore,iso1
    # chromsome = a1,...,RAL-176 = 2L, 2R, 3L, 3R, X
    # start = bp
    # stop = bp
    wrkdir="/homes/users/hlindstadt/gonzalez_lab/CNV/Assemblies/"
    filename = wrkdir + strain + ".fa"
    if strain == "iso_v31_genome":
        shellCommand = "samtools faidx " + wrkdir + "iso_v31_genome.fasta" + " "+chromosome + ":" + start + "-" + stop
    else:
        if int(start) > int(stop):
            shellCommand = "samtools faidx --reverse-complement --mark-strand no " + filename + " " + chromosome + ":" + stop + "-" + start
        else:
            shellCommand = "samtools faidx " + filename + " " + chromosome + ":" + start + "-" + stop
    proc = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, shell=True, encoding='utf-8') # In all the subproccess we need to add the coding flag to save information as string and no bytes.
    fseq = proc.stdout.read()
    return fseq


# print a header so we have a real vcf file
print("""##fileformat=VCFv4.0
##fileDate=20180212
##alignmentGenome=Dmelr6_v31
##INFO=<ID=FL,Number=1,Type=String,Description="CNV-Q SVs">
##INFO=<ID=NA,Number=1,Type=Integer,Description="Number of Alleles">
##INFO=<ID=XI,Number=1,Type=String,Description="External ID">
##INFO=<ID=CE,Number=1,Type=Integer,Description="Simple Event = 0, Event near complex event = 1, Complex Event = 2">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Haploid Genotype">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    format    TOM008 B59   I23 N25 T29A    ZH26    A1  A2  A3  A4  A5  A6  A7  AB8 B1  B2  B3  B4  B6  ORE AKA018  AKA017  COR014  COR018  COR023  COR025  GIM012  GIM024  JUT008  JUT011  KIE094  LUN004  LUN007  MUN008  MUN009  MUN013  MUN015  MUN016  MUN020  RAL059  RAL091  RAL176  RAL177  RAL375  RAL426  RAL737  RAL855  SLA001  STO022  TEN015  TOM007""")

mystrains = {"B59":1,"I23":2,"N25":3,"T29A":4,"ZH26":5,"A1":6,"A2":7,"A3":8,"A4":9,"A5":10,"A6":11,"A7":12,"AB8":13,"B1":14,"B2":15,"B3":16,"B4":17,"B6":18,\
 "ORE":19,"AKA018":20,"AKA017":21,"COR014":22,"COR018":23,"COR023":24,"COR025":25,"GIM012":26,"GIM024":27,"JUT008":28,"JUT011":29,"KIE094":30,\
  "LUN004":31,"LUN007":32,"MUN008":33,"MUN009":34,"MUN013":35,"MUN015":36,"MUN016":37,"MUN020":38,"RAL059":39,"RAL091":40,"RAL176":41,"RAL177":42,\
   "RAL375":43,"RAL426":44,"RAL737":45,"RAL855":46,"SLA001":47,"STO022":48,"TEN015":49,"TOM007":50,"TOM008":0}


def get_strains_from_id(infile):
    """
    This function retrieve the strains associated with each ID
    """
    id_dict = {}
    for line in open(infile,"r").readlines():
        ids,strains = line.strip().split("\t")
        id_dict[ids] = strains
    return id_dict


id_dict = get_strains_from_id(sys.argv[2])


count = 0
for line in open(sys.argv[1],"r").readlines(): ### PUT THE PATH TO THIS FILE
    genos = [0 for x in range(0,len(mystrains))]
    line=line.rstrip()
    Line = line.split()
    chr = Line[0].strip()  # we changed this here to take into account the correct chromosome names.
    start = Line[1].strip()
    end = Line[2].strip()
    label = chr+'_'+start+'_'+end
    numberDiffs = len(Line[4].split(";"))   # we changed this here to take into account the "error" in our file, doesn't show count correctly  
    flavor = Line[7].split(";")[0].strip()
    externalID = Line[11]
    complexEvent = Line[15]
    output=""
    # chr, pos, id
    print("chr"+chr+"\t"+start+"\t.\t",end='')
    refseq = extractFasta("iso_v31_genome", chr, start, end)
    # ref
    print(''.join(refseq.splitlines()[1:])+"\t",end='')
    if numberDiffs > 1:
        AA={}
        for i in range(numberDiffs):
            tmpstrain = id_dict[Line[11]].split(";")[i].split("_")[0].strip() # change this to get the correct name of the strain
            tmpchr = Line[4].strip().split(";")[i].strip() # add this to ensure we add the chromosome from the strain.
            tmpstart = Line[9].split(";")[i].strip()
            tmpstop = Line[10].split(";")[i].strip()
            tmpFasta = extractFasta(tmpstrain, tmpchr, tmpstart, tmpstop)
            output += '>'+tmpstrain+'.'+tmpFasta[1:]
            seq = ''.join(tmpFasta.splitlines()[1:])
            AA[tmpstrain]=seq
        
        fh = open(sys.argv[3] + "/"+label+".seq","w")
        fh.write(output)
        fh.close()
        # module load module load Clustal-Omega/1.2.1
        #./clustalo-1.2.4-Ubuntu-x86_64 -i test2.fa --outfmt=phy -o test2.phy 
        # ./clustalo-1.2.4-Ubuntu-x86_64 -i test.fa --outfmt=phy -o test.phy --percent-id --force	
        shellCommand = "clustalo -i " + sys.argv[3] + "/" + label + ".seq --outfmt=phy -o "  + sys.argv[3] + "/" + label + ".phy --percent-id --force"
        proc = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        blah = proc.stdout.read()
        #Module load R
        #Rscript --vanilla sillyScript.R iris.txt out.txt
        cutree = sys.argv[4]
        shellCommand2 = "Rscript --vanilla " + cutree + " " + sys.argv[3] + "/" + label + ".phy " + sys.argv[3] + "/" + label + ".lev"
        proc = subprocess.Popen(shellCommand2, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        blah2 = proc.stdout.read()
        
        fh = open(sys.argv[3] + "/" + label + ".lev","r")
        myin = fh.read()
        fh.close()
        #ALT	QUAL	FILTER	INFO	FORMAT	TOM008 B59   I23 N25 T29A    ZH26    A1  A2  A3  A4  A5  A6  A7  AB8 B1  B2  B3  B4  B6  ORE AKA018  AKA017  COR014  COR018  COR023  COR025  GIM012  GIM024  JUT008  JUT011  KIE094  LUN004  LUN007  MUN008  MUN009  MUN013  MUN015  MUN016  MUN020  RAL059  RAL091  RAL176  RAL177  RAL375  RAL426  RAL737  RAL855  SLA001  STO022  TEN015  TOM007
        Myin = myin.split("\t")
        Mynames = Myin[0].split(";")
        Mycut = Myin[1].split(";")
        MyNalleles = int(Myin[2])
        mm = {}
        for i in range(numberDiffs):
          tmpname = Mynames[i].split(".")[0].strip()
          tmpallele = Mycut[i].strip().strip()
          genos[mystrains[tmpname]] = tmpallele
          if tmpallele not in mm:
              mm[tmpallele]=tmpname
        
        if MyNalleles == 1:
          print(AA[mm["1"]]+"\t.\t.\tFL="+flavor+";NA=1;XI="+externalID+";CE="+complexEvent+"\tGT\t",end='')
          print("\t".join(map(str,genos))) # We need to change this because no there are all integeres, so we need to convert it to strings.
        else:
          for i in range(1,MyNalleles):
              print(AA[mm[str(i)]]+",  ",end='')				
          print(AA[mm[str(MyNalleles)]]+"\t.\t.\tFL="+flavor+";NA="+str(MyNalleles)+";XI="+externalID+";CE="+complexEvent+"\tGT\t",end='')
          print("\t".join(map(str,genos))) # We need to change this because no there are all integeres, so we need to convert it to strings.
    else:
        tmpstrain = id_dict[Line[11]].split("_")[0].strip() # change this to get the correct name of the strain
        tmpstart = Line[9].strip()
        tmpstop = Line[10].strip()
        tmpFasta = extractFasta(tmpstrain, chr, tmpstart, tmpstop)
        seq = ''.join(tmpFasta.splitlines()[1:])
        print(seq+"\t.\t.\tFL="+flavor+";NA=1;XI="+externalID+";CE="+complexEvent+"\tGT\t",end='')
        genos[mystrains[tmpstrain]] = "1"
        print("\t".join(map(str,genos))) # We need to change this because no there are all integeres, so we need to convert it to strings.