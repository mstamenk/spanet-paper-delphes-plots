# Script to plot HH4b and HHH6b pT spectra
import os, ROOT
ROOT.gROOT.SetBatch(True)

from array import array
import sys
from utils import drawText

f_in = sys.argv[1] if len(sys.argv) > 1 else '/afs/cern.ch/work/m/mstamenk/public/spanet-delphes-paper/HH4b.root'

if not os.path.exists(f_in):
    print(f"File {f_in} does not exist.")
    sys.exit(1)

hhh = 'HHH6b.root' in f_in
hh = 'HH4b.root' in f_in

if not (hhh or hh):
    print("Input file must be HHH6b.root or HH4b.root")
    sys.exit(1)

df = ROOT.RDataFrame('Events', f_in)

ls = [0,100,200,300,400,500,600,700,800,900,1000]
ls = [20 * i for i in range(30)]

bins = array('d', ls)
binsx = len(ls) - 1

varx = 'genHiggs1Pt'
h1 = df.Histo1D((varx,varx,binsx,bins),varx)

varx = 'genHiggs2Pt'
h2 = df.Histo1D((varx,varx,binsx,bins),varx)

varx = 'genHiggs3Pt'
h3 = df.Histo1D((varx,varx,binsx,bins),varx)

h1 = h1.GetValue()
h2 = h2.GetValue()
h3 = h3.GetValue()


h1.SetStats(0)
h1.SetTitle('')
h1.GetXaxis().SetTitle('H p_{T} [GeV]')
h1.GetYaxis().SetTitle('d#sigma/dp_{T} [fb]')
h1.GetXaxis().SetTitleSize(0.05)
h1.GetYaxis().SetTitleSize(0.05)
h1.GetXaxis().SetLabelSize(0.04)
h1.GetYaxis().SetLabelSize(0.04)

xsec = 0.101 if hhh else 36.69

h1.Scale(xsec/h1.Integral())
h2.Scale(xsec/h2.Integral())
h3.Scale(xsec/h3.Integral())

if hhh:
    h1.SetMaximum(max([h1.GetMaximum(), h2.GetMaximum(), h3.GetMaximum()])*1.5)
else:
    h1.SetMaximum(max([h1.GetMaximum(), h2.GetMaximum()])*1.5)

h1.SetLineColor(ROOT.kGreen + 2)
h2.SetLineColor(ROOT.kAzure + 7)
h3.SetLineColor(ROOT.kRed + 1)

h1.SetMarkerColor(ROOT.kGreen + 2)
h2.SetMarkerColor(ROOT.kAzure + 7)
h3.SetMarkerColor(ROOT.kRed + 1)

h1.SetMarkerStyle(22)
h2.SetMarkerStyle(21)
h3.SetMarkerStyle(20)

h1.SetMarkerSize(0.8)
h2.SetMarkerSize(0.8)
h3.SetMarkerSize(0.8)

h1.SetLineWidth(2)
h2.SetLineWidth(2)
h3.SetLineWidth(2)

h2.SetLineStyle(2)
h3.SetLineStyle(3)

if hhh:
    legend = ROOT.TLegend(0.75,0.7,0.9,0.88)
else:
    legend = ROOT.TLegend(0.75,0.76,0.9,0.88)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.AddEntry(h1,'H_{1}')
legend.AddEntry(h2,'H_{2}')
if hhh:
    legend.AddEntry(h3,'H_{3}')


c = ROOT.TCanvas()
c.SetLeftMargin(0.15)
c.SetBottomMargin(0.12)
h1.Draw("hist e")
h2.Draw("hist e same")
if hhh:
    h3.Draw("hist e same")

if hhh:
    drawText(0.2,0.85, "pp #rightarrow HHH",fontsize=0.05)
else:
    drawText(0.2,0.85, "pp #rightarrow HH",fontsize=0.05)
drawText(0.2,0.78, "#lambda_{3} = #lambda_{4} = #lambda_{SM}",fontsize=0.05)
legend.Draw()

if hhh:
    c.Print('HHH_pt_spectrum.png')
    c.Print('HHH_pt_spectrum.pdf')
else:
    c.Print('HH_pt_spectrum.png')
    c.Print('HH_pt_spectrum.pdf')
