Yizhe Song

y.song@wustl.edu

Last updated: 10/23/21

Adapted from Dan Cui Zhou's hg38 pipeline and Qingsong Gao's hg19 pipeline

VERSION: v2.2
Build: hg38
Cluster: katmai

Three tools are used for fusion calling:
Databases and references were downloaded from their respective websites.
STAR-Fusion is downloaded from https://github.com/STAR-Fusion/STAR-Fusion/wiki
EricScript is downloaded from https://sites.google.com/site/bioericscript
Integrate is downloaded from https://sourceforge.net/p/integrate-fusion/wiki/Home/

Fusion pipeline:
Fusions are called by each tool then merged into a single file. This is done for tumor and normal RNA-Seq files individually.
Since raw fusion calls may contain many false positives, extensive filtering is done, as detailed below.
Finally, normal fusions are then filtered out from the tumor fusions.

Filtering strategy:
Get fusions reported by at least 2 callers or reported by STAR-Fusion (shows higher sensitivity) but with higher supporting evidence (defined by fusion fragments per million total reads, or FFPM, >0.1).
Then, remove fusions present in the filtering database, which includes:
1) Uncharacterized genes, immunoglobin genes, mitochondrial genes, etc.
2) Fusions from the same gene or paralog genes (downloaded from https://www.genenames.org/cgi-bin/statistics)
3) Fusions reported in TCGA normal samples from pancan fusion analysis (PMID:29617662), GTEx tissues (reported in star-fusion output), and non-cancer cell studies (PMID: 26837576)

Output format:
In the output file, each row represents one fusion.
There are 9 columns for each fusion:
1) FusionName
2) LeftBreakpoint
3) RightBreakpoint
4) Cancer__Sample
5) JunctionReadCount
6) SpanningFragCount
7) FFPM 		- fusion fragments per million total reads, 'NA' means the fusion was found by both EricScript and Integrate but not STAR-Fusion
8) PROT_FUSION_TYPE 	- INFRAME, FRAMESHIFT or '.'
9) CallerN 		- number of callers

Processing details:
Run "makeDir.py" to create the appropriate folder directory for each sample.
Run "to_run.sh" in order to submit tmux instances.
Once it's all done, run "normalFilter.py" to remove normal fusions.

v2.2 revision history:
Fixed bug that basically ignored Integrate calls
Automatically compresses large Star fusion file
Added a copy any fusion script so we can provide normal calls too (no longer filtering germline by default)
