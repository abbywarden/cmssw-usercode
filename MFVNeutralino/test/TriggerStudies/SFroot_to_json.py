import numpy as np
import correctionlib.schemav2 as cs
import correctionlib.convert
import json
import ROOT

#TO USE : THIS SHOULD BE RAN OUTSIDE OF CMSSW (ie do not cmsenv)
#also make certain that you have correctionlib installed (python3 -m pip install correctionlib)
#run : python3 SFroot_to_json.py 

# ROOT filenames (they are expected to be in the same directory as the script)
lep = "muon" #either muon or electron

year_files = {
    "20161": "sf_%s_20161.root"%lep,
    "20162": "sf_%s_20162.root"%lep,
    "2017" : "sf_%s_2017.root"%lep,
    "2018" : "sf_%s_2018.root"%lep,
}

# Hist names expected in each file 
# the nominal scale factor, the scale factor + systunc, and scale factor - systunc
hist_names = {
    "nominal": "sf_nominal",
    "systup":  "sf_systup",
    "systdown": "sf_systdown",
}

year_items = []

# Loop over years and build a per-year category
for year, filename in year_files.items():
    print(f"Processing {year} from {filename}")
    
    with ROOT.TFile.Open(filename) as f:
        # Load histograms
        hists = {key: f[val] for key, val in hist_names.items()}

        # Convert to correctionlib format
        corr_nom = correctionlib.convert.from_histogram(hists["nominal"])
        corr_up  = correctionlib.convert.from_histogram(hists["systup"])
        corr_dn  = correctionlib.convert.from_histogram(hists["systdown"])

        # Rename input names for clarity
        corr_nom.inputs[0].name = "pt"
        corr_nom.inputs[1].name = "eta"
        corr_nom.output.name = "weight"
        
        #Rename data input names for clarity ([eta, pt] instead of [axis0, axis1])
        if isinstance(corr_nom.data, cs.MultiBinning):
            corr_nom.data.inputs[0] = "eta"
            corr_nom.data.inputs[1] = "pt"
        if isinstance(corr_nom.data, cs.MultiBinning):
            corr_up.data.inputs[0] = "eta"
            corr_up.data.inputs[1] = "pt"
        if isinstance(corr_dn.data, cs.MultiBinning):
            corr_dn.data.inputs[0] = "eta"
            corr_dn.data.inputs[1] = "pt"
            
            
        # set overflow bin behavior (clamp means overflow ok)
        corr_nom.data.flow = "clamp"
        corr_up.data.flow = "clamp"
        corr_dn.data.flow = "clamp"

        # Build per-year variation category
        year_item = cs.CategoryItem(
            key=year,
            value=cs.Category(
                nodetype="category",
                input="ValType",
                content=[
                    cs.CategoryItem(key="nominal",  value=corr_nom.data),
                    cs.CategoryItem(key="systup",   value=corr_up.data),
                    cs.CategoryItem(key="systdown", value=corr_dn.data),
                ],
            ),
        )

        year_items.append(year_item)

# Combine everything into one Correction object
corr_full = cs.Correction(
    name="scale_factor",
    version=1,
    description="%s trigger scale factors with systematics for the full RUN-II Ultra Legacy dataset. They are dependent on the transverse momentum and pseudorapidity of the %s."%(lep,lep),
    inputs=[
        cs.Variable(name="pt", type="real", description="%s pT [GeV]"%lep),
        cs.Variable(name="eta", type="real", description="%s eta"%lep),
        cs.Variable(name="year", type="string", description="era"),
        cs.Variable(name="ValType", type="string", description="(nominal/systup/systdown)"),
    ],
    output=cs.Variable(name="weight", type="real", description="scale factor"),
    data=cs.Category(
        nodetype="category",
        input="year",
        content=year_items,
    ),
)

# Wrap in CorrectionSet
corrset = cs.CorrectionSet(schema_version=2, corrections=[corr_full])

# Save to JSON
with open("%s_trigsf_runII.json"%lep, "w") as fout:
    fout.write(corrset.json(exclude_unset=True))
print("CorrectionSet saved to %s_trigsf_runII.json"%lep)