#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=True)

#from plotly.graph_objs import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import datetime
import string
import sys
import csv
import re

from collections import Counter, namedtuple
from unidecode   import unidecode

# Colour pallete (kids to adults)
cp = [(179,0,0), (227,74,51), (252,141,89), (54,144,192)]

# Colour pallete (independent groups)
cp2 = [(166,206,227), (31,120,180), (178,223,138), (51,160,44), (251,154,153), \
       (227,26,28), (253,191,111), (255,127,0), (202,178,214), (106,61,154)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(cp)):    
    r, g, b = cp[i]    
    cp[i] = (r / 255., g / 255., b / 255.)    
for i in range(len(cp2)):
    r, g, b = cp2[i]
    cp2[i] = (r / 255., g / 255., b / 255.)

# General
def remove2axis(ax):   # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

# load CSV data
def showCsvStats( listContent, strFile ):
    
    print ( '\n\n -< Archivo: %s >-' % strFile )

    print ( ' -< Nunero de entradas: %4d >-' % len(listContent) )
    print ( ' -< Numero de campos: %4d >-\n' % len(listContent[0]) )

    # Check number of entries per column and the most common value
    print ( "    CAMPO       | # Entradas | # Ent. UNICAS | Ent. MAS COMUN (#)" )
    print ( "-----------------------------------------------------------------" )

    for field in sorted(listContent[0].keys()):

        # get all entries for 1 fields in one list
        fieldListAll = [dic[field] for dic in listContent]

        # remove empteis and capitalise
        fieldList = [f.upper() for f in fieldListAll if f != '']

        if len(fieldList) > 0:
            count = Counter(fieldList)
            print ( "%-15s | %10d | %12d  | (%4d) %s  " % (field, len(fieldList), \
                    len(count), count.most_common(1)[0][1], count.most_common(1)[0][0]) )
        else:
            print ( "%-15s | %10d |" % ( field, len(fieldList)) ) 

    print ( "-----------------------------------------------------------------" )

def csvToDicList( strFile, showStats=True ):

    file  = open(strFile, "r")
    dicContent = csv.DictReader(file)
    listContent = []

    for d in dicContent :
        listContent.append(d)

    if showStats:
        showCsvStats( listContent, strFile )

    return listContent

def adjustName ( stringIN ):

    dicNombresModernos = {  'Josef':     'Jose', \
                            'Joseph':    'Jose', \
                            'Josep':     'Jose', \
                            'Jusep':     'Jose', \
                            'Jusepe':    'Jose', \
                            'Josepha':   'Josefa', \
                            'Josepa':    'Josefa', \
                            'Jusepa':    'Josefa', \
                            'Anna':      'Ana', \
                            'Ynes':      'Ines', \
                            'Ysabel':    'Isabel', \
                            'Ygnacia':   'Ignacia', \
                            'Mathias':   'Matias', \
                            'Jayme':     'Jaime', \
                            'Thomas':    'Tomas', \
                            'Thomasa':   'Tomasa', \
                            'Theresa':   'Teresa', \
                            'Pasqual':   'Pascual', \
                            'Pasquala':  'Pascuala', \
                            'Xavier':    'Javier', \
                            'Xaviera':   'Javiera', \
                            'Cristoval': 'Cristobal', \
                            'Hursola':   'Ursula', \
                            'Joachina':  'Juaquina', \
                            'Juachina':  'Juaquina', \
                            'Raymundo':  'Raimundo', \
                            'Raymunda':  'Raimunda', \
                            'Joachin':   'Juaquin', \
                            'Juachin':   'Juaquin', \
                            'Joaquin':   'Juaquin', \
                            'Joachim':   'Juaquin' }

    nameList = stringIN.split()

    for i, nombre in enumerate(nameList):
        if nombre in dicNombresModernos:
            #print ( '%s -> %s  in  (%s)' % (nombre, dicNombresModernos[nombre], stringIN))
            nameList[i] = dicNombresModernos[nombre]
            #print('.', end="")

    #print( '%s | %s | %s' % (nameList, [' '.join(nameList)], [stringIN]) )

    return ' '.join(nameList)

def noAccents ( stringIN ):

    return unidecode(stringIN) # remove accents and stange characters

def createNacimientos( dicList ):
    
    print ( '  ---- Creando diccionario de nacimientos ----')
    nacimientos = []

    for i, dic in enumerate(dicList):

        persona = dict()

        persona['ID']               = dic['ID']
        persona['nombre']           = noAccents(string.capwords( dic['NOMBRE']))
        persona['nombreAjustado']   = adjustName(persona['nombre'])
        persona['apellido1']        = noAccents(string.capwords(dic['APELL1']))
        persona['apellido2']        = noAccents(string.capwords(dic['APELL2']))
        persona['sexo']             = string.capwords(dic['SEXO'])

        persona['nacimientoEstimado']   = datetime.date(1,1,1)
        try: 
            persona['bautismo']     = datetime.datetime.strptime(dic['BAUTISMO'], '%d.%m.%Y').date()
            persona['nacimientoEstimado'] = persona['bautismo'] # copy baustimso as estimated date of birth
        except:
            persona['bautismo']     = datetime.date(1,1,1)

        try: 
            persona['nacimiento']   = datetime.datetime.strptime(dic['NACIMIENTO'], '%d.%m.%Y').date()
            persona['nacimientoEstimado'] = persona['nacimiento'] # if nacimiento exists, overwrite it
        except:
            persona['nacimiento']   = datetime.date(1,1,1)


        persona['padreNombre']          = noAccents(string.capwords(dic['NOMPADRE']))
        persona['madreNombre']          = noAccents(string.capwords(dic['NOMMADRE']))

        persona['padreNombreAjustado']  = adjustName(persona['padreNombre'])
        persona['madreNombreAjustado']  = adjustName(persona['madreNombre'])

        persona['padreApellido2']       = noAccents(string.capwords(dic['APELL2PAD']))
        persona['madreApellido2']       = noAccents(string.capwords(dic['APELL2MAD']))

        persona['observaciones']    = dic['OBSERVACN']

        nacimientos.append( persona )

    #print ( '\n  --------------------------------------------\n')

    return nacimientos

def createDefunciones( dicList ):
    
    print ( '  ---- Creando diccionario de defunciones ----')
    defunciones = []

    for i, dic in enumerate(dicList):

        persona = dict()

        persona['ID']               = dic['ID']
        persona['nombre']           = noAccents(string.capwords( dic['NOMBRE']))
        persona['nombreAjustado']   = adjustName(persona['nombre'])
        persona['apellido1']        = noAccents(string.capwords(dic['APELL1']))
        persona['apellido2']        = noAccents(string.capwords(dic['APELL2']))
        persona['sexo']             = string.capwords(dic['SEXO'])

        # Becase sometimes APELLIDO is empty and it is stored in APELLPAD2...
        if persona['apellido1'] == '':
            persona['apellido1'] = string.capwords(dic['APELL2PAD'])
        if persona['apellido2'] == '':
            persona['apellido2'] = string.capwords(dic['APELL2MAD'])


        persona['defuncionEstimado']= datetime.date(1,1,1)
        try: 
            persona['entierro']     = datetime.datetime.strptime(dic['ENTERRAMIE'], '%d %m %Y').date()
            persona['defuncionEstimado']    = persona['entierro'] # Copy as estimated, in case there is no defuncion
        except:
            persona['entierro']     = datetime.date(1,1,1)

        try: 
            persona['defuncion']    = datetime.datetime.strptime(dic['DEFUNCION'], '%d %m %Y').date()
            persona['defuncionEstimado']    = persona['defuncion']
        except:
            persona['defuncion']    = datetime.date(1,1,1)

        persona['padreNombre']          = noAccents(string.capwords(dic['NOMPADRE']))
        persona['madreNombre']          = noAccents(string.capwords(dic['NOMMADRE']))

        persona['padreNombreAjustado']  = adjustName(persona['padreNombre'])
        persona['madreNombreAjustado']  = adjustName(persona['madreNombre'])

        #persona['padreApellido2']       = noAccents(string.capwords(dic['APELL2PAD']))
        #persona['madreApellido2']       = noAccents(string.capwords(dic['APELL2MAD']))
        persona['padreApellido2']       = '' # I don't trust them
        persona['madreApellido2']       = ''

        persona['edadTexto']        = dic['edatTEXT']
        persona['oficio']           = dic['OFICIO']

        persona['observaciones']    = dic['OBSERVACN']

        defunciones.append( persona )

    #print ( '\n  --------------------------------------------\n')
    return defunciones

# Merge databases
def isSameName ( n1, n2 ):
    if n1 == 'Maria' and n1 == n2 or \
       n1 == 'Jose'  and n1 == n2:
       return True

    n1list = n1.split()
    n2list = n2.split()

    n1list = [n for n in n1list if n != 'Maria' and n != 'Jose']
    n2list = [n for n in n2list if n != 'Maria' and n != 'Jose']

    if len(set(n1list) & set(n2list)) > 0:
        return True

    return False

def isSamePerson( n, d ):

    if n['nombreAjustado'] != '' and n['apellido1'] != '' and n['apellido2'] != '' and \
       isSameName(n['nombreAjustado'], d['nombreAjustado']) and \
       n['apellido1'] == d['apellido1'] and \
       n['apellido2'] == d['apellido2'] and \
       d['defuncionEstimado'] >= n['nacimientoEstimado'] and \
       d['defuncionEstimado'].year - n['nacimientoEstimado'].year < 100 and \
       n['sexo'] == d['sexo']:
       #n['padreApellido2'] == d['padreApellido2'] and \
       #n['madreApellido2'] == d['madreApellido2']:
           return True

    return False

def mergePerson( n, d, id_matching ):

        persona = dict()

        persona['ID']                   = id_matching
        persona['IDn']                  = n['ID']
        persona['IDd']                  = d['ID']

        persona['nombre']               = n['nombre']
        persona['apellido1']            = n['apellido1']
        persona['apellido2']            = n['apellido2']
        persona['sexo']                 = n['sexo']

        persona['bautismo']             = n['bautismo']
        persona['nacimiento']           = n['nacimiento']
        persona['nacimientoEstimado']   = n['nacimientoEstimado']

        persona['padreNombre']          = n['padreNombre']
        persona['madreNombre']          = n['madreNombre']
        persona['padreApellido2']       = n['padreApellido2']
        persona['madreApellido2']       = n['madreApellido2']

        persona['entierro']             = d['entierro']
        persona['defuncion']            = d['defuncion']
        persona['defuncionEstimado']    = d['defuncionEstimado']

        persona['obsNacimiento']        = n['observaciones']
        persona['obsDefuncion']         = d['observaciones']

        persona['oficio']               = d['oficio']

        # THIS IS CALENDAR BASED (NEEDS FIXING)
        persona['edad']                 = int((d['defuncionEstimado'] - n['nacimientoEstimado']).days / 365.25)
        persona['edadTexto']            = d['edadTexto']

        return persona

def mergePeople( nacimientos, defunciones ):

    print ( '\n  ---- Creando personas (matching nacimientos y defuncion) ----')
    people = []
    numM = 0

    for n in nacimientos:
        for d in defunciones:
            if isSamePerson(n, d):
                numM += 1
                #print ('\n%4d> (%s) %s, %s, %s\n      (%s) %s, %s, %s' % \
                #    ( numM, n['nacimientoEstimado'].strftime('%d/%m/%Y'), \
                #            n['nombre'], n['apellido1'], n['apellido2'], \
                #            d['defuncionEstimado'].strftime('%d/%m/%Y'), \
                #            d['nombre'], d['apellido1'], d['apellido2'] ) )
                people.append( mergePerson(n, d, numM) )
                #print('.', end="")
                #sys.stdout.flush()
                #break

    print( 'Numero de matchings: %d' % numM )
    return people

# Analyse/plot data
def printMostCommon( vec, n=float("inf") ):

    #vec2 = vec [ vec != '' ]
    count = Counter(vec)

    print ("\nValores mas comunes")
    for idx in range(min(len(count), n)):
        print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

# Distributions
def showDistribution( vec, stringX, stringY, fig=None, colourIN='0.7' ):

	#minBin = min([v for v in vec if v > 1]) # exclude values with 1 (as they are default for empty ones)
	#maxBin = max(vec)

    minBin = 1605
    maxBin = 1855
    
    binsV = range(minBin, maxBin + 1, 1)
    histV = np.histogram(vec, binsV)
    
    # Plot distribution
    if fig is None:
        fig = plt.figure()
    ax = plt.subplot(111)
    bars = ax.bar( histV[1][:-1], histV[0], alpha=0.6, color=colourIN, align='center', linewidth = '0' )
    
    ticks = [b for b in list(binsV) if b % 10 == 0]
    plt.xticks( ticks )
    
    plt.ylabel( stringY )
    plt.xlabel( stringX )
    
    ax.axis((minBin-1,maxBin+1,0,max(histV[0])*1.05))
    remove2axis( ax )
    
def showDistributionByDecade( vec, stringX, stringY, fig=None, colourIN='0.7' ):

	#minBin = min([v for v in vec if v > 1]) # exclude values with 1 (as they are default for empty ones)
	#maxBin = max(vec)

    minBin = 1600
    maxBin = 1860
    
    binsV = range(minBin, maxBin + 1, 10)
    histV = np.histogram(vec, binsV)
    
    # Plot distribution
    if fig is None:
        fig = plt.figure()
    ax = plt.subplot(111)
    bars = ax.bar( histV[1][:-1], histV[0], width=9, color=colourIN, align='center', linewidth = '0' )
    
    ticks = [b for b in list(binsV) if b % 10 == 0]
    plt.xticks( ticks )
    
    plt.ylabel( stringY )
    plt.xlabel( stringX )
    
    ax.axis((minBin-1,maxBin+1,0,max(histV[0])*1.05))
    remove2axis( ax )
    
    return fig

# Deaths by age
def plotDeathAgeStatistics( merged ):
    # Get death ages
    edad = [p['edad'] for p in merged]
    
    # Print statistical numbers
    edadInfantes = [e for e in edad if e ==  0]
    edadNinos    = [e for e in edad if e <   5]
    edadMenores  = [e for e in edad if e <  12]
    edadMayores  = [e for e in edad if e >= 12]

    mortInfantil = len(edadInfantes) / len(edad) * 100
    mortNinos    = len(edadNinos)    / len(edad) * 100
    mortMenores  = len(edadMenores)  / len(edad) * 100
  
    print( '\n > Esperanza de vida: %.1f' % np.mean(edad))
    print( ' > Esperanza de vida (> 12 años): %.1f' % np.mean(edadMayores))

    print( ' > Mediana de vida: %.1f' % np.median(edad))
    print( ' > Mediana de vida (> 12 años): %.1f' % np.median(edadMayores))

    print( ' > Mortalidad infantil ( <1 años): %.1f%%' % mortInfantil)
    print( ' > Mortalidad Niños    ( <5 años): %.1f%%' % mortNinos)
    print( ' > Mortalidad Menores  (<12 años): %.1f%%' % mortMenores)

    # Get statistical numbers using only reported age at death
    # nAlbados = sum([1 for p in defunciones if p['edadTexto'] == 'Albado'])
    # nAdultos = sum([1 for p in defunciones if p['edadTexto'] == 'Adulto'])

    # mortAlbados = nAlbados / (nAlbados + nAdultos) * 100
    # print( ' > Mortalidad albados (%d of %d): %.1f%%' \
    #         % (nAlbados, nAlbados + nAdultos, mortAlbados) )
    
    binsEdad = range(0, max(edad) + 1, 1)
    histEdad = np.histogram(edad, binsEdad)
    
    # Plot distribution of age at death
    fig = plt.figure()
    ax = plt.subplot(111)
    bars = ax.bar( histEdad[1][:-1], histEdad[0], alpha=0.7, align='center', linewidth = '0' )
    
    plt.ylabel( 'Defunciones' )
    plt.xlabel( 'Edad al momento de defuncion' )
       
    # change the colors according to age
    for i, b in enumerate(bars):
        if i < 1:
            b.set_color(cp[0])
            b.set_label('0 años')
        elif i < 5:
            b.set_color(cp[1])
            b.set_label('1-4 años')
        elif i < 12:
            b.set_color(cp[2])
            b.set_label('5-11 años')
        else:
            b.set_color(cp[3])
            b.set_label('>11 años')
            
    ax.axis((-1,100,0,max(histEdad[0])+25))
    ax.legend( loc= 'best', handles=[bars[12], bars[5], bars[1], bars[0]], frameon=False )
    plt.xticks( [b for b in binsEdad if b % 5 == 0] )
    remove2axis( ax ) 
    
    #py.iplot_mpl(fig)

# Name of the village
def wordInString(stringIN, match):

    stringIN = re.sub('[’:;.,]', ' ', stringIN)
    string_list = stringIN.split()

    match_list = []
    for word in string_list:
        if match in word:
            match_list.append(word)
    return match_list

def getAlmonecirMentions( nacimientos, defunciones ):

    dictNombres = dict()
    lPersona    = []
    lFecha      = []
    lNombre     = []
    lCampo      = []
    lContenido  = []

    for dic in nacimientos+defunciones:
        for key, val in dic.items():
            nombres = wordInString(str(val).lower(), 'almon')
            for n in nombres:
                try:
                    fecha = dic['nacimientoEstimado']
                except:
                    fecha = dic['defuncionEstimado']

                lNombre.append(n)
                lPersona.append(dic)
                lFecha.append(fecha)
                lCampo.append(key)
                lContenido.append(val)

                if n in dictNombres:
                    dictNombres[n]   += 1
                else:
                    dictNombres[n]    = 1

    print ('\n-- Nombres mas comunes del pueblo --\n')

    idNom = 0
    lID = [0] * len(lNombre)
    lNomUnique = []
    # print dict entries sorted from higher to lower freq and assing IDs to names
    for k in sorted(dictNombres, key=dictNombres.get, reverse=True):
        print(' %14s: %d' % (string.capwords(k), dictNombres[k]))
        for i, n in enumerate(lNombre):
                if n == k:
                    lID[i] = idNom
        idNom += 1
        lNomUnique.append(k)

    sc = []
    fig = plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    for idNom in [6,4,2,1,0]:
	#for idNom in range(max(lID)+1):
        xVec = [f.year for i,f in enumerate(lFecha) if lID[i] == idNom ]
        yVec = [idNom] * len(xVec) + np.random.normal(0,0.1,len(xVec))

        strLabel = string.capwords(lNomUnique[idNom]) + " (" + str(dictNombres[lNomUnique[idNom]]) + ")"
        sc.append( ax.scatter(xVec, yVec, marker='.', s=200, alpha=0.5, color=cp2[idNom+1], label=strLabel) )
        
    ax.legend( loc= 'best', handles=sc[:], frameon=False, scatterpoints = 1 )
    ax.axis((1605,1855,-0.5,max(lID)+0.5))
    ticks = [b for b in range(1605,1855) if b % 10 == 0]
    plt.xticks( ticks )
    
    ax.set_yticks( [] )
    ax.spines['left'].set_visible(False)
    
    remove2axis( ax )

# most common names
def commonNames(  dictionary, n=8, splitName=True ):

    allNames = []
    allYears = []

    for d in dictionary:
        #print( '%s | %s' % (d['nombreAjustado'].split(), [d['nombreAjustado']]) )
        if splitName:
            names = d['nombre'].split()
        else:
            names = [d['nombre']]

        try:
            fecha = d['nacimientoEstimado']
        except:
            fecha = d['defuncionEstimado']

        if names:
            allNames.extend( names )
            allYears.extend( [fecha.year] * len(names) )

    count = Counter(allNames)

    n = min(len(count), n)

    # Text output
    print ("Nombres mas comunes (unicos:%d | total:%d)" % (len(count), len(allNames)) )
    # for idx in range(n):
    #     print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

    # Plot output
    sc = []
    fig = plt.figure(figsize=(20, 1+(n/2)))
    ax = plt.subplot(111)

    for idx in range(n):
        name = count.most_common()[idx][0]
        years = [allYears[i] for i,n in enumerate(allNames) if allNames[i] == name \
                                                            and allYears[i] > 1600]
        numName = len(years)
        strLabel = name + " (" + str(numName) + ")"

         

        xVec = years
        yVec = [idx] * len(xVec) + np.random.normal(0,0.1,len(xVec))

        sc.append( ax.scatter(xVec, yVec, \
                    color=cp2[idx%len(cp2)], marker='.', s=100, alpha=0.2, label=strLabel) )

    # ax.legend( loc= 'best', handles=sc[::-1], frameon=False, scatterpoints = 1 )

    xTicks = [b for b in range(1605, max(allYears)+5) if b % 10 == 0]
    plt.xticks( xTicks )

    yTicks = range(n)
    yTicksLabels = [count.most_common()[idx][0] + " (" + str(count.most_common()[idx][1]) + ")" \
                     for idx in range(n)]
    plt.yticks( yTicks, yTicksLabels )

    # ax.set_yticks( [] )
    remove2axis( ax )
    ax.spines['left'].set_visible(False)
    ax.axis((1610,1860,-1,n+1))


    # Plot Histograms
    if False:
        fig = plt.figure(figsize=(20, 8))
        ax = plt.subplot(111)

        minBin = 1625
        maxBin = 1860
        bins = range(minBin, maxBin + 1, 10)

        validYears = [y for y in allYears if y > 1600]
        hAll = np.histogram(validYears, bins)

        np.seterr(divide='ignore', invalid='ignore')    # tolerate division by 0

        h = []
        ratio = []
        for idx in range(n):
            name = count.most_common()[idx][0]
            years = [allYears[i] for i,n in enumerate(allNames) if allNames[i] == name and allYears[i] > 1610]
            numName = len(years)
            strLabel = name + " (" + str(numName) + ")"
        
            h.append( np.histogram(years, bins) )
            ratio.append( h[-1][0] / hAll[0] * 100 )

            ax.plot( hAll[1][:-1], ratio[-1],  color=cp2[idx%len(cp2)], \
                        linewidth = '4', label=name)

        ax.legend( loc= 'best', frameon=False )

        ticks = [b for b in range(minBin-1, maxBin+1) if b % 10 == 0]
        plt.xticks( ticks )
        remove2axis( ax )

        # Plot individual histograms
        fig, ax = plt.subplots(n, sharex=True, sharey=True, figsize=(20, n*3))

        for idx in range(n):
            ax[idx].plot( bins[:-1], ratio[idx],  color=cp2[idx%len(cp2)], \
                        linewidth = '4')
            remove2axis( ax[idx] )
            ax[idx].legend( [yTicksLabels[idx]], loc= 'best', frameon=False )


        plt.xticks( ticks )

        ax[0].set_title('Sharing both axes')
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        fig.subplots_adjust(hspace=0.1)
        plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)





# Events by year
def plotEventByYear ( merged, str_event, str_ylabel ):

    edad         = [p['edad'] for p in merged]
    
    # Evolution of mortalidad infantil
    hEntierros   = np.zeros(200)
    hEntierros1  = np.zeros(200)
    hEntierros5  = np.zeros(200)
    hEntierros12 = np.zeros(200)
    hEntierrosAd = np.zeros(200)

    mortality1   = np.full(200, np.nan)
    mortality5   = np.full(200, np.nan)
    mortality12  = np.full(200, np.nan)
    mortalityAd  = np.full(200, np.nan)

    # get year of all deaths
    anyoEnt = [p[str_event].year for p in merged]

    # build histograms with number of death in each 10-year period
    for i, anyo in enumerate(anyoEnt):
        hEntierros[anyo // 10] += 1
        if edad[i] < 1:
            hEntierros1[anyo // 10] += 1
        elif edad[i] < 5:
            hEntierros5[anyo // 10] += 1
        elif edad[i] < 12:
            hEntierros12[anyo // 10] += 1
        else:
            hEntierrosAd[anyo // 10] += 1

    mask = [hEntierros != 0] # bins with data

    # find first and last bin (for plotting)
    min_bin = next(i for i, v in enumerate(hEntierros) if v > 0)
    max_bin_tmp = next(i for i, v in enumerate(reversed(hEntierros)) if v > 0)
    max_bin = len(hEntierros) - 1 - max_bin_tmp
    #min_bin = 168
    #max_bin = 185
    range_bin = np.arange(min_bin, max_bin+1)
    
    # print( "\nPorcentaje de entierros de niños (<1 año): ")
    # for i, v in enumerate(hEntierros):
    #     if v > 0:
    #         print ( "%d - %d: %3.1f (%3d/%3d)" % (i*10, (i+1)*10, mortality1[i], hEntierros1[i], hEntierros[i]) )

    # print( "\nPorcentaje de entierros de niños (<5 año): ")
    # for i, v in enumerate(hEntierros):
    #     if v > 0:
    #         print ( "%d - %d: %3.1f (%3d/%3d)" % (i*10, (i+1)*10, mortality5[i], hEntierros5[i], hEntierros[i]) )

    # print( "\nPorcentaje de entierros de niños (<12 año): ")
    # for i, v in enumerate(hEntierros):
    #     if v > 0:
    #         print ( "%d - %d: %3.1f (%3d/%3d)" % (i*10, (i+1)*10, mortality12[i], hEntierros12[i], hEntierros[i]) )

    # Plot it absolute
    fig = plt.figure()
    ax = plt.subplot(111)
    b1 = ax.bar( range_bin, hEntierros[min_bin:max_bin+1],  color='0.9', label='Total', align='center', edgecolor = 'none' )
    l1, = ax.plot( range_bin, hEntierros1[min_bin:max_bin+1],  color=cp[0], marker='.', markersize ='14', linewidth='3', label='0 años' )
    l2, = ax.plot( range_bin, hEntierros5[min_bin:max_bin+1],  color=cp[1], marker='.', markersize ='14', linewidth='3', label='1-4 años' )
    l3, = ax.plot( range_bin, hEntierros12[min_bin:max_bin+1], color=cp[2], marker='.', markersize ='14', linewidth='3', label='5-11 años' )
    l4, = ax.plot( range_bin, hEntierrosAd[min_bin:max_bin+1], color=cp[3], marker='.', markersize ='14', linewidth='3', label='>11 años' )
    ax.axis((min_bin-0.5,max_bin+4,0,max(hEntierros)+10))    # Tweak spacing to prevent clipping of tick-labels
    ax.legend( loc= 'best', handles=[b1, l4, l3, l2, l1], frameon=False )
    plt.xticks( range_bin, range_bin*10 )
    plt.ylabel( str_ylabel )
    plt.xlabel( 'Decada' )
    remove2axis( ax )
    
    mask = [hEntierros != 0] # bins with data
    
    
    ratio1   = np.full(200, np.nan)
    ratio5   = np.full(200, np.nan)
    ratio12  = np.full(200, np.nan)
    ratioAd  = np.full(200, np.nan)
    
    ratio1[mask] = hEntierros1[mask] / hEntierros[mask] * 100
    ratio5[mask] = hEntierros5[mask] / hEntierros[mask] * 100
    ratio12[mask] = hEntierros12[mask] / hEntierros[mask] * 100
    ratioAd[mask] = hEntierrosAd[mask] / hEntierros[mask] * 100
    
    fig = plt.figure()
    ax = plt.subplot(111)
    #b1 = ax.bar( range_bin, hEntierros[min_bin:max_bin+1],  color='0.9', label='Total', align='center', edgecolor = 'none' )
    b1 = ax.bar( range_bin, ratio1[min_bin:max_bin+1],  color=cp[0], alpha=0.6, label='0 años'    , align='center', linewidth=0 )
    b2 = ax.bar( range_bin, ratio5[min_bin:max_bin+1],  color=cp[1], alpha=0.6, label='1-4 años'  , align='center', linewidth=0, \
                            bottom=ratio1[min_bin:max_bin+1])
    b3 = ax.bar( range_bin, ratio12[min_bin:max_bin+1], color=cp[2], alpha=0.6, label='5-11 años', align='center', linewidth=0, \
                            bottom=ratio1[min_bin:max_bin+1]+ratio5[min_bin:max_bin+1] )
    b4 = ax.bar( range_bin, ratioAd[min_bin:max_bin+1], color=cp[3], alpha=0.6, label='>11 años' , align='center', linewidth=0, \
                            bottom=ratio1[min_bin:max_bin+1]+ratio5[min_bin:max_bin+1]+ratio12[min_bin:max_bin+1] )
    ax.axis((min_bin-0.5,max_bin+4,0,100))    # Tweak spacing to prevent clipping of tick-labels
    ax.legend( loc= 'best', handles=[b4, b3, b2, b1], frameon=False )
    
    plt.xticks( range_bin, range_bin*10 )
    plt.ylabel( str_ylabel + ' (% del total)' )
    plt.xlabel( 'Decada' )
    remove2axis( ax )

# Events by Month
def plotEventByMonth ( merged, str_event, str_ylabel ):

    # Get death ages
    edad = [p['edad'] for p in merged]
    mes  = [p[str_event].month for p in merged]

    str_months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'Agoust', 'September', 'October', 'November', 'December']

    porMes          = np.zeros(12)
    porMes1         = np.zeros(12)
    porMes5         = np.zeros(12)
    porMes12        = np.zeros(12)
    porMesAdultos   = np.zeros(12)

    # put entries in bin for each occurance
    for i, e in enumerate(edad):
        porMes[mes[i]-1] += 1
        if e < 1:
            porMes1[mes[i]-1] += 1
        elif e < 5:
            porMes5[mes[i]-1] += 1
        elif e < 12:
            porMes12[mes[i]-1] += 1
        else:
            porMesAdultos[mes[i]-1] += 1

    fig = plt.figure()
    ax = plt.subplot(111)
    b1 = ax.bar( range(12), porMes,  color='0.9', label='Total', align='center', edgecolor = 'none' )
    l1, = ax.plot( range(12), porMes1,       color=cp[0], linewidth='3', marker='.', markersize ='14', label='0 años' )
    l2, = ax.plot( range(12), porMes5,       color=cp[1], linewidth='3', marker='.', markersize ='14', label='1-4 años' )
    l3, = ax.plot( range(12), porMes12,      color=cp[2], linewidth='3', marker='.', markersize ='14', label='5-11 años' )
    l4, = ax.plot( range(12), porMesAdultos, color=cp[3], linewidth='3', marker='.', markersize ='14', label='>11 años' )
    ax.legend( loc= 'best', handles=[b1, l4, l3, l2, l1], frameon=False )
    ax.set_xticks( range(12) )
    ax.set_xticklabels( [v[0:1] for v in str_months] )
    ax.axis((-0.5,13.5,0,max(porMes)+10))
    ax.set_ylabel( str_ylabel )
    plt.xlabel( 'Mes' )
    remove2axis( ax )
    
    ratioPorMes1        = porMes1  / porMes  * 100
    ratioPorMes5        = porMes5  / porMes  * 100
    ratioPorMes12       = porMes12 / porMes * 100
    ratioPorMesAdultos  = porMesAdultos / porMes * 100
    
    fig = plt.figure()
    ax = plt.subplot(111)
    #b1 = ax.bar( range_bin, hEntierros[min_bin:max_bin+1],  color='0.9', label='Total', align='center', edgecolor = 'none' )
    b1 = ax.bar( range(12), ratioPorMes1, color=cp[0], alpha = 0.6, align='center', linewidth=0, label='0 años')
    b2 = ax.bar( range(12), ratioPorMes5, color=cp[1], alpha = 0.6, align='center', linewidth=0, label='1-4 años', \
                            bottom=ratioPorMes1)
    b3 = ax.bar( range(12), ratioPorMes12, color=cp[2], alpha = 0.6, align='center', linewidth=0, label='5-11 años', \
                            bottom=ratioPorMes1+ratioPorMes5 )
    b4 = ax.bar( range(12), ratioPorMesAdultos, color=cp[3], alpha = 0.6, align='center', linewidth=0, label='>11 años', \
                            bottom=ratioPorMes1+ratioPorMes5+ratioPorMes12 )
	# ax.axis((min_bin-0.5,max_bin+0.5,0,100))    # Tweak spacing to prevent clipping of tick-labels
    ax.legend( loc= 'best', handles=[b4, b3, b2, b1], frameon=False )
    ax.set_xticks( range(12) )
    ax.set_xticklabels( [v[0] for v in str_months] )
    ax.axis((-0.5,13.5,0,100))
    plt.ylabel( str_ylabel + ' (% del total)' )
    plt.xlabel( 'Mes' )
    remove2axis( ax )

# Child mortality (using text data)
def childMotality( nacimientos, defunciones ):

	#minBin = min([v for v in vec if v > 1]) # exclude values with 1 (as they are default for empty ones)
	#maxBin = max(vec)

    childDeaths = [d for d in defunciones if str(d['edadTexto']).upper() \
                   in ['P', 'A', 'ALB', 'N', 'NIÑA', 'ŃIÑO']]

    minBin = 1600
    maxBin = 1860
    
    bins = range(minBin, maxBin + 1, 10)
    hDeaths = np.histogram([p['defuncionEstimado'].year for p in childDeaths], bins)
    hBirths = np.histogram([p['nacimientoEstimado'].year for p in nacimientos], bins)

    ratio = hDeaths[0] / hBirths[0] * 100

    # print( ratio )
    
    # Plot distribution
    fig = plt.figure()
    ax = plt.subplot(111)
            
    bBirths = ax.bar( hBirths[1][:-1], hBirths[0], width=9, color='0.85', \
                        align='center', linewidth = '0', label='Births')
    bDeaths = ax.bar( hDeaths[1][:-1], hDeaths[0], width=7, color=cp2[7], \
                        align='center', linewidth = '0', alpha=0.7, label='Children deaths')
    ticks = [b for b in list(bins) if b % 10 == 0]
    plt.xticks( ticks )
    
    plt.ylabel( '#' )
    plt.xlabel( 'Decade' )

    ax.legend( loc= 'best', handles=[bBirths, bDeaths], frameon=False )
    
    ax.axis((minBin+1,maxBin-1,0,max(hBirths[0])*1.05))
    remove2axis( ax )

    # Plot ratio
    fig = plt.figure()
    ax = plt.subplot(111)
            
    pRatio = ax.plot( bins[:-1], ratio,  color='0.5', linewidth = '4', label='Child mortality ratio')
    plt.xticks( ticks )
    
    plt.ylabel( '% of children funerals (over total)' )
    plt.xlabel( 'Decade' )

    ax.legend( loc= 'best', handles=pRatio, frameon=False )
    
    #ax.axis((minBin+1,maxBin-1,0,100))
    remove2axis( ax )    