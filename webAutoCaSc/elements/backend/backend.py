import pandas as pd
from AutoCaSc_core.AutoCaSc import AutoCaSc, VERSION
import copy

########## BACKEND ##########
def score_variants(instances, inheritance):
    instances_processed = []
    if inheritance == "comphet":
        variant_transcript_df = pd.DataFrame()
        for _variant_instance in instances:
            _variant_instance.inheritance = "comphet"
            if _variant_instance.__dict__.get("status_code") == 200:
                for _transcript in _variant_instance.__dict__.get("affected_transcripts"):
                    variant_transcript_df.loc[len(variant_transcript_df), "variant"] = _variant_instance.__dict__.get(
                        "variant")
                    variant_transcript_df.loc[len(variant_transcript_df) - 1, "transcript"] = _transcript
                    variant_transcript_df.loc[len(variant_transcript_df) - 1, "instance"] = _variant_instance
            else:
                instances_processed.append(_variant_instance)

        for _variant in variant_transcript_df.variant.unique():
            match_found = False
            _variant_instance = variant_transcript_df.loc[variant_transcript_df.variant == _variant, "instance"].values[
                0]
            for _transcript in variant_transcript_df.loc[variant_transcript_df.variant == _variant].transcript.unique():
                df_chunk = variant_transcript_df.loc[variant_transcript_df.transcript == _transcript].reset_index(
                    drop=True)
                if len(df_chunk) == 2:
                    transcript_instance_1 = copy.deepcopy(_variant_instance)
                    transcript_instance_1.__dict__.pop("transcript_instances")
                    transcript_instance_1.assign_results(_transcript)

                    variant_instance_2 = df_chunk.loc[(df_chunk.transcript == _transcript)
                                                      & (df_chunk.variant != _variant), "instance"].values[0]
                    transcript_instance_2 = copy.deepcopy(variant_instance_2)
                    transcript_instance_2.__dict__.pop("transcript_instances")
                    transcript_instance_2.assign_results(_transcript.split(".")[0])

                    transcript_instance_1.other_autocasc_obj = transcript_instance_2
                    transcript_instance_1.calculate_candidate_score()
                    _variant_instance.transcript_instances[_transcript] = copy.deepcopy(transcript_instance_1)
                    match_found = True
                else:
                    _variant_instance.affected_transcripts.remove(_transcript)
            if not match_found:
                _variant_instance.status_code = 301
            else:
                for _attribute in ["candidate_score", "other_variant", "other_autocasc_obj"]:
                    _variant_instance.__dict__[_attribute] = \
                        list(_variant_instance.transcript_instances.values())[0].__dict__.get(_attribute)
            instances_processed.append(_variant_instance)

    else:
        for _instance in instances:
            _instance.update_inheritance(inheritance=inheritance)
            if _instance.__dict__.get("status_code") == 200:
                highest_casc = 0
                transcript_to_use = _instance.get("affected_transcripts")[0]
                for _transcript in _instance.get("affected_transcripts"):
                    _transcript_instance = copy.deepcopy(_instance)
                    _transcript_instance.__dict__.pop("transcript_instances")


                    _transcript_instance.__dict__["transcript"] = _transcript  # added this line on 2021-12-06


                    _transcript_instance.assign_results(_transcript, clear_params=True)
                    _transcript_instance.__dict__["mode"] = "web"
                    _transcript_instance.calculate_candidate_score()
                    _instance.transcript_instances[_transcript] = _transcript_instance
                    if _transcript_instance.candidate_score > highest_casc:
                        transcript_to_use = _transcript
                        highest_casc = _transcript_instance.candidate_score
                        affected_transcripts_id = _instance.get("affected_transcripts").index(transcript_to_use)
                _instance.affected_transcripts[0], _instance.affected_transcripts[affected_transcripts_id] = \
                    _instance.affected_transcripts[affected_transcripts_id], _instance.affected_transcripts[0]
            instances_processed.append(_instance)
    return instances_processed

def dict_to_instances(dict):
    instances = []
    try:
        for _variant in dict.get("instances").keys():
            _instance = dict.get("instances").get(_variant)
            assembly  = _instance.get('assembly')

            instance = AutoCaSc(_variant, mode="web",assembly=assembly)
            if _instance.get("data_retrieved"):
                for _key in _instance.keys():
                    instance.__dict__[_key] = _instance.get(_key)
            instances.append(instance)
        return instances
    except AttributeError:
        return None

def instances_to_dict(instance, recursion_level=0):
    instance_dict = {}
    if isinstance(instance, dict):
        items = instance.items()
    else:
        items = instance.__dict__.items()
    for key, value in items:
        if any([x in type(value).__name__ for x in ["int", "float", "bool", "NoneType", "str", "list"]]):
            instance_dict[key] = value
        else:
            if type(value).__name__ == "AutoCaSc":
                if recursion_level < 1:
                    instance_dict[key] = instances_to_dict(value, recursion_level + 1)
            else:
                instance_dict[key] = instances_to_dict(value, recursion_level)
    return instance_dict

def store_instances(instance_list, code_key="variant"):
    # this is needed to turn AutoCaSc instances to dicts in order to store them in a dcc.Store.
    instance_dicts = [instances_to_dict(_instance) for _instance in instance_list]
    return {"instances": {_instance_dict.get(code_key): _instance_dict for _instance_dict in instance_dicts}}


def clean_genomeversion(genomeversion):
    if genomeversion=='HG19':
        genomeversion='GRCh37'
    else:
        genomeversion='GRCh38'
    return genomeversion