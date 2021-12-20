#!/usr/bin/python

import sys;
import subprocess;

outputFolder = sys.argv[3];

# Single column
wantedFile = open(sys.argv[1]);
wanted = [line.strip() for line in wantedFile];
wantedFile.close();

pathDict = {};
# BamMap file
matchFile = open(sys.argv[2])
matchFile.readline();
for line in matchFile:
	line = line.strip().split("\t");
	sample = line[0].split(".")[0];
	if sample not in wanted:
		continue;
	if "tumor" in line[4]:
		tissue = "T";
	else:
		tissue = "N";
	pairDir = line[0].split(".")[-2];
	path = line[5];
	if "fastq" not in path:
		continue;
	if sample not in pathDict:
		pathDict[sample] = {"T":{"R1":"","R2":""},"N":{"R1":"","R2":""}};
	pathDict[sample][tissue][pairDir] = path;
matchFile.close();

outputa = open("toRun1_tumor.sh","w");
outputb = open("toRun2_normal.sh","w");
output = open("toRun_tmux.sh","w");
output1 = open("missingSamples.txt","w");
#output2 = open("missingNormalSamples.txt","w");
#output3 = open("availableSamples.txt","w");
for sample in pathDict:
	if sample not in wanted:
		print(sample+"\t"+"noData",file=output2);
		continue;
	elif pathDict[sample]["T"]["R1"] == "" or pathDict[sample]["T"]["R2"] == "":
		print(sample+"\t"+"noTumorData",file=output1);
		subprocess.call("mkdir "+outputFolder+"/"+sample+"_N",shell=True);
		subprocess.call("ln -s "+pathDict[sample]["N"]["R1"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_1.fastq.gz",shell=True);
		subprocess.call("ln -s "+pathDict[sample]["N"]["R2"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_2.fastq.gz",shell=True);
		print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_N "+sample+"_N_1.fastq.gz "+sample+"_N_2.fastq.gz 4",file=outputb);
		print("tmux new -d -s "+ sample +" '"+ "bash /diskmnt/Projects/cptac_scratch/CPTAC3_analysis/Fusion_hg38/EJ_testing/fusion_pipeline_v2.sh "+sample+"_N "+sample+"_N_1.fastq.gz "+sample+"_N_2.fastq.gz 4" +"'",file=output);
		continue;
	elif pathDict[sample]["N"]["R1"] == "" or pathDict[sample]["N"]["R2"] == "":
		print(sample+"\t"+"noNormalData",file=output1);
		subprocess.call("mkdir "+outputFolder+"/"+sample+"_T",shell=True);
		subprocess.call("ln -s "+pathDict[sample]["T"]["R1"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_1.fastq.gz",shell=True);
		subprocess.call("ln -s "+pathDict[sample]["T"]["R2"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_2.fastq.gz",shell=True);
		print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_T "+sample+"_T_1.fastq.gz "+sample+"_T_2.fastq.gz 4",file=outputa);
		print("tmux new -d -s "+ sample +" '"+ "bash /diskmnt/Projects/cptac_scratch/CPTAC3_analysis/Fusion_hg38/EJ_testing/fusion_pipeline_v2.sh "+sample+"_T "+sample+"_T_1.fastq.gz "+sample+"_T_2.fastq.gz 4" +"'",file=output); 
		continue;
	subprocess.call("mkdir "+outputFolder+"/"+sample+"_T",shell=True);
	subprocess.call("mkdir "+outputFolder+"/"+sample+"_N",shell=True);
	subprocess.call("ln -s "+pathDict[sample]["T"]["R1"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_1.fastq.gz",shell=True);
	subprocess.call("ln -s "+pathDict[sample]["T"]["R2"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_2.fastq.gz",shell=True);
	subprocess.call("ln -s "+pathDict[sample]["N"]["R1"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_1.fastq.gz",shell=True);
	subprocess.call("ln -s "+pathDict[sample]["N"]["R2"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_2.fastq.gz",shell=True);
	print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_T "+sample+"_T_1.fastq.gz "+sample+"_T_2.fastq.gz 4",file=outputa);
	print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_N "+sample+"_N_1.fastq.gz "+sample+"_N_2.fastq.gz 4",file=outputb);
	print("tmux new -d -s "+ sample +" '"+ "bash /diskmnt/Projects/cptac_scratch/CPTAC3_analysis/Fusion_hg38/EJ_testing/fusion_pipeline_v2.sh "+sample+"_N "+sample+"_N_1.fastq.gz "+sample+"_N_2.fastq.gz 4" +"'",file=output);
	print("tmux new -d -s "+ sample +" '"+ "bash /diskmnt/Projects/cptac_scratch/CPTAC3_analysis/Fusion_hg38/EJ_testing/fusion_pipeline_v2.sh "+sample+"_T "+sample+"_T_1.fastq.gz "+sample+"_T_2.fastq.gz 4" +"'",file=output); 
#	elif pathDict[sample]["T"]["R1"] != "" or pathDict[sample]["T"]["R2"] != "":
#		print(sample+"\t"+"withTumorData",file=output3);
#		continue;
#	elif pathDict[sample]["N"]["R1"] != "" or pathDict[sample]["N"]["R2"] != "":
#		print(sample+"\t"+"withNormalData",file=output3);
#		continue;
#	subprocess.call("mkdir "+outputFolder+"/"+sample+"_T",shell=True);
#	subprocess.call("ln -s "+pathDict[sample]["T"]["R1"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_1.fastq.gz",shell=True);
#	subprocess.call("ln -s "+pathDict[sample]["T"]["R2"]+" "+outputFolder+"/"+sample+"_T/"+sample+"_T_2.fastq.gz",shell=True);
#	print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_T "+sample+"_T_1.fastq.gz "+sample+"_T_2.fastq.gz 4",file=output);
#	subprocess.call("mkdir "+outputFolder+"/"+sample+"_N",shell=True);
#	subprocess.call("ln -s "+pathDict[sample]["N"]["R1"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_1.fastq.gz",shell=True);
#	subprocess.call("ln -s "+pathDict[sample]["N"]["R2"]+" "+outputFolder+"/"+sample+"_N/"+sample+"_N_2.fastq.gz",shell=True);
#	print("bash /diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/hg38_Scripts/fusion_pipeline_v2.sh "+sample+"_N "+sample+"_N_1.fastq.gz "+sample+"_N_2.fastq.gz 4",file=output);
outputa.close();
outputb.close();
output1.close();
outputa.close();
#output2.close();
#output3.close();