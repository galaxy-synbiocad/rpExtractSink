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
        self.cid_strc = None #There are the structures from MNXM
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
            with tempfile.TemporaryDirectory() as tmpOutputFolder:
                self.rpsbml.writeSBML(tmpOutputFolder)
                self.cobraModel = cobra.io.read_sbml_model(glob.glob(tmpOutputFolder+'/*')[0], use_fbc_package=True)
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
        # For assert and logging: Backup the list of metabolites and reactions
        nb_metabolite_model_ids = set([m.id for m in self.cobraModel.metabolites])
        nb_reaction_model_ids = set([m.id for m in self.cobraModel.reactions])
        # Remove unwanted reactions and metabolites
        self.cobraModel.remove_reactions(lof_zero_flux_rxn, remove_orphans=True)
        # Assert the number are expected numbers
        assert len(set([m.id for m in self.cobraModel.reactions])) == len(nb_reaction_model_ids) - len(lof_zero_flux_rxn)


    ##
    #
    #
    def _removeDeadEnd(self, sbml_path):
        self.cobraModel = cobra.io.read_sbml_model(sbml_path, use_fbc_package=True)
        self._reduce_model()
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            cobra.io.write_sbml_model(self.cobraModel, tmpOutputFolder+'/tmp.xml')
            self.rpsbml = rpSBML.rpSBML('tmp')
            self.rpsbml.readSBML(tmpOutputFolder+'/tmp.xml')


    #######################################################################
    ############################# PUBLIC FUNCTIONS ########################
    #######################################################################


    ## Generate the sink from a given model and the
    #
    # NOTE: this only works for MNX models, since we are parsing the id
    # TODO: change this to read the annotations and extract the MNX id's
    #
    def genSink(self, input_sbml, output_sink, remove_dead_end=False, compartment_id='MNXC3'):
        if remove_dead_end:
            self._removeDeadEnd(input_sbml)
        else:
            self.rpsbml = rpSBML.rpSBML('tmp')
            self.rpsbml.readSBML(input_sbml)
            '''
            try:
                self._removeDeadEnd()
            except OSError as e:
                logging.warning(e)
                logging.warning('Could not use FVA on this model')
                self.rpsbml = rpSBML.rpSBML('tmp')
                self.rpsbml.readSBML(input_sbml)
            '''
        ### open the cache ###
        cytoplasm_species = []
        for i in self.rpsbml.model.getListOfSpecies():
            if i.getCompartment()==compartment_id:
                cytoplasm_species.append(i)
        if not cytoplasm_species:
            logging.error('Could not retreive any species in the compartment: '+str(compartment_id))
            logging.error('Is the right compartment set?')
            return False
        with open(output_sink, 'w') as outS:
            writer = csv.writer(outS, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['Name','InChI'])
            for i in cytoplasm_species:
                res = self.rpsbml.readMIRIAMAnnotation(i.getAnnotation())
                #extract the MNX id's
                try:
                    mnx = res['metanetx'][0]
                except KeyError:
                    logging.warning('Cannot find MetaNetX ID for '+str(i.getId()))
                    continue
                try:
                    inchi = self.cid_strc[mnx]['inchi']
                except KeyError:
                    inchi = None
                if inchi:
                    writer.writerow([mnx,inchi])
