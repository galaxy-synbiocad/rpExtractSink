import csv
import os
import pickle
import gzip
from rdkit.Chem import MolFromSmiles, MolFromInchi, MolToSmiles, MolToInchi, MolToInchiKey, AddHs
import sys
import urllib.request
#from .setup_self.logger import self.logger
import logging
import io
import re
import libsbml
#import tarfile

import rpSBML


## @package rpReader
#
# Collection of functions that convert the outputs from various sources to the SBML format (rpSBML) for further analyses


## Error function for the convertion of structures
#
class Error(Exception):
    pass


## Error function for the convertion of structures
#
class DepictionError(Error):
    def __init__(self, message):
        #self.expression = expression
        self.message = message


#######################################################
################### rpCache  ##########################
#######################################################

## Class to generate the cache
#
# Contains all the functions that parse different files, used to calculate the thermodynamics and the FBA of the
#the other steps. These should be called only when the files have changes
class rpCache:
    ## Cache constructor
    #
    # @param self The object pointer
    # @param inputPath The path to the folder that contains all the input/output files required
    def __init__(self):
        #given by Thomas
        self.logger = logging.getLogger(__name__)
        self.logger.info('Started instance of rpCache')
        self.convertMNXM = {'MNXM162231': 'MNXM6',
                'MNXM84': 'MNXM15',
                'MNXM96410': 'MNXM14',
                'MNXM114062': 'MNXM3',
                'MNXM145523': 'MNXM57',
                'MNXM57425': 'MNXM9',
                'MNXM137': 'MNXM588022'}
        self.deprecatedMNXM_mnxm = {}


    #######################################################
    ################### PRIVATE FUNCTION ##################
    #######################################################


    ## Convert chemical depiction to others type of depictions
    #
    # Usage example:
    # - convert_depiction(idepic='CCO', otype={'inchi', 'smiles', 'inchikey'})
    # - convert_depiction(idepic='InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3', itype='inchi', otype={'inchi', 'smiles', 'inchikey'})
    #  @param self The object pointer
    #  @param idepic String depiction to be converted, str
    #  @param itype type of depiction provided as input, str
    #  @param otype types of depiction to be generated, {"", "", ..}
    #  @return odepic generated depictions, {"otype1": "odepic1", ..}
    def _convert_depiction(self, idepic, itype='smiles', otype={'inchikey'}):
        # Import (if needed)
        if itype == 'smiles':
            rdmol = MolFromSmiles(idepic, sanitize=True)
        elif itype == 'inchi':
            rdmol = MolFromInchi(idepic, sanitize=True)
        else:
            raise NotImplementedError('"{}" is not a valid input type'.format(itype))
        if rdmol is None:  # Check imprt
            raise DepictionError('Import error from depiction "{}" of type "{}"'.format(idepic, itype))
        # Export
        odepic = dict()
        for item in otype:
            if item == 'smiles':
                odepic[item] = MolToSmiles(rdmol)  # MolToSmiles is tricky, one mays want to check the possible options..
            elif item == 'inchi':
                odepic[item] = MolToInchi(rdmol)
            elif item == 'inchikey':
                odepic[item] = MolToInchiKey(rdmol)
            else:
                raise NotImplementedError('"{}" is not a valid output type'.format(otype))
        return odepic


    #######################################################
    #######################################################
    #######################################################


    ## Function to create a dictionnary of old to new chemical id's
    #
    #  Generate a one-to-one dictionnary of old id's to new ones. Private function
    #
    # TODO: check other things about the mnxm emtry like if it has the right structure etc...
    def _checkMNXMdeprecated(self, mnxm):
        try:
            return self.deprecatedMNXM_mnxm[mnxm]
        except KeyError:
            return mnxm


    #[TODO] merge the two functions
    ## Function to parse the chem_xref.tsv file of MetanetX
    #
    #  Generate a dictionnary of old to new MetanetX identifiers to make sure that we always use the freshest id's.
    # This can include more than one old id per new one and thus returns a dictionnary. Private function
    #
    #  @param self Object pointer
    #  @param chem_xref_path Input file path
    #  @return Dictionnary of identifiers
    #TODO: save the self.deprecatedMNXM_mnxm to be used in case there rp_paths uses an old version of MNX
    def deprecatedMNXM(self, chem_xref_path):
        self.deprecatedMNXM_mnxm = {}
        with open(chem_xref_path) as f:
            c = csv.reader(f, delimiter='\t')
            for row in c:
                if not row[0][0]=='#':
                    mnx = row[0].split(':')
                    if mnx[0]=='deprecated':
                        self.deprecatedMNXM_mnxm[mnx[1]] = row[1]
            self.deprecatedMNXM_mnxm.update(self.convertMNXM)
            self.deprecatedMNXM_mnxm['MNXM01'] = 'MNXM1'


    ## Function to parse the chemp_prop.tsv file from MetanetX and compounds.tsv from RetroRules. Uses the InchIkey as key to the dictionnary
    #
    #  Generate a dictionnary gaving the formula, smiles, inchi and inchikey for the components
    #
    #  @param self Object pointer
    #  @param chem_prop_path Input file path
    #  @return mnxm_strc Dictionnary of formula, smiles, inchi and inchikey
    def mnx_strc(self, rr_compounds_path, chem_prop_path):
        mnxm_strc = {}
        for row in csv.DictReader(open(rr_compounds_path), delimiter='\t'):
            tmp = {'forumla':  None,
                    'smiles': None,
                    'inchi': row['inchi'],
                    'inchikey': None,
                    'mnxm': self._checkMNXMdeprecated(row['cid']),
                    'name': None}
            try:
                resConv = self._convert_depiction(idepic=tmp['inchi'], itype='inchi', otype={'smiles','inchikey'})
                for i in resConv:
                    tmp[i] = resConv[i]
            except DepictionError as e:
                self.logger.warning('Could not convert some of the structures: '+str(tmp))
                self.logger.warning(e)
            mnxm_strc[tmp['mnxm']] = tmp
        with open(chem_prop_path) as f:
            c = csv.reader(f, delimiter='\t')
            for row in c:
                if not row[0][0]=='#':
                    mnxm = self._checkMNXMdeprecated(row[0])
                    tmp = {'forumla':  row[2],
                            'smiles': row[6],
                            'inchi': row[5],
                            'inchikey': row[8],
                            'mnxm': mnxm,
                            'name': row[1]}
                    for i in tmp:
                        if tmp[i]=='' or tmp[i]=='NA':
                            tmp[i] = None
                    if mnxm in mnxm_strc:
                        mnxm_strc[mnxm]['forumla'] = row[2]
                        mnxm_strc[mnxm]['name'] = row[1]
                        if not mnxm_strc[mnxm]['smiles'] and tmp['smiles']:
                            mnxm_strc[mnxm]['smiles'] = tmp['smiles']
                        if not mnxm_strc[mnxm]['inchikey'] and tmp['inchikey']:
                            mnxm_strc[mnxm]['inchikey'] = tmp['inchikey']
                    else:
                        #check to see if the inchikey is valid or not
                        otype = set({})
                        if not tmp['inchikey']:
                            otype.add('inchikey')
                        if not tmp['smiles']:
                            otype.add('smiles')
                        if not tmp['inchi']:
                            otype.add('inchi')
                        itype = ''
                        if tmp['inchi']:
                            itype = 'inchi'
                        elif tmp['smiles']:
                            itype = 'smiles'
                        else:
                            self.logger.warning('No valid entry for the convert_depiction function')
                            continue
                        try:
                            resConv = self._convert_depiction(idepic=tmp[itype], itype=itype, otype=otype)
                            for i in resConv:
                                tmp[i] = resConv[i]
                        except DepictionError as e:
                            self.logger.warning('Could not convert some of the structures: '+str(tmp))
                            self.logger.warning(e)
                        mnxm_strc[tmp['mnxm']] = tmp
            #inchikey_mnam
            inchikey_mnxm = {}
            for mnxm in mnxm_strc:
                if not mnxm_strc[mnxm]['inchikey'] in inchikey_mnxm:
                    inchikey_mnxm[mnxm_strc[mnxm]['inchikey']] = []
                inchikey_mnxm[mnxm_strc[mnxm]['inchikey']].append(mnxm)
        return mnxm_strc, inchikey_mnxm



#WARNING: if you define inputPath, then all the files must have specific names to
#make sure that it can find the appropriate files


## Class to read all the input files
#
# Contains all the functions that read the cache files and input files to reconstruct the heterologous pathways
class rpExtractSink:
    ## InputReader constructor
    #
    #  @param self The object pointer
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Starting instance of rpReader')
        self.mnxm_strc = None #There are the structures from MNXM
        if not self._loadCache():
            raise ValueError


    #######################################################################
    ############################# PRIVATE FUNCTIONS #######################
    #######################################################################


    ## Private function to fetch the required data, parse them and generate the pickle
    #
    #  Opens the previously generated cache to the object memory
    #
    # @param The oject pointer
    # @return Boolean detemining the success of the function or not
    def _loadCache(self, fetchInputFiles=False):
        dirname = os.path.dirname(os.path.abspath( __file__ ))
        #################### make the local folders ############################
        # input_cache
        if not os.path.isdir(dirname+'/input_cache'):
            os.mkdir(dirname+'/input_cache')
        # cache
        if not os.path.isdir(dirname+'/cache'):
            os.mkdir(dirname+'/cache')
        #################### make the local folders ############################
        # rr_compounds.tsv
        #TODO: need to add this file to the git or another location
        if not os.path.isfile(dirname+'/input_cache/rr_compounds.tsv') or fetchInputFiles:
            urllib.request.urlretrieve(
                    'TODO', 
                    dirname+'/input_cache/rr_compounds.tsv')
            '''
            tf = tarfile.open(dirname+'/input_cache/retrorules_preparsed.tar.xz')
            tf.extractall(path=dirname+'/input_cache/')
            tf.close()
            '''
        # chem_prop.tsv
        if not os.path.isfile(dirname+'/input_cache/chem_prop.tsv') or fetchInputFiles:
            urllib.request.urlretrieve('https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_prop.tsv', 
                    dirname+'/input_cache/chem_prop.tsv')
        ###################### Populate the cache #################################
        rpcache = rpCache()
        if not os.path.isfile(dirname+'/cache/mnxm_strc.pickle.gz'):
            mnxm_strc, inchikey_mnxm = rpcache.mnx_strc(dirname+'/input_cache/rr_compounds.tsv',
                                                        dirname+'/input_cache/chem_prop.tsv')
            pickle.dump(mnxm_strc, gzip.open(dirname+'/cache/mnxm_strc.pickle.gz','wb'))
        self.mnxm_strc = pickle.load(gzip.open(dirname+'/cache/mnxm_strc.pickle.gz', 'rb'))
        rpcache = None
        return True



    #TODO: move this to another place

    ## Generate the sink from a given model and the
    #
    # NOTE: this only works for MNX models, since we are parsing the id
    # TODO: change this to read the annotations and extract the MNX id's
    #
    def genSink(self, input_sbml, compartment_id='MNXC3'):
        rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromFile(input_sbml))
        #rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromString(sbml_string))
        #rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromString(sbml_bytes.decode('utf-8')))
        file_out = io.StringIO()
        #file_out = io.BytesIO()
        ### open the cache ###
        cytoplasm_species = []
        for i in rpsbml.model.getListOfSpecies():
            if i.getCompartment()==compartment_id:
                cytoplasm_species.append(i)
        count = 0
        #with open(file_out, mode='wb') as f:
        #writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer = csv.writer(file_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['Name','InChI'])
        for i in cytoplasm_species:
            res = rpsbml.readMIRIAMAnnotation(i.getAnnotation())
            #extract the MNX id's
            try:
                mnx = res['metanetx'][0]
            except KeyError:
                continue
            #mnx = i.getId().split('__')[0]
            try:
                inchi = self.mnxm_strc[mnx]['inchi']
            except KeyError:
                inchi = None
            if mnx and inchi:
                writer.writerow([mnx,inchi])
                count += 1
        file_out.seek(0)
        #out = file_out.read()
        if count==0:
            return ''
        else:
            return file_out


if __name__== "__main__":
    rpExtractSink()
