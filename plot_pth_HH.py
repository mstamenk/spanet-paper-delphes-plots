# Script to plot HH4b 

import os, ROOT
ROOT.gROOT.SetBatch(True)


from utils import wps_years, luminosities, drawText

from array import array

#import CMS_lumi, tdrstyle

#tdrstyle.setTDRStyle()


path = '/afs/cern.ch/work/m/mstamenk/public/spanet-delphes-paper/'
f_in = 'HH4b'

df = ROOT.RDataFrame('Events', path +'/' + f_in + '.root')

computeRapidity = '''
    double computeRapidity(float pT, float eta, float phi, float m){
        TLorentzVector v;
        v.SetPtEtaPhiM(pT,eta,phi,m);

        return v.Rapidity();
    } 

'''

ROOT.gInterpreter.Declare(computeRapidity)


df = df.Define('genHiggs1Rapidity','computeRapidity(genHiggs1Pt,genHiggs1Eta,genHiggs1Phi,125)')
df = df.Define('genHiggs2Rapidity','computeRapidity(genHiggs2Pt,genHiggs2Eta,genHiggs2Phi,125)')
df = df.Define('genHiggs3Rapidity','computeRapidity(genHiggs3Pt,genHiggs3Eta,genHiggs3Phi,125)')


#df = df.Filter('TMath::Abs(genHiggs1Rapidity) < 2 && TMath::Abs(genHiggs1Rapidity) < 2 && TMath::Abs(genHiggs1Rapidity) < 2')


varx = 'genHiggs1Pt'
ls = [0,100,200,300,400,500,600,700]
ls = [20 * i for i in range(30)]

bins = array('d', ls)
binsx = len(ls) - 1

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
h1.GetXaxis().SetTitle('Higgs p_{T} [GeV]')
#h1.GetYaxis().SetTitle('Normalized')
h1.GetYaxis().SetTitle('#frac{d#sigma}{dp_{T}} [fb]')


#h1.Scale(1./h1.Integral())
#h2.Scale(1./h2.Integral())
#h3.Scale(1./h3.Integral())

h1.Scale(36.69/h1.Integral())
h2.Scale(36.69/h2.Integral())
h3.Scale(36.69/h3.Integral())

h1.SetMaximum(h1.GetMaximum()*1.5)

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

legend = ROOT.TLegend(0.75,0.7,0.89,0.89)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.AddEntry(h1,'H_{1}')
legend.AddEntry(h2,'H_{2}')
#legend.AddEntry(h3,'Third p_{T} Higgs')



c = ROOT.TCanvas()
c.SetLeftMargin(0.15)
h1.Draw("hist e")
h2.Draw("hist e same")
#h3.Draw("hist e same")

drawText(0.20,0.85, "pp #rightarrow HH",fontsize=0.05)
drawText(0.20,0.78, "#lambda_{3} = #lambda_{4}= #lambda_{SM}",fontsize=0.05)
#drawText(0.15,0.71, "Rapidity |y(H)| < 2",fontsize=0.05)
legend.Draw()

c.Print('HH_pt_spectrum.png')
c.Print('HH_pt_spectrum.pdf')


