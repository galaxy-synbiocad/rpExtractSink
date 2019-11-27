import csv
import os
import pickle
import gzip
from rdkit.Chem import MolFromSmiles, MolFromInchi, MolToSmiles, MolToInchi, MolToInchiKey, AddHs
import sys
import logging
import io
import re
import libsbml

import rpSBML

## Class to read all the input files
#
# Contains all the functions that read the cache files and input files to reconstruct the heterologous pathways
class rpGenSink:
    ## InputReader constructor
    #
    #  @param self The object pointer
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Starting instance of rpGenSink')
        self.mnxm_strc = None #There are the structures from MNXM


    #######################################################################
    ############################# PRIVATE FUNCTIONS #######################
    #######################################################################



    #TODO: move this to another place

    ## Generate the sink from a given model and the
    #
    # NOTE: this only works for MNX models, since we are parsing the id
    # TODO: change this to read the annotations and extract the MNX id's
    #
    def genSink(self, input_sbml, compartment_id='MNXC3'):
        print("toc 2")
        rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromFile(input_sbml))
        #rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromString(sbml_string))
        #rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromString(sbml_bytes.decode('utf-8')))
        print("toc 2")
        file_out = io.StringIO()
        #file_out = io.BytesIO()
        ### open the cache ###
        print("toc 2")
        cytoplasm_species = []
        print("toc 2")
        for i in rpsbml.model.getListOfSpecies():
            if i.getCompartment()==compartment_id:
                cytoplasm_species.append(i)
        print("toc 2")
        count = 0
        #with open(file_out, mode='wb') as f:
        #writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        print("toc 2")
        writer = csv.writer(file_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        print("toc 2")
        writer.writerow(['Name','InChI'])
        print("toc 2")
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
        print("toc 2")
        file_out.seek(0)
        #out = file_out.read()
        print("toc 2")
        if count==0:
            return ''
        else:
            return file_out
