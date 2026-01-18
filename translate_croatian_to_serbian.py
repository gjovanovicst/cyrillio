#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Croatian to Serbian Word Translator for Subtitles
Converts Croatian vocabulary to Serbian equivalents in .srt files
"""

import os
import re
from pathlib import Path

# Croatian to Serbian word mappings
# Format: 'Croatian word': 'Serbian word'
CROATIAN_TO_SERBIAN = {
    # =====================================================
    # LOCATION/PLACE ADVERBS (ovdje, gdje, etc.)
    # =====================================================
    'ovdje': 'ovde',
    'Ovdje': 'Ovde',
    'gdje': 'gde',
    'Gdje': 'Gde',
    'negdje': 'negde',
    'Negdje': 'Negde',
    'nigdje': 'nigde',
    'Nigdje': 'Nigde',
    'svugdje': 'svugde',
    'Svugdje': 'Svugde',
    'igdje': 'igde',
    'Igdje': 'Igde',
    'ondje': 'onde',
    'Ondje': 'Onde',
    'odakle': 'odakle',
    'dokle': 'dokle',
    
    # =====================================================
    # TIME ADVERBS (uvijek, prije, poslije)
    # =====================================================
    'uvijek': 'uvek',
    'Uvijek': 'Uvek',
    'zauvijek': 'zauvek',
    'Zauvijek': 'Zauvek',
    'prije': 'pre',
    'Prije': 'Pre',
    'poslije': 'posle',
    'Poslije': 'Posle',
    'najprije': 'najpre',
    'Najprije': 'Najpre',
    
    # =====================================================
    # SEE/WATCH (vidjeti -> videti)
    # =====================================================
    'vidjeti': 'videti',
    'vidio': 'video',
    'vidjela': 'videla',
    'vidjeli': 'videli',
    'vidjelo': 'videlo',
    'Vidjeti': 'Videti',
    'Vidio': 'Video',
    'Vidjela': 'Videla',
    'Vidjeli': 'Videli',
    
    # =====================================================
    # FEEL (osjećati -> osećati)
    # =====================================================
    'osjećati': 'osećati',
    'osjećam': 'osećam',
    'osjećaš': 'osećaš',
    'osjeća': 'oseća',
    'osjećamo': 'osećamo',
    'osjećate': 'osećate',
    'osjećaju': 'osećaju',
    'Osjećam': 'Osećam',
    'Osjećaš': 'Osećaš',
    'Osjeća': 'Oseća',
    'osjećaj': 'osećaj',
    'osjećaja': 'osećaja',
    'osjećaje': 'osećaje',
    'osjećajima': 'osećajima',
    'Osjećaj': 'Osećaj',
    
    # =====================================================
    # REMEMBER (sjećati -> sećati)
    # =====================================================
    'sjećati': 'sećati',
    'sjećam': 'sećam',
    'sjećaš': 'sećaš',
    'sjeća': 'seća',
    'sjećamo': 'sećamo',
    'sjećate': 'sećate',
    'sjećaju': 'sećaju',
    'Sjećam': 'Sećam',
    'Sjećaš': 'Sećaš',
    'Sjećate': 'Sećate',
    'sjećanje': 'sećanje',
    'sjećanja': 'sećanja',
    'Sjećanje': 'Sećanje',
    'sjetiti': 'setiti',
    'sjetio': 'setio',
    'sjetila': 'setila',
    'sjetili': 'setili',
    'sjeti': 'seti',
    
    # =====================================================
    # LIVE (živjeti -> živeti)
    # =====================================================
    'živjeti': 'živeti',
    'živio': 'živeo',
    'živjela': 'živela',
    'živjeli': 'živeli',
    'živjelo': 'živelo',
    'Živjeti': 'Živeti',
    'Živio': 'Živeo',
    'Živjela': 'Živela',
    'Živjeli': 'Živeli',
    
    # =====================================================
    # LOVE (voljeti -> voleti)
    # =====================================================
    'voljeti': 'voleti',
    'volio': 'voleo',
    'voljela': 'volela',
    'voljeli': 'voleli',
    'voljelo': 'volelo',
    'Voljeti': 'Voleti',
    'Volio': 'Voleo',
    'Voljela': 'Volela',
    'Voljeli': 'Voleli',
    
    # =====================================================
    # HAPPY (sretan -> srećan)
    # =====================================================
    'sretan': 'srećan',
    'sretna': 'srećna',
    'sretno': 'srećno',
    'sretni': 'srećni',
    'sretne': 'srećne',
    'sretnog': 'srećnog',
    'sretnoj': 'srećnoj',
    'Sretan': 'Srećan',
    'Sretna': 'Srećna',
    'Sretno': 'Srećno',
    'sreća': 'sreća',
    'sreće': 'sreće',
    'sreći': 'sreći',
    'srećom': 'srećom',
    
    # =====================================================
    # LABORATORY (laboratorij -> laboratorija)
    # =====================================================
    'laboratorij': 'laboratorija',
    'laboratorija': 'laboratorije',
    'laboratoriju': 'laboratoriji',
    'Laboratorij': 'Laboratorija',
    
    # =====================================================
    # VISITOR (posjetitelj -> posetilac)
    # =====================================================
    'posjetitelj': 'posetilac',
    'posjetitelja': 'posetioca',
    'posjetitelju': 'posetiocu',
    'posjetitelji': 'posetioci',
    'posjetitelje': 'posetioce',
    'Posjetitelj': 'Posetilac',
    'posjetiti': 'posetiti',
    'posjetio': 'posetio',
    'posjetila': 'posetila',
    'posjetili': 'posetili',
    'posjet': 'poseta',
    'posjeta': 'posete',
    'posjetu': 'posetu',
    'posjetom': 'posetom',
    
    # =====================================================
    # BEAUTIFUL (lijep -> lep)
    # =====================================================
    'lijep': 'lep',
    'lijepa': 'lepa',
    'lijepo': 'lepo',
    'lijepi': 'lepi',
    'lijepe': 'lepe',
    'lijepog': 'lepog',
    'lijepoj': 'lepoj',
    'lijepom': 'lepom',
    'Lijep': 'Lep',
    'Lijepa': 'Lepa',
    'Lijepo': 'Lepo',
    'ljepota': 'lepota',
    'ljepote': 'lepote',
    'ljepoti': 'lepoti',
    'ljepotom': 'lepotom',
    'Ljepota': 'Lepota',
    'ljepotan': 'lepotan',
    'ljepotana': 'lepotana',
    'ljepotanu': 'lepotanu',
    'Ljepotan': 'Lepotan',
    
    # =====================================================
    # SHADOW (sjena -> senka)
    # =====================================================
    'sjena': 'senka',
    'sjene': 'senke',
    'sjeni': 'senci',
    'sjenom': 'senkom',
    'sjenu': 'senku',
    'Sjena': 'Senka',
    'Sjene': 'Senke',
    
    # =====================================================
    # BLADDER/BUBBLE (mjehur -> mehur)
    # =====================================================
    'mjehur': 'mehur',
    'mjehura': 'mehura',
    'mjehuru': 'mehuru',
    'mjehurom': 'mehurom',
    'mjehuri': 'mehuri',
    'Mjehur': 'Mehur',
    
    # =====================================================
    # FUNNY (smiješan -> smešan)
    # =====================================================
    'smiješan': 'smešan',
    'smiješna': 'smešna',
    'smiješno': 'smešno',
    'smiješni': 'smešni',
    'smiješne': 'smešne',
    'Smiješan': 'Smešan',
    'Smiješna': 'Smešna',
    'Smiješno': 'Smešno',
    
    # =====================================================
    # LAUGH (smijeh -> smeh)
    # =====================================================
    'smijeh': 'smeh',
    'smijeha': 'smeha',
    'smijehu': 'smehu',
    'smijehom': 'smehom',
    'Smijeh': 'Smeh',
    'smijati': 'smejati',
    'smijem': 'smejem',
    'smiješ': 'smeješ',
    
    # =====================================================
    # ERROR (greška - same, but pogreška -> greška)
    # =====================================================
    'pogreška': 'greška',
    'pogreške': 'greške',
    'pogrešku': 'grešku',
    'pogreškom': 'greškom',
    'pogreški': 'greški',
    'Pogreška': 'Greška',
    
    # =====================================================
    # CROATIAN FUTURE TENSE (bit ću -> biću)
    # =====================================================
    'bit ću': 'biću',
    'Bit ću': 'Biću',
    'bit ćeš': 'bićeš',
    'Bit ćeš': 'Bićeš',
    'bit će': 'biće',
    'Bit će': 'Biće',
    'bit ćemo': 'bićemo',
    'Bit ćemo': 'Bićemo',
    'bit ćete': 'bićete',
    'Bit ćete': 'Bićete',
    
    # =====================================================
    # FUTURE TENSE with voljeti (Voljet će -> Voleće)
    # =====================================================
    'voljet ću': 'voleću',
    'Voljet ću': 'Voleću',
    'voljet ćeš': 'volećeš',
    'Voljet ćeš': 'Volećeš',
    'voljet će': 'voleće',
    'Voljet će': 'Voleće',
    'voljet ćemo': 'volećemo',
    'Voljet ćemo': 'Volećemo',
    
    # =====================================================
    # FUTURE TENSE - verbs ending in -at/-it + ću/će/ćemo/ćete
    # =====================================================
    # Show (Pokazat ću -> Pokazaću)
    'pokazat ću': 'pokazaću',
    'Pokazat ću': 'Pokazaću',
    'pokazat ćeš': 'pokazaćeš',
    'pokazat će': 'pokazaće',
    'pokazat ćemo': 'pokazaćemo',
    'pokazat ćete': 'pokazaćete',
    
    # Return (Vratit ću -> Vratiću)
    'vratit ću': 'vratiću',
    'Vratit ću': 'Vratiću',
    'vratit ćeš': 'vratićeš',
    'vratit će': 'vratiće',
    'vratit ćemo': 'vratićemo',
    'vratit ćete': 'vratićete',
    'Vratit ćeš': 'Vratićeš',
    
    # Have to (Morat ću -> Moraću)
    'morat ću': 'moraću',
    'Morat ću': 'Moraću',
    'morat ćeš': 'moraćeš',
    'morat će': 'moraće',
    'morat ćemo': 'moraćemo',
    'morat ćete': 'moraćete',
    
    # Explode (Eksplodirat će -> Eksplodiraće)
    'eksplodirat ću': 'eksplodiraću',
    'eksplodirat ćeš': 'eksplodiraćeš',
    'eksplodirat će': 'eksplodiraće',
    'Eksplodirat će': 'Eksplodiraće',
    'eksplodirat ćemo': 'eksplodiraćemo',
    'eksplodirat ćete': 'eksplodiraćete',
    
    # Overload (Preopteretit ćete -> Preopteretićete)
    'preopteretit ću': 'preopteretiću',
    'preopteretit ćeš': 'preopteretićeš',
    'preopteretit će': 'preopteretiće',
    'preopteretit ćemo': 'preopteretićemo',
    'preopteretit ćete': 'preopteretićete',
    'Preopteretit ćete': 'Preopteretićete',
    
    # Mean (Značit će -> Značiće)
    'značit ću': 'značiću',
    'značit ćeš': 'značićeš',
    'značit će': 'značiće',
    'značit ćemo': 'značićemo',
    'značit ćete': 'značićete',
    
    # Lower (Spustit ću -> Spustiću)
    'spustit ću': 'spustiću',
    'Spustit ću': 'Spustiću',
    'spustit ćeš': 'spustićeš',
    'spustit će': 'spustiće',
    'spustit ćemo': 'spustićemo',
    'spustit ćete': 'spustićete',
    
    # Scream (Vrištat će -> Vristaće)
    'vrištat ću': 'vrištaću',
    'vrištat ćeš': 'vrištaćeš',
    'vrištat će': 'vrištaće',
    'Vrištat će': 'Vrištaće',
    'vrištat ćemo': 'vrištaćemo',
    'vrištat ćete': 'vrištaćete',
    
    # Wander (Lutat ću -> Lutaću)
    'lutat ću': 'lutaću',
    'Lutat ću': 'Lutaću',
    'lutat ćeš': 'lutaćeš',
    'lutat će': 'lutaće',
    'lutat ćemo': 'lutaćemo',
    'lutat ćete': 'lutaćete',
    
    # Do/Make (Učinit ćemo -> Učinićemo)
    'učinit ću': 'učiniću',
    'Učinit ću': 'Učiniću',
    'učinit ćeš': 'učinićeš',
    'učinit će': 'učiniće',
    'učinit ćemo': 'učinićemo',
    'Učinit ćemo': 'Učinićemo',
    'učinit ćete': 'učinićete',
    
    # Perform/Appear (Nastupit ćeš -> Nastupićeš)
    'nastupit ću': 'nastupiću',
    'nastupit ćeš': 'nastupićeš',
    'Nastupit ćeš': 'Nastupićeš',
    'nastupit će': 'nastupiće',
    'nastupit ćemo': 'nastupićemo',
    'nastupit ćete': 'nastupićete',
    
    # Hide (Sakriti se -> same, but future forms)
    'sakrit ću': 'sakriću',
    'sakrit ćeš': 'sakrićeš',
    'sakrit će': 'sakriće',
    'sakrit ćemo': 'sakrićemo',
    'sakrit ćete': 'sakrićete',
    
    # =====================================================
    # PRICE (cijena -> cena)
    # =====================================================
    'cijena': 'cena',
    'cijenu': 'cenu',
    'cijene': 'cene',
    'cijenom': 'cenom',
    'cijenama': 'cenama',
    'cijeni': 'ceni',
    'cijenjen': 'cenjen',
    'cijenjena': 'cenjena',
    'cijenjeno': 'cenjeno',
    'Cijena': 'Cena',
    'Cijenu': 'Cenu',
    
    # =====================================================
    # LEFT (lijevo -> levo)
    # =====================================================
    'lijevo': 'levo',
    'lijeva': 'leva',
    'lijevi': 'levi',
    'lijeve': 'leve',
    'lijeva': 'leva',
    'lijevog': 'levog',
    'lijevoj': 'levoj',
    'lijevom': 'levom',
    'Lijevo': 'Levo',
    'Lijeva': 'Leva',
    
    # =====================================================
    # RIGHT (desno - same in both)
    # =====================================================
    
    # =====================================================
    # CHILD (dijete -> dete)
    # =====================================================
    'dijete': 'dete',
    'djeteta': 'deteta',
    'djetetu': 'detetu',
    'djetetom': 'detetom',
    'Dijete': 'Dete',
    
    # =====================================================
    # ANIMAL/BEAST (zvijer -> zver)
    # =====================================================
    'zvijer': 'zver',
    'zvijeri': 'zveri',
    'zvijerima': 'zverima',
    'Zvijer': 'Zver',
    'Zvijeri': 'Zveri',
    
    # =====================================================
    # STAR (zvijezda -> zvezda)
    # =====================================================
    'zvijezda': 'zvezda',
    'zvijezde': 'zvezde',
    'zvijezdu': 'zvezdu',
    'zvijezdom': 'zvezdom',
    'zvijezdama': 'zvezdama',
    'Zvijezda': 'Zvezda',
    'Zvijezde': 'Zvezde',
    
    # =====================================================
    # FORWARD (naprijed -> napred)
    # =====================================================
    'naprijed': 'napred',
    'Naprijed': 'Napred',
    'unaprijed': 'unapred',
    'Unaprijed': 'Unapred',
    
    # =====================================================
    # VALUE/WORTH (vrijediti -> vredeti)
    # =====================================================
    'vrijedi': 'vredi',
    'vrijede': 'vrede',
    'vrijedim': 'vredim',
    'vrijediš': 'vrediš',
    'vrijedimo': 'vredimo',
    'vrijedite': 'vredite',
    'Vrijedi': 'Vredi',
    'vrijednost': 'vrednost',
    'vrijednosti': 'vrednosti',
    'Vrijednost': 'Vrednost',
    'vrijedan': 'vredan',
    'vrijedna': 'vredna',
    'vrijedno': 'vredno',
    'vrijedni': 'vredni',
    'Vrijedan': 'Vredan',
    
    # =====================================================
    # UNDERSTAND (razumjeti -> razumeti)
    # =====================================================
    'razumije': 'razume',
    'razumijem': 'razumem',
    'razumiješ': 'razumeš',
    'razumijemo': 'razumemo',
    'razumijete': 'razumete',
    'razumiju': 'razumeju',
    'Razumije': 'Razume',
    'Razumijem': 'Razumem',
    'Razumiješ': 'Razumeš',
    
    # =====================================================
    # HURT/INJURE (ozlijediti -> ozlediti)
    # =====================================================
    'ozlijediti': 'ozlediti',
    'ozlijedio': 'ozledio',
    'ozlijedila': 'ozledila',
    'ozlijedili': 'ozledili',
    'ozlijeđen': 'ozleđen',
    'ozlijeđena': 'ozleđena',
    'ozlijeđeno': 'ozleđeno',
    'Ozlijediti': 'Ozlediti',
    'Ozlijeđen': 'Ozleđen',
    
    # =====================================================
    # SIN (grijeh -> greh)
    # =====================================================
    'grijeh': 'greh',
    'grijeha': 'greha',
    'grijehu': 'grehu',
    'grijehom': 'grehom',
    'Grijeh': 'Greh',
    'griješiti': 'grešiti',
    'griješim': 'grešim',
    'griješiš': 'grešiš',
    'griješi': 'greši',
    'griješimo': 'grešimo',
    'griješite': 'grešite',
    'griješe': 'greše',
    'Griješiti': 'Grešiti',
    
    # =====================================================
    # SOLVE/RESOLVE (riješiti -> rešiti)
    # =====================================================
    'riješiti': 'rešiti',
    'riješio': 'rešio',
    'riješila': 'rešila',
    'riješili': 'rešili',
    'riješeno': 'rešeno',
    'Riješiti': 'Rešiti',
    'Riješeno': 'Rešeno',
    
    # =====================================================
    # MAKE MISTAKE (pogriješiti -> pogrešiti)
    # =====================================================
    'pogriješiti': 'pogrešiti',
    'pogriješio': 'pogrešio',
    'pogriješila': 'pogrešila',
    'pogriješili': 'pogrešili',
    'Pogriješiti': 'Pogrešiti',
    'Pogriješio': 'Pogrešio',
    
    # =====================================================
    # WHOLE/ENTIRE (cijeli -> celi)
    # =====================================================
    'cijeli': 'celi',
    'cijela': 'cela',
    'cijelo': 'celo',
    'cijele': 'cele',
    'cijelog': 'celog',
    'cijeloj': 'celoj',
    'cijelom': 'celom',
    'cijelih': 'celih',
    'Cijeli': 'Celi',
    'Cijela': 'Cela',
    'Cijelo': 'Celo',
    'Cijele': 'Cele',
    
    # =====================================================
    # HURT/INJURED (povrijediti -> povrediti)
    # =====================================================
    'povrijediti': 'povrediti',
    'povrijedio': 'povredio',
    'povrijedila': 'povredila',
    'povrijedili': 'povredili',
    'povrijeđen': 'povređen',
    'povrijeđena': 'povređena',
    'povrijeđeno': 'povređeno',
    'povrijeđeni': 'povređeni',
    'povrijeđene': 'povređene',
    'Povrijediti': 'Povrediti',
    'Povrijeđen': 'Povređen',
    'Povrijeđena': 'Povređena',
    
    # =====================================================
    # DIVISION/SHARE (podjela -> podela)
    # =====================================================
    'podjela': 'podela',
    'podjele': 'podele',
    'podjeli': 'podeli',
    'podjelom': 'podelom',
    'podjelu': 'podelu',
    'Podjela': 'Podela',
    'Podjele': 'Podele',
    'Podjelu': 'Podelu',
    'podjeliti': 'podeliti',
    'podijeliti': 'podeliti',
    'podijelio': 'podelio',
    'podijelila': 'podelila',
    'podijelili': 'podelili',
    'podijele': 'podele',
    'podijeli': 'podeli',
    'Podijeliti': 'Podeliti',
    'Podijeli': 'Podeli',
    
    # =====================================================
    # PASS/CROSS (prijeći -> preći)
    # =====================================================
    'prijeći': 'preći',
    'prešao': 'prešao',
    'prešla': 'prešla',
    'prešli': 'prešli',
    'prijelaz': 'prelaz',
    'prijelaza': 'prelaza',
    'prijelazu': 'prelazu',
    'Prijelaz': 'Prelaz',
    'prijedlog': 'predlog',
    'prijedloga': 'predloga',
    'prijedlogu': 'predlogu',
    'Prijedlog': 'Predlog',
    
    # =====================================================
    # PERSON WORDS (čovjek, ljudi)
    # =====================================================
    'čovjek': 'čovek',
    'čovjeka': 'čoveka',
    'čovjeku': 'čoveku',
    'čovjekom': 'čovekom',
    'čovječe': 'čoveče',
    'Čovjek': 'Čovek',
    'Čovjeka': 'Čoveka',
    'Čovjeku': 'Čoveku',
    'čovječanstvo': 'čovečanstvo',
    'čovječanstva': 'čovečanstva',
    'Čovječanstvo': 'Čovečanstvo',
    
    # GUYS/BOYS (dečki -> momci)
    'dečki': 'momci',
    'dečko': 'momak',
    'dečka': 'momka',
    'dečku': 'momku',
    'dečkom': 'momkom',
    'Dečki': 'Momci',
    'Dečko': 'Momak',
    
    # DOG/PUPPY (psić -> pas)
    'psić': 'pas',
    'psića': 'psa',
    'psiću': 'psu',
    'psićem': 'psom',
    'psići': 'psi',
    'Psić': 'Pas',
    'Psići': 'Psi',
    
    # =====================================================
    # ANGER/RAGE WORDS (bijes -> bes)
    # =====================================================
    'bijes': 'bes',
    'bijesa': 'besa',
    'bijesu': 'besu',
    'bijesom': 'besom',
    'Bijes': 'Bes',
    'bijesan': 'besan',
    'bijesna': 'besna',
    'bijesno': 'besno',
    'bijesni': 'besni',
    'bijesne': 'besne',
    'bijesnu': 'besnu',
    'bijesnog': 'besnog',
    'bijesnoj': 'besnoj',
    'bijesnom': 'besnom',
    'Bijesan': 'Besan',
    'Bijesna': 'Besna',
    'Bijesno': 'Besno',
    'Bijesni': 'Besni',
    'Bijesne': 'Besne',
    'Bijesnom': 'Besnom',
    
    # =====================================================
    # SUCCESS/FAILURE WORDS
    # =====================================================
    'uspjeh': 'uspeh',
    'uspjeha': 'uspeha',
    'uspjehu': 'uspehu',
    'uspjehom': 'uspehom',
    'Uspjeh': 'Uspeh',
    'uspješan': 'uspešan',
    'uspješna': 'uspešna',
    'uspješno': 'uspešno',
    'uspješni': 'uspešni',
    'Uspješan': 'Uspešan',
    'Uspješna': 'Uspešna',
    'Uspješno': 'Uspešno',
    'uspio': 'uspeo',
    'uspjela': 'uspela',
    'uspjeli': 'uspeli',
    'uspjelo': 'uspelo',
    'Uspio': 'Uspeo',
    'Uspjela': 'Uspela',
    'Uspjeli': 'Uspeli',
    'neuspjeh': 'neuspeh',
    'neuspjeha': 'neuspeha',
    'Neuspjeh': 'Neuspeh',
    # Infinitive forms
    'uspjeti': 'uspeti',
    'Uspjeti': 'Uspeti',
    
    # =====================================================
    # DOWN (dolje -> dole)
    # =====================================================
    'dolje': 'dole',
    'Dolje': 'Dole',
    'odozdo': 'odozdo',
    'podalje': 'podalje',
    
    # =====================================================
    # KNEE (koljeno -> koleno)
    # =====================================================
    'koljeno': 'koleno',
    'koljena': 'kolena',
    'koljenu': 'kolenu',
    'koljenom': 'kolenom',
    'koljenima': 'kolenima',
    'Koljeno': 'Koleno',
    'Koljena': 'Kolena',
    
    # =====================================================
    # FORCE/DRIVE (natjerati -> naterati)
    # =====================================================
    'natjerati': 'naterati',
    'natjerao': 'naterao',
    'natjerala': 'naterala',
    'natjerali': 'naterali',
    'natjera': 'natera',
    'Natjerati': 'Naterati',
    'Natjerao': 'Naterao',
    'tjerati': 'terati',
    'tjera': 'tera',
    'tjerao': 'terao',
    'tjerala': 'terala',
    'tjerali': 'terali',
    'Tjerati': 'Terati',
    'istjerati': 'isterati',
    'istjerao': 'isterao',
    'istjerala': 'isterala',
    'istjerali': 'isterali',
    'potjerati': 'poterati',
    'potjerao': 'poterao',
    'potjerala': 'poterala',
    'potjerali': 'poterali',
    'protjerati': 'proterati',
    'protjerao': 'proterao',
    'protjerala': 'proterala',
    'protjerali': 'proterali',
    
    # =====================================================
    # WHITE/BRIGHT WORDS (bijel -> bel)
    # =====================================================
    'bijel': 'beo',
    'bijela': 'bela',
    'bijelo': 'belo',
    'bijeli': 'beli',
    'bijele': 'bele',
    'bijelom': 'belom',
    'bijeloj': 'beloj',
    'bijelih': 'belih',
    'Bijel': 'Beo',
    'Bijela': 'Bela',
    'Bijelo': 'Belo',
    'Bijeli': 'Beli',
    
    # =====================================================
    # LAUGHTER WORDS (smijeh -> smeh)
    # =====================================================
    'smijeh': 'smeh',
    'smijeha': 'smeha',
    'smijehu': 'smehu',
    'smijehom': 'smehom',
    'Smijeh': 'Smeh',
    'smiješan': 'smešan',
    'smiješna': 'smešna',
    'smiješno': 'smešno',
    'smiješni': 'smešni',
    'smiješne': 'smešne',
    'Smiješan': 'Smešan',
    'Smiješna': 'Smešna',
    'Smiješno': 'Smešno',
    'smijati': 'smejati',
    'smijem': 'smejem',
    'smiješ': 'smeješ',
    
    # =====================================================
    # NEXT/FOLLOWING (sljedeći -> sledeći)
    # =====================================================
    'sljedeći': 'sledeći',
    'sljedeća': 'sledeća',
    'sljedeće': 'sledeće',
    'sljedećeg': 'sledećeg',
    'sljedećoj': 'sledećoj',
    'sljedećem': 'sledećem',
    'Sljedeći': 'Sledeći',
    'Sljedeća': 'Sledeća',
    'Sljedeće': 'Sledeće',
    
    # =====================================================
    # WINNER/VICTORY (pobjednik -> pobednik)
    # =====================================================
    'pobjednik': 'pobednik',
    'pobjednika': 'pobednika',
    'pobjedniku': 'pobedniku',
    'pobjednikom': 'pobednikom',
    'pobjednici': 'pobednici',
    'Pobjednik': 'Pobednik',
    'pobjeda': 'pobeda',
    'pobjede': 'pobede',
    'pobjedu': 'pobedu',
    'pobjedom': 'pobedom',
    'Pobjeda': 'Pobeda',
    'pobijediti': 'pobediti',
    'pobijedio': 'pobedio',
    'pobijedila': 'pobedila',
    'pobijedili': 'pobedili',
    
    # =====================================================
    # ESCAPE (pobjeći -> pobeći)
    # =====================================================
    'pobjeći': 'pobeći',
    'pobjegao': 'pobegao',
    'pobjegla': 'pobegla',
    'pobjegli': 'pobegli',
    'Pobjeći': 'Pobeći',
    'bježati': 'bežati',
    'bježim': 'bežim',
    'bježiš': 'bežiš',
    'bježi': 'beži',
    'bježimo': 'bežimo',
    'bježite': 'bežite',
    'bježe': 'beže',
    'Bježati': 'Bežati',
    'Bježi': 'Beži',
    'Bježite': 'Bežite',
    'Bježimo': 'Bežimo',
    
    # =====================================================
    # AVOID (izbjegavati -> izbegavati)
    # =====================================================
    'izbjegavati': 'izbegavati',
    'izbjegavam': 'izbegavam',
    'izbjegavaš': 'izbegavaš',
    'izbjegava': 'izbegava',
    'izbjegavamo': 'izbegavamo',
    'izbjegavate': 'izbegavate',
    'izbjegavaju': 'izbegavaju',
    'izbjegavaj': 'izbegavaj',
    'izbjegavajte': 'izbegavajte',
    'Izbjegavati': 'Izbegavati',
    'Izbjegavajte': 'Izbegavajte',
    'izbjegao': 'izbegao',
    'izbjegla': 'izbegla',
    'izbjegli': 'izbegli',
    
    # =====================================================
    # DIE/DEATH (umrijeti -> umreti)
    # =====================================================
    'umrijeti': 'umreti',
    'umro': 'umro',
    'umrla': 'umrla',
    'umrli': 'umrli',
    'Umrijeti': 'Umreti',
    'smrt': 'smrt',
    'smrti': 'smrti',
    
    # =====================================================
    # WORLD (svijet -> svet) - expanded
    # =====================================================
    'svijet': 'svet',
    'svijeta': 'sveta',
    'svijetu': 'svetu',
    'svjetom': 'svetom',
    'Svijet': 'Svet',
    'svjetski': 'svetski',
    'svjetska': 'svetska',
    'svjetsko': 'svetsko',
    'svjetske': 'svetske',
    'svjetskog': 'svetskog',
    'svjetskoj': 'svetskoj',
    'Svjetski': 'Svetski',
    'Svjetska': 'Svetska',
    'Svjetsko': 'Svetsko',
    'Svjetske': 'Svetske',
    
    # =====================================================
    # LIFELONG (cjeloživotni -> celoživotni)
    # =====================================================
    'cjeloživotna': 'celoživotna',
    'cjeloživotni': 'celoživotni',
    'cjeloživotno': 'celoživotno',
    'Cjeloživotna': 'Celoživotna',
    'Cjeloživotni': 'Celoživotni',
    'cjelokupan': 'celokupan',
    'cjelokupna': 'celokupna',
    'cjelokupno': 'celokupno',
    'Cjelokupan': 'Celokupan',
    
    # =====================================================
    # FAULT/GUILT (krivica)
    # =====================================================
    'krivica': 'krivica',
    'krivnja': 'krivica',
    'krivnje': 'krivice',
    
    # =====================================================
    # EXPLODE
    # =====================================================
    'eksplodirat': 'eksplodiraće',
    'eksplodirati': 'eksplodirati',
    
    # =====================================================
    # LIKE/PLEASE (svidjeti -> svideti)
    # =====================================================
    'svidjeti': 'svideti',
    'svidio': 'svideo',
    'svidjela': 'svidela',
    'svidjeli': 'svideli',
    'svidjelo': 'svidelo',
    'svidje': 'svide',
    'sviđa': 'sviđa',
    
    # =====================================================
    # NOTICE/PERCEIVE (primijetiti -> primetiti)
    # =====================================================
    'primijetiti': 'primetiti',
    'primijetio': 'primetio',
    'primijetila': 'primetila',
    'primijetili': 'primetili',
    'primijete': 'primete',
    'primijeti': 'primeti',
    'Primijetiti': 'Primetiti',
    
    # =====================================================
    # CAPITAL (prijestolnica -> prestonica)
    # =====================================================
    'prijestolnica': 'prestonica',
    'prijestolnice': 'prestonice',
    'prijestolnici': 'prestonici',
    'Prijestolnica': 'Prestonica',
    
    # =====================================================
    # BODY (tijelo -> telo)
    # =====================================================
    'tijelo': 'telo',
    'tijela': 'tela',
    'tijelu': 'telu',
    'tijelom': 'telom',
    'Tijelo': 'Telo',
    'tjelesni': 'telesni',
    'tjelesna': 'telesna',
    'tjelesno': 'telesno',
    
    # =====================================================
    # FLOW/COURSE (tijek -> tok)
    # =====================================================
    'tijek': 'tok',
    'tijeka': 'toka',
    'tijeku': 'toku',
    'tijekom': 'tokom',
    'Tijek': 'Tok',
    'Tijekom': 'Tokom',
    
    # =====================================================
    # PANTS (hlače -> pantalone)
    # =====================================================
    'hlače': 'pantalone',
    'hlača': 'pantalona',
    'hlačama': 'pantalonama',
    'Hlače': 'Pantalone',
    
    # =====================================================
    # PLIERS/TONGS (kliješta -> klešta)
    # =====================================================
    'kliješta': 'klešta',
    'Kliješta': 'Klešta',
    
    # =====================================================
    # SYSTEM (sustav -> sistem)
    # =====================================================
    'sustav': 'sistem',
    'sustava': 'sistema',
    'sustavu': 'sistemu',
    'sustavom': 'sistemom',
    'sustavi': 'sistemi',
    'Sustav': 'Sistem',
    
    # =====================================================
    # FAIR (pošten -> pošten - same but pošteno context)
    # =====================================================
    'pošteno': 'fer',
    'Pošteno': 'Fer',
    
    # =====================================================
    # WANT/WISH verbs (htjeti -> hteti)
    # =====================================================
    'htjeti': 'hteti',
    'htio': 'hteo',
    'htjela': 'htela',
    'htjeli': 'hteli',
    'htjelo': 'htelo',
    'Htjeti': 'Hteti',
    'Htio': 'Hteo',
    'Htjela': 'Htela',
    'Htjeli': 'Hteli',
    
    # =====================================================
    # YESTERDAY (jučer -> juče)
    # =====================================================
    'jučer': 'juče',
    'Jučer': 'Juče',
    
    # =====================================================
    # TOMORROW (sutra - same in both)
    # =====================================================
    
    # =====================================================
    # EVENING (večer -> veče)
    # =====================================================
    'večer': 'veče',
    'večeri': 'večeri',
    'Večer': 'Veče',
    'Večeras': 'Večeras',
    
    # =====================================================
    # SORRY/EXCUSE (oprostiti -> izviniti)
    # =====================================================
    'oprosti': 'izvini',
    'oprostite': 'izvinite',
    'Oprosti': 'Izvini',
    'Oprostite': 'Izvinite',
    
    # =====================================================
    # TRY (pokušati -> probati/pokušati)
    # =====================================================
    'pokušaj': 'pokušaj',
    'pokušajte': 'pokušajte',
    
    # =====================================================
    # SHOULD/NEED (trebati)
    # =====================================================
    'trebao': 'trebao',
    'trebala': 'trebala',
    'trebali': 'trebali',
    
    # =====================================================
    # Common vocabulary differences
    # =====================================================
    'tisuća': 'hiljada',
    'tisuće': 'hiljade',
    'tisući': 'hiljadi',
    'tisućama': 'hiljadama',
    'Tisuća': 'Hiljada',
    'Tisuće': 'Hiljade',
    'Tisući': 'Hiljadi',
    
    'kruh': 'hleb',
    'kruha': 'hleba',
    'kruhu': 'hlebu',
    'kruhom': 'hlebom',
    'Kruh': 'Hleb',
    
    'tjedan': 'nedelja',
    'tjedna': 'nedelje',
    'tjednu': 'nedelji',
    'tjednima': 'nedeljama',
    'Tjedan': 'Nedelja',
    
    'zrak': 'vazduh',
    'zraka': 'vazduha',
    'zraku': 'vazduhu',
    'zrakom': 'vazduhom',
    'Zrak': 'Vazduh',
    
    'vlak': 'voz',
    'vlaka': 'voza',
    'vlaku': 'vozu',
    'vlakom': 'vozom',
    'vlakovi': 'vozovi',
    'vlakova': 'vozova',
    'Vlak': 'Voz',
    
    'kolodvor': 'stanica',
    'kolodvora': 'stanice',
    'kolodvoru': 'stanici',
    'kolodvorom': 'stanicom',
    'Kolodvor': 'Stanica',
    
    'kazalište': 'pozorište',
    'kazališta': 'pozorišta',
    'kazalištu': 'pozorištu',
    'kazalištem': 'pozorištem',
    'Kazalište': 'Pozorište',
    
    'sveučilište': 'univerzitet',
    'sveučilišta': 'univerziteta',
    'sveučilištu': 'univerzitetu',
    'sveučilištem': 'univerzitetom',
    'Sveučilište': 'Univerzitet',
    
    'glazba': 'muzika',
    'glazbe': 'muzike',
    'glazbi': 'muzici',
    'glazbom': 'muzikom',
    'glazbeni': 'muzički',
    'glazbena': 'muzička',
    'glazbeno': 'muzičko',
    'Glazba': 'Muzika',
    
    'otok': 'ostrvo',
    'otoka': 'ostrva',
    'otoku': 'ostrvu',
    'otokom': 'ostrvom',
    'otoci': 'ostrva',
    'Otok': 'Ostrvo',
    
    'tvrtka': 'firma',
    'tvrtke': 'firme',
    'tvrtki': 'firmi',
    'tvrtkom': 'firmom',
    'Tvrtka': 'Firma',
    
    'udruga': 'udruženje',
    'udruge': 'udruženja',
    'udruzi': 'udruženju',
    'udrugom': 'udruženjem',
    'Udruga': 'Udruženje',
    
    'opća': 'opšta',
    'opći': 'opšti',
    'opće': 'opšte',
    'općeg': 'opšteg',
    'općoj': 'opštoj',
    'općim': 'opštim',
    'općenito': 'uopšte',
    'Opća': 'Opšta',
    'Opći': 'Opšti',
    'Opće': 'Opšte',
    
    'osobito': 'naročito',
    'Osobito': 'Naročito',
    
    'točno': 'tačno',
    'točan': 'tačan',
    'točna': 'tačna',
    'točke': 'tačke',
    'točku': 'tačku',
    'točka': 'tačka',
    'Točno': 'Tačno',
    'Točka': 'Tačka',
    
    'tečaj': 'kurs',
    'tečaja': 'kursa',
    'tečaju': 'kursu',
    'tečajem': 'kursom',
    'Tečaj': 'Kurs',
    
    'uspjeh': 'uspeh',
    'uspjeha': 'uspeha',
    'uspjehu': 'uspehu',
    'uspjehom': 'uspehom',
    'uspješan': 'uspešan',
    'uspješna': 'uspešna',
    'uspješno': 'uspešno',
    'Uspjeh': 'Uspeh',
    'Uspješan': 'Uspešan',
    
    'pogreška': 'greška',
    'pogreške': 'greške',
    'pogrešku': 'grešku',
    'pogreškom': 'greškom',
    'Pogreška': 'Greška',
    
    'mjera': 'mera',
    'mjere': 'mere',
    'mjeri': 'meri',
    'mjerom': 'merom',
    'Mjera': 'Mera',
    
    'mjeren': 'meren',
    'mjerenje': 'merenje',
    'mjerenja': 'merenja',
    'mjeriti': 'meriti',
    
    'mjesto': 'mesto',
    'mjesta': 'mesta',
    'mjestu': 'mestu',
    'mjestom': 'mestom',
    'Mjesto': 'Mesto',
    
    'mjesec': 'mesec',
    'mjeseca': 'meseca',
    'mjesecu': 'mesecu',
    'mjesecom': 'mesecom',
    'mjeseci': 'meseci',
    'Mjesec': 'Mesec',
    
    'sjeme': 'seme',
    'sjemena': 'semena',
    'sjemenu': 'semenu',
    'Sjeme': 'Seme',
    
    'sjever': 'sever',
    'sjevera': 'severa',
    'sjeveru': 'severu',
    'sjeverni': 'severni',
    'sjeverna': 'severna',
    'sjeverno': 'severno',
    'Sjever': 'Sever',
    
    'vrijeme': 'vreme',
    'vremena': 'vremena',
    'vremenu': 'vremenu',
    'Vrijeme': 'Vreme',
    
    'riječ': 'reč',
    'riječi': 'reči',
    'riječima': 'rečima',
    'riječju': 'rečju',
    'Riječ': 'Reč',
    
    'rječnik': 'rečnik',
    'rječnika': 'rečnika',
    'rječniku': 'rečniku',
    'Rječnik': 'Rečnik',
    
    'rijeka': 'reka',
    'rijeke': 'reke',
    'rijeci': 'reci',
    'rijekom': 'rekom',
    'Rijeka': 'Reka',
    
    'liječnik': 'lekar',
    'liječnika': 'lekara',
    'liječniku': 'lekaru',
    'liječnici': 'lekari',
    'Liječnik': 'Lekar',
    
    'liječenje': 'lečenje',
    'liječenja': 'lečenja',
    'liječiti': 'lečiti',
    'Liječenje': 'Lečenje',
    
    'lijek': 'lek',
    'lijeka': 'leka',
    'lijeku': 'leku',
    'lijekom': 'lekom',
    'lijekovi': 'lekovi',
    'Lijek': 'Lek',
    
    'lijepa': 'lepa',
    'lijep': 'lep',
    'lijepo': 'lepo',
    'lijepog': 'lepog',
    'lijepoj': 'lepoj',
    'Lijep': 'Lep',
    'Lijepa': 'Lepa',
    'Lijepo': 'Lepo',
    
    'mlijeko': 'mleko',
    'mlijeka': 'mleka',
    'mlijeku': 'mleku',
    'Mlijeko': 'Mleko',
    
    'cvijet': 'cvet',
    'cvijeta': 'cveta',
    'cvijetu': 'cvetu',
    'cvijeće': 'cveće',
    'cvijećem': 'cvećem',
    'Cvijet': 'Cvet',
    'Cvijeće': 'Cveće',
    
    'svijet': 'svet',
    'svijeta': 'sveta',
    'svijetu': 'svetu',
    'Svijet': 'Svet',
    
    'svjetlo': 'svetlo',
    'svjetla': 'svetla',
    'svjetlu': 'svetlu',
    'Svjetlo': 'Svetlo',
    
    'djeca': 'deca',
    'djece': 'dece',
    'djeci': 'deci',
    'djecom': 'decom',
    'djecu': 'decu',
    'Djeca': 'Deca',
    'Djecu': 'Decu',
    
    'dječak': 'dečak',
    'dječaka': 'dečaka',
    'dječaku': 'dečaku',
    'dječaci': 'dečaci',
    'Dječak': 'Dečak',
    
    'djevojka': 'devojka',
    'djevojke': 'devojke',
    'djevojci': 'devojci',
    'djevojkom': 'devojkom',
    'Djevojka': 'Devojka',
    
    'djed': 'deda',
    'djeda': 'dede',
    'djedu': 'dedi',
    'djedom': 'dedom',
    'Djed': 'Deda',
    
    'djelovati': 'delovati',
    'djeluje': 'deluje',
    'djelujem': 'delujem',
    'djelovanje': 'delovanje',
    
    'povijest': 'istorija',
    'povijesti': 'istorije',
    'poviješću': 'istorijom',
    'povijesni': 'istorijski',
    'povijesna': 'istorijska',
    'povijesno': 'istorijsko',
    'povijesnim': 'istorijskim',
    'povijesnih': 'istorijskih',
    'povijesne': 'istorijske',
    'Povijest': 'Istorija',
    'Povijesni': 'Istorijski',
    
    'odgoj': 'vaspitanje',
    'odgoja': 'vaspitanja',
    'odgoju': 'vaspitanju',
    'odgojiti': 'vaspitati',
    'Odgoj': 'Vaspitanje',
    
    'promicati': 'promovisati',
    'promiče': 'promoviše',
    
    'tražilica': 'pretraživač',
    'tražilice': 'pretraživača',
    'tražilici': 'pretraživaču',
    'Tražilica': 'Pretraživač',
    
    'računalo': 'računar',
    'računala': 'računara',
    'računalu': 'računaru',
    'računalom': 'računarom',
    'Računalo': 'Računar',
    
    'tipkovnica': 'tastatura',
    'tipkovnice': 'tastature',
    'tipkovnici': 'tastaturi',
    'tipkovnicom': 'tastaturom',
    'Tipkovnica': 'Tastatura',
    
    'zaslon': 'ekran',
    'zaslona': 'ekrana',
    'zaslonu': 'ekranu',
    'zaslonom': 'ekranom',
    'Zaslon': 'Ekran',
    
    'datoteka': 'fajl',
    'datoteke': 'fajla',
    'datoteci': 'fajlu',
    'datotekom': 'fajlom',
    'Datoteka': 'Fajl',
    
    'mapa': 'folder',
    'mape': 'foldera',
    'mapi': 'folderu',
    'mapom': 'folderom',
    
    'pričekaj': 'sačekaj',
    'pričekajte': 'sačekajte',
    'Pričekaj': 'Sačekaj',
    'Pričekajte': 'Sačekajte',
    
    'odabrati': 'izabrati',
    'odabir': 'izbor',
    'odabira': 'izbora',
    'odabiru': 'izboru',
    'Odabrati': 'Izabrati',
    'Odabir': 'Izbor',
    
    'cesta': 'put',
    'ceste': 'puta',
    'cesti': 'putu',
    'cestom': 'putem',
    'Cesta': 'Put',
    
    'sat': 'čas',
    'sata': 'časa',
    'satu': 'času',
    'satom': 'časom',
    'sati': 'časova',
    'satima': 'časovima',
    
    'šalica': 'šolja',
    'šalice': 'šolje',
    'šalici': 'šolji',
    'šalicom': 'šoljom',
    'Šalica': 'Šolja',
    
    'žlica': 'kašika',
    'žlice': 'kašike',
    'žlici': 'kašici',
    'žlicom': 'kašikom',
    'Žlica': 'Kašika',
    
    'zrcalo': 'ogledalo',
    'zrcala': 'ogledala',
    'zrcalu': 'ogledalu',
    'zrcalom': 'ogledalom',
    'Zrcalo': 'Ogledalo',
    
    'tvornica': 'fabrika',
    'tvornice': 'fabrike',
    'tvornici': 'fabrici',
    'tvornicom': 'fabrikom',
    'Tvornica': 'Fabrika',
    
    'poduzeće': 'preduzeće',
    'poduzeća': 'preduzeća',
    'poduzeću': 'preduzeću',
    'poduzećem': 'preduzećem',
    'Poduzeće': 'Preduzeće',
    
    'športski': 'sportski',
    'šport': 'sport',
    'športa': 'sporta',
    'športu': 'sportu',
    'Šport': 'Sport',
    
    'nutarnji': 'unutrašnji',
    'nutarnja': 'unutrašnja',
    'nutarnje': 'unutrašnje',
    
    'izvanjski': 'spoljašnji',
    'izvanjska': 'spoljašnja',
    'izvanjsko': 'spoljašnje',
    
    'prošle': 'prošle',
    
    'pisati ću': 'pisaću',
    'raditi ću': 'radiću',
    'doći ću': 'doći ću',
    
    'trebao bih': 'trebalo bi',
    
    # Question words
    'što': 'šta',
    'Što': 'Šta',
    
    'tko': 'ko',
    'Tko': 'Ko',
    
    'netko': 'neko',
    'Netko': 'Neko',
    
    'nitko': 'niko',
    'Nitko': 'Niko',
    
    'svatko': 'svako',
    'Svatko': 'Svako',
    
    'itko': 'iko',
    'Itko': 'Iko',
    
    # Conjunctions and particles
    'također': 'takođe',
    'Također': 'Takođe',
    
    'uopće': 'uopšte',
    'Uopće': 'Uopšte',
    
    'inače': 'inače',
    
    'jako': 'jako',
    
    'možda': 'možda',
    
    # Verb forms
    'htjeti': 'hteti',
    'htio': 'hteo',
    'htjela': 'htela',
    'htjeli': 'hteli',
    
    'smjeti': 'smeti',
    'smio': 'smeo',
    'smjela': 'smela',
    'smjeli': 'smeli',
    
    'vidjeti': 'videti',
    'vidio': 'video',
    'vidjela': 'videla',
    'vidjeli': 'videli',
    
    'razumjeti': 'razumeti',
    'razumio': 'razumeo',
    'razumjela': 'razumela',
    'razumjeli': 'razumeli',
    
    'željeti': 'želeti',
    'želio': 'želeo',
    'željela': 'želela',
    'željeli': 'želeli',
    
    'letjeti': 'leteti',
    'letio': 'leteo',
    'letjela': 'letela',
    'letjeli': 'leteli',
    
    'trčati': 'trčati',
    
    'voljeti': 'voleti',
    'volio': 'voleo',
    'voljela': 'volela',
    'voljeli': 'voleli',
    
    'živjeti': 'živeti',
    'živio': 'živeo',
    'živjela': 'živela',
    'živjeli': 'živeli',
    
    'sjediti': 'sedeti',
    'sjedio': 'sedeo',
    'sjedila': 'sedela',
    'sjedili': 'sedeli',
    'sjedi': 'sedi',
    'sjedim': 'sedim',
    'sjedala': 'sedala',
    'sjedalo': 'sedalo',
    'Sjedala': 'Sedala',
    
    'sjesti': 'sesti',
    'sjeo': 'seo',
    'sjela': 'sela',
    'sjeli': 'seli',
    
    # BELIEVE (vjerovati -> verovati)
    'vjerovati': 'verovati',
    'vjerujem': 'verujem',
    'vjeruješ': 'veruješ',
    'vjeruje': 'veruje',
    'vjerujemo': 'verujemo',
    'vjerujete': 'verujete',
    'vjeruju': 'veruju',
    'vjerovao': 'verovao',
    'vjerovala': 'verovala',
    'vjerovali': 'verovali',
    'Vjerovati': 'Verovati',
    'Vjerujem': 'Verujem',
    'Vjeruješ': 'Veruješ',
    'Vjeruje': 'Veruje',
    'nevjerica': 'neverica',
    'nevjerice': 'neverice',
    'nevjerici': 'neverici',
    'povjerovao': 'poverovao',
    'povjerovala': 'poverovala',
    'povjerovali': 'poverovali',
    'povjeren': 'poveren',
    'povjerenje': 'poverenje',
    'povjerenja': 'poverenja',
    'Povjerenje': 'Poverenje',
    
    # CHECK/VERIFY (provjeriti -> proveriti)
    'provjeriti': 'proveriti',
    'provjerio': 'proverio',
    'provjerila': 'proverila',
    'provjerili': 'proverili',
    'provjeri': 'proveri',
    'provjerim': 'proverim',
    'provjerava': 'proverava',
    'provjeravati': 'proveravati',
    'Provjeriti': 'Proveriti',
    
    # EXERCISE (vježbati -> vežbati)
    'vježbati': 'vežbati',
    'vježbam': 'vežbam',
    'vježbaš': 'vežbaš',
    'vježba': 'vežba',
    'vježbamo': 'vežbamo',
    'vježbate': 'vežbate',
    'vježbaju': 'vežbaju',
    'vježbaj': 'vežbaj',
    'Vježbati': 'Vežbati',
    'Vježba': 'Vežba',
    
    # ARTIST (umjetnik -> umetnik)
    'umjetnik': 'umetnik',
    'umjetnika': 'umetnika',
    'umjetniku': 'umetniku',
    'umjetnikom': 'umetnikom',
    'umjetnici': 'umetnici',
    'Umjetnik': 'Umetnik',
    'Umjetnici': 'Umetnici',
    'umjetnost': 'umetnost',
    'umjetnosti': 'umetnosti',
    'Umjetnost': 'Umetnost',
    
    # NOTICE (primijetiti -> primetiti) - additional forms
    'neprimijećen': 'neprimećen',
    'neprimijećena': 'neprimećena',
    'neprimijećeno': 'neprimećeno',
    'Neprimijećen': 'Neprimećen',
    # Also handle variant without 'i' (neprimjećen)
    'neprimjećen': 'neprimećen',
    'neprimjećena': 'neprimećena',
    'neprimjećeno': 'neprimećeno',
    'Neprimjećen': 'Neprimećen',
    
    # WITNESS (svjedočiti -> svedočiti)
    'svjedočiti': 'svedočiti',
    'svjedočim': 'svedočim',
    'svjedočiš': 'svedočiš',
    'svjedoči': 'svedoči',
    'svjedočimo': 'svedočimo',
    'svjedočite': 'svedočite',
    'svjedoče': 'svedoče',
    'svjedočio': 'svedočio',
    'svjedočila': 'svedočila',
    'svjedočili': 'svedočili',
    'Svjedočiti': 'Svedočiti',
    'svjedočit': 'svedočit',
    'svjedok': 'svedok',
    'svjedoka': 'svedoka',
    'svjedoku': 'svedoku',
    'Svjedok': 'Svedok',
    
    # SENSITIVE (osjetljiv -> osetljiv)
    'osjetljiv': 'osetljiv',
    'osjetljiva': 'osetljiva',
    'osjetljivo': 'osetljivo',
    'osjetljivi': 'osetljivi',
    'osjetljive': 'osetljive',
    'osjetljivog': 'osetljivog',
    'osjetljivoj': 'osetljivoj',
    'osjetljivom': 'osetljivom',
    'osjetljivim': 'osetljivim',
    'osjetljivih': 'osetljivih',
    'neosjetljiv': 'neosetljiv',
    'neosjetljiva': 'neosetljiva',
    'neosjetljivo': 'neosetljivo',
    'neosjetljivi': 'neosetljivi',
    'neosjetljivim': 'neosetljivim',
    'Osjetljiv': 'Osetljiv',
    
    # NEIGHBOR (susjed -> komšija/sused)
    'susjed': 'komšija',
    'susjeda': 'komšije',
    'susjedu': 'komšiji',
    'susjedom': 'komšijom',
    'susjedi': 'komšije',
    'Susjed': 'Komšija',
    'susjedstvo': 'komšiluk',
    'susjedstva': 'komšiluka',
    'Susjedstvo': 'Komšiluk',
    
    # REFRESH (osvježiti -> osvežiti)
    'osvježiti': 'osvežiti',
    'osvježio': 'osvežio',
    'osvježila': 'osvežila',
    'osvježili': 'osvežili',
    'osvježi': 'osveži',
    'osvježenje': 'osveženje',
    'osvježenja': 'osveženja',
    'osvježenju': 'osveženju',
    'Osvježiti': 'Osvežiti',
    'Osvježenje': 'Osveženje',
    
    # GIRL diminutive (djevojčica -> devojčica)
    'djevojčica': 'devojčica',
    'djevojčice': 'devojčice',
    'djevojčici': 'devojčici',
    'djevojčicom': 'devojčicom',
    'djevojčicu': 'devojčicu',
    'Djevojčica': 'Devojčica',
    'Djevojčicu': 'Devojčicu',
    
    # More common words
    'Europa': 'Evropa',
    'Europe': 'Evrope',
    'Europi': 'Evropi',
    'Europom': 'Evropom',
    'europski': 'evropski',
    'europska': 'evropska',
    'europsko': 'evropsko',
    
    'organizacija': 'organizacija',
    
    'odlično': 'odlično',
    
    'dobro': 'dobro',
    
    # Days of week - Croatian to Serbian
    'ponedjeljak': 'ponedeljak',
    'ponedjeljka': 'ponedeljka',
    'ponedjeljku': 'ponedeljku',
    'Ponedjeljak': 'Ponedeljak',
    
    'srijeda': 'sreda',
    'srijede': 'srede',
    'srijedu': 'sredu',
    'srijedom': 'sredom',
    'Srijeda': 'Sreda',
    
    # Months
    'siječanj': 'januar',
    'siječnja': 'januara',
    'siječnju': 'januaru',
    'Siječanj': 'Januar',
    
    'veljača': 'februar',
    'veljače': 'februara',
    'veljači': 'februaru',
    'Veljača': 'Februar',
    
    'ožujak': 'mart',
    'ožujka': 'marta',
    'ožujku': 'martu',
    'Ožujak': 'Mart',
    
    'travanj': 'april',
    'travnja': 'aprila',
    'travnju': 'aprilu',
    'Travanj': 'April',
    
    'svibanj': 'maj',
    'svibnja': 'maja',
    'svibnju': 'maju',
    'Svibanj': 'Maj',
    
    'lipanj': 'jun',
    'lipnja': 'juna',
    'lipnju': 'junu',
    'Lipanj': 'Jun',
    
    'srpanj': 'jul',
    'srpnja': 'jula',
    'srpnju': 'julu',
    'Srpanj': 'Jul',
    
    'kolovoz': 'avgust',
    'kolovoza': 'avgusta',
    'kolovozu': 'avgustu',
    'Kolovoz': 'Avgust',
    
    'rujan': 'septembar',
    'rujna': 'septembra',
    'rujnu': 'septembru',
    'Rujan': 'Septembar',
    
    'listopad': 'oktobar',
    'listopada': 'oktobra',
    'listopadu': 'oktobru',
    'Listopad': 'Oktobar',
    
    'studeni': 'novembar',
    'studenoga': 'novembra',
    'studenom': 'novembru',
    'Studeni': 'Novembar',
    
    'prosinac': 'decembar',
    'prosinca': 'decembra',
    'prosincu': 'decembru',
    'Prosinac': 'Decembar',
}

# Build regex pattern - sort by length descending to match longer words first
# Use word boundaries to avoid partial matches
def build_pattern():
    """Build regex pattern with word boundaries."""
    sorted_keys = sorted(CROATIAN_TO_SERBIAN.keys(), key=len, reverse=True)
    escaped_keys = [re.escape(k) for k in sorted_keys]
    pattern = r'\b(' + '|'.join(escaped_keys) + r')\b'
    return re.compile(pattern)

PATTERN = build_pattern()


def croatian_to_serbian(text: str) -> str:
    """Convert Croatian text to Serbian vocabulary."""
    return PATTERN.sub(lambda m: CROATIAN_TO_SERBIAN[m.group()], text)


def detect_encoding(file_path: Path) -> str:
    """Try to detect the file encoding."""
    encodings = ['utf-8', 'utf-8-sig', 'cp1250', 'cp1251', 'iso-8859-2', 'iso-8859-1', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    return 'utf-8'  # fallback


def translate_file(input_path: Path, output_path: Path = None, in_place: bool = False) -> tuple:
    """
    Translate Croatian words to Serbian in a file.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file (optional, defaults to adding '_sr' suffix)
        in_place: If True, modify the file in place
    
    Returns:
        Tuple of (success: bool, changes_count: int)
    """
    try:
        # Detect and read with appropriate encoding
        encoding = detect_encoding(input_path)
        print(f"  Detected encoding: {encoding}")
        
        with open(input_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        # Count changes
        original_content = content
        
        # Translate Croatian to Serbian
        translated_content = croatian_to_serbian(content)
        
        # Count how many replacements were made
        changes_count = sum(1 for a, b in zip(original_content.split(), translated_content.split()) if a != b)
        
        # Determine output path
        if in_place:
            final_output_path = input_path
        elif output_path:
            final_output_path = output_path
        else:
            # Add '_sr' suffix before extension
            final_output_path = input_path.parent / f"{input_path.stem}_sr{input_path.suffix}"
        
        # Ensure output directory exists
        final_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with UTF-8 encoding
        with open(final_output_path, 'w', encoding='utf-8-sig') as f:
            f.write(translated_content)
        
        return True, changes_count
    
    except Exception as e:
        print(f"  Error: {e}")
        return False, 0


def translate_text(text: str) -> str:
    """
    Translate Croatian words to Serbian in a text string.
    
    Args:
        text: Input text in Croatian
    
    Returns:
        Text with Croatian words replaced by Serbian equivalents
    """
    return croatian_to_serbian(text)


def main():
    """Main function to process files or demonstrate translation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Translate Croatian vocabulary to Serbian in subtitle files'
    )
    parser.add_argument(
        'input', 
        nargs='?',
        help='Input file or directory to translate'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file or directory'
    )
    parser.add_argument(
        '-i', '--in-place',
        action='store_true',
        help='Modify files in place'
    )
    parser.add_argument(
        '-t', '--text',
        help='Translate a text string directly'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    args = parser.parse_args()
    
    # If text argument provided, translate and print
    if args.text:
        print("Original:", args.text)
        print("Translated:", translate_text(args.text))
        return
    
    # If no input provided, show demo
    if not args.input:
        print("Croatian to Serbian Translator")
        print("=" * 50)
        print("\nDemo translations:")
        demo_sentences = [
            "Što radiš?",
            "Tko je tamo?",
            "Imam tisuću razloga.",
            "Vlak dolazi u pet sati.",
            "Djeca su na igralištu.",
            "Vidio sam lijep cvijet.",
            "Vrijeme je za ručak.",
            "Idemo u kazalište.",
            "Računalo ne radi.",
            "Siječanj je hladan mjesec.",
        ]
        
        for sentence in demo_sentences:
            translated = translate_text(sentence)
            print(f"\n  HR: {sentence}")
            print(f"  SR: {translated}")
        
        print("\n" + "=" * 50)
        print("\nUsage:")
        print("  python translate_croatian_to_serbian.py file.srt")
        print("  python translate_croatian_to_serbian.py -t 'Što radiš?'")
        print("  python translate_croatian_to_serbian.py -r input_folder/ -o output_folder/")
        return
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist!")
        return
    
    # Process single file
    if input_path.is_file():
        print(f"Translating: {input_path.name}")
        output_path = Path(args.output) if args.output else None
        success, changes = translate_file(input_path, output_path, args.in_place)
        
        if success:
            print(f"  ✓ Translation complete ({changes} words changed)")
        else:
            print(f"  ✗ Translation failed")
        return
    
    # Process directory
    if input_path.is_dir():
        if args.recursive:
            files = list(input_path.glob('**/*.srt'))
        else:
            files = list(input_path.glob('*.srt'))
        
        if not files:
            print(f"No .srt files found in '{input_path}'")
            return
        
        print(f"Found {len(files)} SRT file(s) to translate")
        print("-" * 50)
        
        success_count = 0
        for srt_file in files:
            print(f"\nProcessing: {srt_file.name}")
            
            if args.output:
                output_dir = Path(args.output)
                relative_path = srt_file.relative_to(input_path)
                output_path = output_dir / relative_path
            else:
                output_path = None
            
            success, changes = translate_file(srt_file, output_path, args.in_place)
            
            if success:
                print(f"  ✓ Complete ({changes} words changed)")
                success_count += 1
            else:
                print(f"  ✗ Failed")
        
        print("\n" + "=" * 50)
        print(f"Translation complete: {success_count}/{len(files)} files processed")


if __name__ == '__main__':
    main()
