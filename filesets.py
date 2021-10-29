import os
import json

def split(allfiles, tags, filename):
    
    filesets = {}
    for t in tags:
        for k in allfiles.keys():
            if t in k:
                filesets[k] = allfiles[k]

    names = list(filesets.keys())
    print(names)
    files = {}
    files["files"] = []
    
    for n in names:
        
        files["files"] += filesets[n]
        
        with open(filename, 'w') as json_file:
            json.dump(files, json_file)
    print('Created file')


def main():

    allfiles = {}
    allfiles["2016"] = 'infiles/v2x16_lpc_merged.json'
    allfiles["2017"] = 'infiles/v2x17_lpc_merged.json'
    allfiles["2018"] = 'infiles/v2x18_lpc_merged.json'
    
    for year in ["2016","2017","2018"]:

        with open(allfiles[year]) as f:
            filesets = json.load(f)

        split(filesets,["HToBB"],"infiles/"+year+"_higgs.json")
        split(filesets,["QCD"],"infiles/"+year+"_qcd.json")
        split(filesets,["Wjets","Zjets","DY","WW","ZZ","WZ"],"infiles/"+year+"_wz.json")
        split(filesets,["TT","ST","top"],"infiles/"+year+"_top.json")

        split(filesets,["JetHT","SingleMuon"],"infiles/"+year+"_data.json")

    for year in ["2017"]:
        with open('infiles/JHUgen2017.json') as f:
            filesets = json.load(f)

        split(filesets,["H"],"infiles/"+year+"_bsm.json")


if __name__ == "__main__":
    main()
