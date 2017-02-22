#!/usr/bin/env python
import re,os,sys,warnings,argparse

parser = argparse.ArgumentParser(description="""Read an input file and a gff3 file.
                                              Append the gene information to the
                                              input file.""")
parser.add_argument("-i", "--input", metavar="input.file", dest="finput",
                    action="store", type=str, required=True, 
                    help="input sample_list.txt (required)")
parser.add_argument("-g", "--gtf", metavar="genes.gtf", dest="fgtf",
                    action="store", type=str, required=True, 
                    help="input genes.gtf (required)")
parser.add_argument("-o", "--output", metavar="output.file", dest="foutput",
                    action="store", default="read_gff3.out", type=str, 
                    help="output file name (default: %(default)s)")
args = parser.parse_args()

def main(argv):
    #oID = re.compile(r"ID=(\w+)")
    oParent = re.compile(r"Parent=(\w+)")
    oProduct = re.compile(r"product=([-:()%\.\s\w]+)")
    #sID = oID.search("") 
    sParent = oParent.search("")
    sProduct = oProduct.search("")
    ID2Info= {}

    IN = open(args.fgtf, "r")
    for line in IN:
        sParent = oParent.search(line) 
        if sParent:
            sProduct = oProduct.search(line[0:-1])
            if sProduct:
                ID2Info[sParent.group(1)] = sProduct.group(1)
            else:
                ID2Info[sParent.group(1)] = ""
        else:
            continue
    IN.close()

    IN = open(args.finput, "r")
    OUT = open(args.foutput, "w")
    header = IN.readline()
    #OUT.write("gene id" + header[0:-1] + "\tgene name\tbiotype\tdescription\n")
    OUT.write(header[0:-1] + "\tproduct\n")
    for line in IN:
        columns = line.split("\t")
        if columns[0] in ID2Info:
            OUT.write(line[0:-1] + "\t" + ID2Info[columns[0]] + "\n")
        else:
            OUT.write(line)
            print(line[0:-1])
    IN.close()
    OUT.close()

if __name__ == "__main__":
    main(sys.argv[1:])
