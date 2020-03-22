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


###################################################################################
###################################################################################
###################################################################################

import signal
import inspect
import traceback
from functools import wraps
from multiprocessing import Process, Queue

'''
This is to deal with an error caused by Cobrapy segmentation fault
'''
def handler(signum, frame):
    raise OSError('CobraPy is throwing a segmentation fault')

class Sentinel:
    pass

def processify(func):
    '''Decorator to run a function as a process.
    Be sure that every argument and the return value
    is *pickable*.
    The created process is joined, so the code does not
    run in parallel.
    '''

    def process_generator_func(q, *args, **kwargs):
        result = None
        error = None
        it = iter(func())
        while error is None and result != Sentinel:
            try:
                result = next(it)
                error = None
            except StopIteration:
                result = Sentinel
                error = None
            except Exception:
                ex_type, ex_value, tb = sys.exc_info()
                error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
                result = None
            q.put((result, error))

    def process_func(q, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
            result = None
        else:
            error = None

        q.put((result, error))

    def wrap_func(*args, **kwargs):
        # register original function with different name
        # in sys.modules so it is pickable
        process_func.__name__ = func.__name__ + 'processify_func'
        setattr(sys.modules[__name__], process_func.__name__, process_func)

        signal.signal(signal.SIGCHLD, handler) #This is to catch the segmentation error 

        q = Queue()
        p = Process(target=process_func, args=[q] + list(args), kwargs=kwargs)
        p.start()
        result, error = q.get()
        p.join()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (str(ex_value), tb_str)
            raise ex_type(message)

        return result

    def wrap_generator_func(*args, **kwargs):
        # register original function with different name
        # in sys.modules so it is pickable
        process_generator_func.__name__ = func.__name__ + 'processify_generator_func'
        setattr(sys.modules[__name__], process_generator_func.__name__, process_generator_func)

        signal.signal(signal.SIGCHLD, handler) #This is to catch the segmentation error

        q = Queue()
        p = Process(target=process_generator_func, args=[q] + list(args), kwargs=kwargs)
        p.start()

        result = None
        error = None
        while error is None:
            result, error = q.get()
            if result == Sentinel:
                break
            yield result
        p.join()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (str(ex_value), tb_str)
            raise ex_type(message)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if inspect.isgeneratorfunction(func):
            return wrap_generator_func(*args, **kwargs)
        else:
            return wrap_func(*args, **kwargs)
    return wrapper






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
            self.cobraModel = cobra.io.read_sbml_model(self.rpsbml.document.toXMLNode().toXMLString(),
                    use_fbc_package=True)
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
    @processify
    def _removeDeadEnd(self):
        self._convertToCobra()
        self._reduce_model()
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            cobra.io.write_sbml_model(self.cobraModel, tmpOutputFolder+'/tmp.xml')
            self.rpsbml = rpSBML.rpSBML('inputModel')
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
        self.rpsbml = rpSBML.rpSBML('tmp')
        self.rpsbml.readSBML(input_sbml)
        if remove_dead_end:
            '''
            self._removeDeadEnd()
            '''
            try:
                self._removeDeadEnd()
            except OSError as e:
                logging.warning(e)
                logging.warning('Could not use FVA on this model')
                self.rpsbml = rpSBML.rpSBML('tmp')
                self.rpsbml.readSBML(input_sbml)
        ### open the cache ###
        cytoplasm_species = []
        for i in self.rpsbml.model.getListOfSpecies():
            if i.getCompartment()==compartment_id:
                cytoplasm_species.append(i)
        with open(output_sink, 'w') as outS:
            writer = csv.writer(outS, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
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
