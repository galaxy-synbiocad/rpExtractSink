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
import cobra
import tempfile

import rpSBML

## Class to read all the input files
#
# Contains all the functions that read the cache files and input files to reconstruct the heterologous pathways
class rpExtractSink:
    ## InputReader constructor
    #
    #  @param self The object pointer
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Starting instance of rpExtractSink')
        self.mnxm_strc = None #There are the structures from MNXM
        self.rpsbml = None
        self.cobraModel = None


    #######################################################################
    ############################# PRIVATE FUNCTIONS #######################
    #######################################################################


    ## Pass the libSBML file to Cobra
    #
    #
    def _convertToCobra(self):
        try:
            #self.cobraModel = cobra.io.read_sbml_model(self.rpsbml.document.toXMLNode().toXMLString(),
            #        use_fbc_package=True)
            self.cobraModel = cobra.io.read_sbml_model(self.rpsbml.document.toXMLNode().toXMLString())
            #use CPLEX
            # self.cobraModel.solver = 'cplex'
        except cobra.io.sbml.CobraSBMLError as e:
            self.logger.error(e)
            self.logger.error('Cannot convert the libSBML model to Cobra')


    ## Taken from Thomas Duigou's code
    #
    # @param input Cobra model object
    #
    def _reduce_model(self):
        """
        Reduce the model by removing reaction that cannot carry any flux and orphan metabolites

        :param model: cobra model object
        :return: reduced cobra model object
        """
        lof_zero_flux_rxn = cobra.flux_analysis.find_blocked_reactions(self.cobraModel, open_exchanges=True)
        #logging.info('Reducing model > {} reactions to be removed'.format(len(lof_zero_flux_rxn)))
        # For assert and logging: Backup the list of metabolites and reactions
        nb_metabolite_model_ids = set([m.id for m in model.metabolites])
        nb_reaction_model_ids = set([m.id for m in model.reactions])
        #logging.info('Reducing model > {} metabolites before reduction'.format(len(nb_metabolite_model_ids)))
        #logging.info('Reducing model > {} reactions before reduction'.format(len(nb_reaction_model_ids)))
        # Remove unwanted reactions and metabolites
        self.cobraModel.remove_reactions(lof_zero_flux_rxn, remove_orphans=True)
        # Assert the number are expected numbers
        assert len(set([m.id for m in self.cobraModel.reactions])) == len(nb_reaction_model_ids) - len(lof_zero_flux_rxn)
        # Logs
        #logging.info('Reducing model > {} metabolites after reduction'.format(len(set([m.id for m in model.metabolites]))))
        #logging.info('Reducing model > {} reactions after reduction'.format(len(set([m.id for m in model.reactions]))))
        #return model 

    def _removeDeadEnd(self):
        self._convertToCobra()
        #self.cobraModel = self._reduce_model(self.cobraModel)
        self._reduce_model()
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            cobra.io.write_sbml_model(self.cobraModel, tmpOutputFolder+'/tmp.xml.sbml', use_fbc_package=True)
            self.rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromFile(tmpOutputFolder+'/tmp.xml.sbml'))

    #######################################################################
    ############################# PUBLIC FUNCTIONS ########################
    #######################################################################


    ## Generate the sink from a given model and the
    #
    # NOTE: this only works for MNX models, since we are parsing the id
    # TODO: change this to read the annotations and extract the MNX id's
    #
    def genSink(self, input_sbml, remove_dead_end=False, compartment_id='MNXC3'):
        sbml_data = input_sbml.read().decode("utf-8")
        self.rpsbml = rpSBML.rpSBML('inputModel', libsbml.readSBMLFromString(sbml_data))
        if remove_dead_end:
            self._removeDeadEnd()
        file_out = io.StringIO()
        ### open the cache ###
        cytoplasm_species = []
        for i in self.rpsbml.model.getListOfSpecies():
            if i.getCompartment()==compartment_id:
                cytoplasm_species.append(i)
        count = 0
        writer = csv.writer(file_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['Name','InChI'])
        for i in cytoplasm_species:
            res = self.rpsbml.readMIRIAMAnnotation(i.getAnnotation())
            #extract the MNX id's
            try:
                mnx = res['metanetx'][0]
            except KeyError:
                continue
            try:
                inchi = self.mnxm_strc[mnx]['inchi']
            except KeyError:
                inchi = None
            if mnx and inchi:
                writer.writerow([mnx,inchi])
                count += 1
        file_out.seek(0)
        if count==0:
            return ''
        else:
            return file_out

    

