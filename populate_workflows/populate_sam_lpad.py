import os
import json
import argparse
from pathlib import Path
from fireworks import LaunchPad
from d3tales_api.Workflows.ParamSet import GausParamSet

from fireworks import Workflow
from d3tales_api.Workflows.Fireworks import (
    InitializeMolecule,
    WTuning,
    Optimization,
    Energy,
    TDDFT
)

BASE_DIR = Path(__file__).resolve().parent.parent


# Copyright 2021, University of Kentucky
def sams_wf(paramset, identifier=None, smiles=None, mol_opt_geom=None, wtune=True, wf_tag="", **kwargs):
    f10 = InitializeMolecule(identifier=identifier, smiles=smiles, mol_opt_geom=mol_opt_geom, **kwargs)
    f30 = WTuning(paramset=paramset.wtuning, parents=f10, **kwargs)

    opt_parents = f30 if wtune else f10
    f31 = Optimization(paramset=paramset.opt_groundState, species="groundState", parents=opt_parents, **kwargs)
    f35 = Optimization(paramset=paramset.opt_anion1, species="anion1", parents=opt_parents, **kwargs)
    f37 = Optimization(paramset=paramset.opt_cation1, species="cation1", parents=opt_parents, **kwargs)

    f45 = Energy(paramset=paramset.energy_groundState, species="groundState", geometry="opt_anion1", parents=[f35],
                 **kwargs)
    f46 = Energy(paramset=paramset.energy_anion1, species="anion1", geometry="opt_groundState", parents=[f31], **kwargs)
    f47 = Energy(paramset=paramset.energy_groundState, species="groundState", geometry="opt_cation1", parents=[f37],
                 **kwargs)
    f48 = Energy(paramset=paramset.energy_cation1, species="cation1", geometry="opt_groundState", parents=[f31],
                 **kwargs)

    f61 = TDDFT(paramset=paramset.tddft_groundState, parents=[f31], **kwargs)
    f65 = TDDFT(paramset=paramset.tddft_anion1, species='anion1', parents=[f35], **kwargs)
    f67 = TDDFT(paramset=paramset.tddft_cation1, species='cation1', parents=[f37], **kwargs)

    # Establish fireworks in workflow
    fws = [f10, f31, f35, f37, f45, f46, f47, f48, f61, f65, f67, ]
    if wtune:
        fws.extend([f30])

    wf = Workflow(fws, name="{}gaus_{}".format(wf_tag, identifier or smiles))

    return wf


def populate_sam_lpad(
        filename=None,
        workflow_function=sams_wf,
        priority=4,
        public=False,
        default_origin='Risko',
        submit=True,  # norm: True
        param_tag='gaus_',  # norm: gaus_  ( huckaba_ dihedral_ gaus_singlets_)
        restricted=True,  # norm: True
        wtune=True,  # norm: True
        run_nto=False,  # norm: False
        wf_tag="",  # ""
        data_store="local"
):
    """
    Function to initiate a series of D3TaLES workflows for a given set of molecules.
    """
    gaussian_file_name = 'gaussian_ur' if not restricted else 'gaussian'
    lpad_file = os.path.join(BASE_DIR.parent, 'config', 'my_launchpad.yaml')
    param_file = os.path.join(BASE_DIR, 'parameters', param_tag + 'parameter_file.json')

    mol_dict = {}
    if filename and os.path.isfile(filename):
        with open(filename, 'r') as f:
            mol_dict = json.load(f)

    paramset = GausParamSet().from_json(param_file)
    kwarg_dict = dict(paramset=paramset, public=public, submit=submit, data_store=data_store,
                      check_if_already_run=False, priority=priority,
                      gaussian_file_name=gaussian_file_name, restricted=restricted,
                      wtune=wtune, run_nto=run_nto, origin_group=default_origin, wf_tag=wf_tag)

    fw_id_list = []
    for smiles, geom in mol_dict.items():
        kwarg_dict.update(smiles=smiles, mol_opt_geom=geom)
        wf = workflow_function(**kwarg_dict)
        info = LaunchPad().from_file(lpad_file).add_wf(wf)
        fw_id = list(info.values())[0]
        fw_id_list.append(fw_id)

    print("Added {} workflows to the launchpad".format(len(fw_id_list)))
    print("FW ID List: ", ''.join(str(fw_id_list).split(' ')))
    return fw_id_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch SAMs FireWorks workflow.')
    parser.add_argument('filename', metavar='filename', type=str, help='filepath for a JSON molecule file',
                        default=False)
    parser.add_argument('-p', '--priority', type=int, help='jobs priority', default=2)

    args = parser.parse_args()

    KWARGS = dict(
        workflow_function=sams_wf,
        default_origin="Risko"
    )

    populate_sam_lpad(filename=args.filename, priority=args.priority, **KWARGS)
