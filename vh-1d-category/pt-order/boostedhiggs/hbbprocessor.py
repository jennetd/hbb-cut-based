import logging
import json
import numpy as np
from coffea import processor, hist
from .common import (
    getBosons,
    matchedBosonFlavor,
)
from .corrections import (
    corrected_msoftdrop,
    n2ddt_shift,
    add_pileup_weight,
    add_VJets_NLOkFactor,
    add_jetTriggerWeight,
)
from .btag import BTagEfficiency, BTagCorrector

# for old pancakes
from coffea.nanoaod.methods import collection_methods, FatJet
collection_methods['CustomAK8Puppi'] = FatJet
collection_methods['CustomAK8PuppiSubjet'] = FatJet
FatJet.subjetmap['CustomAK8Puppi'] = 'CustomAK8PuppiSubjet'


logger = logging.getLogger(__name__)


class HbbProcessor(processor.ProcessorABC):
    def __init__(self, year='2017', jet_arbitration='pt'):
        self._year = year
        self._jet_arbitration = jet_arbitration

        self._btagSF = BTagCorrector(year, 'medium')

        self._msdSF = {
            '2016': 1.,
            '2017': 0.987,
            '2018': 0.970,
        }

        with open('muon_triggers.json') as f:
            self._muontriggers = json.load(f)

        with open('triggers.json') as f:
            self._triggers = json.load(f)

        self._accumulator = processor.dict_accumulator({
            # dataset -> sumw
            'sumw': processor.defaultdict_accumulator(float),
            'cutflow': hist.Hist(
                'Events',
                hist.Cat('dataset', 'Dataset'),
                hist.Cat('region', 'Region'),
                hist.Bin('genflavor', 'Gen. jet flavor', [0, 1, 2, 3, 4]),
                hist.Bin('cut', 'Cut index', 11, 0, 11),
            ),
            'btagWeight': hist.Hist('Events', hist.Cat('dataset', 'Dataset'), hist.Bin('val', 'BTag correction', 50, 0, 3)),
            'templates-pt': hist.Hist(
                'Events',
                hist.Cat('dataset', 'Dataset'),
                hist.Cat('region', 'Region'),
                hist.Bin('msd1', r'Jet 1 $m_{sd}$', 22, 47, 201),
                hist.Bin('ddb1', r'Jet 1 ddb score', [0, 0.89, 1]),
                hist.Bin('pt2', r'Jet 2 $p_{T}$ [GeV]', [300, 350, 400, 450, 500, 550, 600, 675, 800, 1200]),
                hist.Bin('msd2', r'Jet 2 $m_{sd}$', 22, 47, 201),
                hist.Bin('n2ddt2',r'Jet 2 N2DDT', [-0.25, 0, 0.25]),
            ),
        })

    @property
    def accumulator(self):
        return self._accumulator

    def process(self, events):
        dataset = events.metadata['dataset']
        isRealData = 'genWeight' not in events.columns
        selection = processor.PackedSelection()
        weights = processor.Weights(len(events))
        output = self.accumulator.identity()
        if not isRealData:
            output['sumw'][dataset] += events.genWeight.sum()

        if isRealData:
            trigger = np.zeros(events.size, dtype='bool')
            for t in self._triggers[self._year]:
                try:
                    trigger = trigger | events.HLT[t]
                except:
                    print("No trigger " + t +" in file")
        else:
            trigger = np.ones(events.size, dtype='bool')
        selection.add('trigger', trigger)

        if isRealData:
            trigger = np.zeros(events.size, dtype='bool')
            for t in self._muontriggers[self._year]:
                try:
                    trigger = trigger | events.HLT[t]
                except:
                    print("No trigger " + t +" in file")
        else:
            trigger = np.ones(events.size, dtype='bool')
        selection.add('muontrigger', trigger)

        try:
            fatjets = events.FatJet
        except AttributeError:
            # early pancakes
            fatjets = events.CustomAK8Puppi
        fatjets['msdcorr'] = corrected_msoftdrop(fatjets)
        fatjets['rho'] = 2 * np.log(fatjets.msdcorr / fatjets.pt)
        fatjets['n2ddt'] = fatjets.n2b1 - n2ddt_shift(fatjets, year=self._year)
        fatjets['msdcorr_full'] = fatjets['msdcorr'] * self._msdSF[self._year]

        candidatejet = fatjets[
            # https://github.com/DAZSLE/BaconAnalyzer/blob/master/Analyzer/src/VJetLoader.cc#L269
            (fatjets.pt > 200)
            & (abs(fatjets.eta) < 2.5)
            & fatjets.isTight  # this is loose in sampleContainer
        ]

        nfatjets = candidatejet[:].counts

        if self._jet_arbitration == 'pt':
            secondjet = candidatejet[:, 1:2]
            candidatejet = candidatejet[:, 0:1]
        elif self._jet_arbitration == 'revpt':
            secondjet = candidatejet[:, 0:1]
            candidatejet = candidatejet[:, 1:2]
        elif self._jet_arbitration == 'mass':
            idx = (candidatejet.msdcorr).argsort()
            idx0 = idx[:,0:1]
            idx1 = idx[:,1:2]
            secondjet = candidatejet[idx1]
            candidatejet = candidatejet[idx0]
        elif self._jet_arbitration == 'n2':
            candidatejet = candidatejet[
                candidatejet.n2ddt.argmin()
            ]
        elif self._jet_arbitration == 'ddb':
            candidatejet = candidatejet[
                candidatejet.btagDDBvL.argmax()
            ]
        else:
            raise RuntimeError("Unknown candidate jet arbitration")

        selection.add('minjetkin', (
            (candidatejet.pt >= 450)
            & (candidatejet.msdcorr >= 40.)
            & (abs(candidatejet.eta) < 2.5)
        ).any())
        selection.add('jetacceptance', (
            (candidatejet.msdcorr >= 47.)
            & (candidatejet.pt < 1200)
            & (candidatejet.msdcorr < 201.)
        ).any())
        selection.add('n2ddt', (candidatejet.n2ddt < 0.).any())
        selection.add('ddbpass', (candidatejet.btagDDBvL >= 0.89).any())

        selection.add('minjetkin2', (
            (secondjet.pt >= 450)
            & (secondjet.msdcorr >= 40.)
            & (abs(secondjet.eta) < 2.5)
        ).any())
        selection.add('jetacceptance2', (
            (secondjet.msdcorr >= 47.)
            & (secondjet.pt < 1200)
            & (secondjet.msdcorr < 201.)
        ).any())
        selection.add('n2ddt2', (secondjet.n2ddt < 0.).any())

        jets = events.Jet[
            (events.Jet.pt > 30.)
            & (abs(events.Jet.eta) < 5.0)
            & events.Jet.isTight
        ]
        # only consider first 4 jets to be consistent with old framework
        njets = jets[:].counts
        jets = jets[:, :4]
        ak4_ak8_pair = jets.cross(candidatejet, nested=True)
        dphi = abs(ak4_ak8_pair.i0.delta_phi(ak4_ak8_pair.i1))
        deta = abs(ak4_ak8_pair.i0.eta - ak4_ak8_pair.i1.eta)
        ak4_opposite = jets[(dphi > np.pi / 2).all()]
#        selection.add('antiak4btagMediumOppHem', ak4_opposite.btagDeepB.max() < BTagEfficiency.btagWPs[self._year]['medium'])
        ak4_away = jets[(dphi > 0.8).all()]
#        selection.add('ak4btagMedium08', ak4_away.btagDeepB.max() > BTagEfficiency.btagWPs[self._year]['medium'])

        selection.add('met', events.MET.pt < 140.)

        dR = np.sqrt(dphi*dphi + deta*deta)
        ak4_outside_ak8 = jets[(dR > 0.8).all()]

        jet1 = ak4_outside_ak8[:, 0:1]
        jet2 = ak4_outside_ak8[:, 1:2]

        ak4_pair = jet1.cross(jet2, nested=False)

        # redefine deta to be between ak4 jets
        deta = abs(ak4_pair.i0.eta - ak4_pair.i1.eta)
        mjj = (ak4_pair.i0+ak4_pair.i1).mass
        qgl1 = jet1.qgl
        qgl2 = jet2.qgl

        selection.add('deta', (deta > 3.5).any())
        selection.add('mjj', (mjj > 1000.).any())

        goodmuon = (
            (events.Muon.pt > 10)
            & (abs(events.Muon.eta) < 2.4)
            & (events.Muon.pfRelIso04_all < 0.25)
            & (events.Muon.looseId).astype(bool)
        )
        nmuons = goodmuon.sum()
        leadingmuon = events.Muon[goodmuon][:, 0:1]
        muon_ak8_pair = leadingmuon.cross(candidatejet, nested=True)

        nelectrons = (
            (events.Electron.pt > 10)
            & (abs(events.Electron.eta) < 2.5)
            & (events.Electron.cutBased >= events.Electron.LOOSE)
        ).sum()

        ntaus = (
            (events.Tau.pt > 20)
            & (events.Tau.idDecayMode).astype(bool)
            # bacon iso looser than Nano selection
        ).sum()

        selection.add('noleptons', (nmuons == 0) & (nelectrons == 0) & (ntaus == 0))
        selection.add('onemuon', (nmuons == 1) & (nelectrons == 0) & (ntaus == 0))
        selection.add('muonkin', (
            (leadingmuon.pt > 55.)
            & (abs(leadingmuon.eta) < 2.1)
        ).all())
        selection.add('muonDphiAK8', (
            abs(muon_ak8_pair.i0.delta_phi(muon_ak8_pair.i1)) > 2*np.pi/3
        ).all().all())

        if isRealData:
            genflavor = candidatejet.pt.zeros_like()
            genflavor2 = secondjet.pt.zeros_like()
        else:
            weights.add('genweight', events.genWeight)
            add_pileup_weight(weights, events.Pileup.nPU, self._year, dataset)
            bosons = getBosons(events)
            genBosonPt = bosons.pt.pad(1, clip=True).fillna(0).flatten()
            add_VJets_NLOkFactor(weights, genBosonPt, self._year, dataset)
            genflavor = matchedBosonFlavor(candidatejet, bosons).pad(1, clip=True).fillna(-1).flatten()
            genflavor2 = matchedBosonFlavor(secondjet, bosons).pad(1, clip=True).fillna(-1).flatten()
            add_jetTriggerWeight(weights, candidatejet.msdcorr, candidatejet.pt, self._year)
            output['btagWeight'].fill(dataset=dataset, val=self._btagSF.addBtagWeight(weights, ak4_away))
            logger.debug("Weight statistics: %r" % weights._weightStats)

        msd_matched = candidatejet.msdcorr * self._msdSF[self._year] * (genflavor > 0) + candidatejet.msdcorr * (genflavor == 0)
        msd2_matched = secondjet.msdcorr * self._msdSF[self._year] * (genflavor2 > 0) + secondjet.msdcorr * (genflavor2 == 0)

        regions = {
            'signal': ['trigger', 'minjetkin', 'jetacceptance', 'n2ddt', 'minjetkin2', 'jetacceptance2', 'met', 'noleptons'],
            'muoncontrol': ['muontrigger', 'minjetkin', 'jetacceptance', 'n2ddt', 'onemuon', 'muonkin', 'muonDphiAK8'],
            'noselection': [],
        }

        for region, cuts in regions.items():
            allcuts = set()
            if isRealData:
                continue

            logger.debug(f"Filling cutflow with: {dataset}, {region}, {genflavor}, {weights.weight()}")
            output['cutflow'].fill(dataset=dataset, region=region, genflavor=genflavor, cut=0, weight=weights.weight())
            for i, cut in enumerate(cuts + ['ddbpass']):
                allcuts.add(cut)
                cut = selection.all(*allcuts)
                output['cutflow'].fill(dataset=dataset, region=region, genflavor=genflavor[cut], cut=i + 1, weight=weights.weight()[cut])

        systematics = [
            None,
#            'jet_triggerUp',
#            'jet_triggerDown',
#            'btagWeightUp',
#            'btagWeightDown',
#            'btagEffStatUp',
#            'btagEffStatDown',
        ]

        def normalize(val, cut):
            return val[cut].pad(1, clip=True).fillna(0).flatten()

        def fill(region, systematic, wmod=None):
            selections = regions[region]
            cut = selection.all(*selections)
            sname = 'nominal' if systematic is None else systematic
            if wmod is None:
                weight = weights.weight(modifier=systematic)[cut]
            else:
                weight = weights.weight()[cut] * wmod[cut]

            output['templates-revpt'].fill(
                dataset=dataset,
                region=region,
#                pt1=normalize(candidatejet.pt, cut),
                msd1=normalize(msd_matched, cut),
                ddb1=normalize(candidatejet.btagDDBvL, cut),
                pt2=normalize(secondjet.pt, cut),
                msd2=normalize(msd2_matched, cut),
#                ddb2=normalize(secondjet.btagDDBvL, cut),
                n2ddt2=normalize(secondjet.n2ddt, cut),
                weight=weight,
            )

        for region in regions:
            cut = selection.all(*(set(regions[region]) - {'n2ddt'}))
            for systematic in [None]: #systematics:
                fill(region, systematic)
#            if 'GluGluHToBB' in dataset:
#                for i in range(9):
#                    fill(region, 'LHEScale_%d' % i, events.LHEScaleWeight[:, i])
#                for c in events.LHEWeight.columns[1:]:
#                    fill(region, 'LHEWeight_%s' % c, events.LHEWeight[c])

        return output

    def postprocess(self, accumulator):
        return accumulator
