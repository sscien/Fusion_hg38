import subprocess
import os
import sys

# call example:
# foo.py samples.txt BRCA Yes submission_dir

cancer = sys.argv[2]

if sys.argv[4]:
    currPath = os.path.abspath(sys.argv[4])+"/";
else:
    currPath = os.path.abspath(".")+"/";

if sys.argv[3] == "Yes":
    miss_samples = [];
    with open("Missing/samples.txt") as sampleFile:
        for line in sampleFile:
            miss_samples.append(line.strip().split("\t")[0])
else:
    miss_samples = [];

#miss_samples = [];
# with open("Missing/samples.txt") as sampleFile:
#     for line in sampleFile:
#         miss_samples.append(line.strip().split("\t")[0])

samples = [];
with open(sys.argv[1]) as sampleFile:
    for line in sampleFile:
        samples.append(line.strip())

uuidDict = {}
sampleFile = open("/diskmnt/Projects/Users/dcui/Projects/Fusion_hg38/Data_locations/CPTAC3.catalog/BamMap/katmai.BamMap.dat");
for line in sampleFile:
    line = line.strip().split("\t");
    if "FASTQ" not in line:
        continue
    if line[1] not in samples+miss_samples:
        continue;
    if line[0].split(".")[1] != "RNA-Seq":
        continue;
    if line[1] not in uuidDict:
        uuidDict[line[1]] = {"tumor":{"R1":"","R2":""},"normal":{"R1":"","R2":""}}
    if line[0][-1] == "T":
        if "R1" in line[0]:
            uuidDict[line[1]]["tumor"]["R1"] = line[9];
        else:
            uuidDict[line[1]]["tumor"]["R2"] = line[9];
    else:
        if "R1" in line[0]:
            uuidDict[line[1]]["normal"]["R1"] = line[9];
        else:
            uuidDict[line[1]]["normal"]["R2"] = line[9];
sampleFile.close();

print("#Case_Name\tDisease\tOutput_File_Path\tOutput_File_Format\tSample_Name_R1\tFASTQ_R1_UUID\tSample_Name_R2\tFASTQ_R2_UUID");
for sample in samples:
    if sample in miss_samples:
        continue
    print("\t".join([sample,
                    cancer,
                     currPath+"Submission/"+sample+"_T.Fusions.txt",
                     "TSV",
                     sample+".RNA-Seq.R1.T",
                   uuidDict[sample]["tumor"]["R1"],
                   sample+".RNA-Seq.R2.T",
                     uuidDict[sample]["tumor"]["R2"]
                    ]))
    print("\t".join([sample,
                    cancer,
                     currPath+"Submission/"+sample+"_N.Fusions.txt",
                     "TSV",
                     sample+".RNA-Seq.R1.A",
                     uuidDict[sample]["normal"]["R1"],
                     sample+".RNA-Seq.R2.A",
                     uuidDict[sample]["normal"]["R2"]
                    ]))
for sample in miss_samples:
    print("\t".join([sample,
                    cancer,
                     currPath+"Submission/"+sample+"_T.Fusions.txt",
                     "TSV",
                     sample+".RNA-Seq.R1.T",
                   uuidDict[sample]["tumor"]["R1"],
                   sample+".RNA-Seq.R2.T",
                     uuidDict[sample]["tumor"]["R2"]
                    ]))
