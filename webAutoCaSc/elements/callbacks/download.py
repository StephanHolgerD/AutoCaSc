import pandas as pd
import io
from AutoCaSc_core.AutoCaSc import AutoCaSc, VERSION



def download(results_memory, transcripts_to_use):
    df = pd.DataFrame()
    for i, _variant in enumerate(results_memory.get("instances").keys()):
        try:
            if _variant in transcripts_to_use.keys():
                _transcript = transcripts_to_use.get(_variant)
            else:
                _transcript = \
                    list(results_memory.get("instances").get(_variant).get("transcript_instances").keys())[0]
        except AttributeError:
            _transcript = list(results_memory.get("instances").get(_variant).get("transcript_instances").keys())[0]

        _instance_attributes = \
            results_memory.get("instances").get(_variant).get("transcript_instances").get(_transcript)

        try:
            if _instance_attributes.get("vcf_string") in df["vcf_format_2"].to_list():
                continue
        except KeyError:
            pass
        if _instance_attributes.get("inheritance") == "comphet":
            comphet = True
            _other_variant = _instance_attributes.get("other_variant")
            _other_instance_attributes = results_memory.get("instances").get(_other_variant).get(
                "transcript_instances").get(_transcript)
        else:
            comphet = False
            _other_instance_attributes = {}
        df.loc[i, "hgnc_symbol"] = _instance_attributes.get("gene_symbol")
        df.loc[i, "transcript"] = _transcript
        df.loc[i, "vcf_format_1"] = _instance_attributes.get("vcf_string")
        df.loc[i, "vcf_format_2"] = _other_instance_attributes.get("vcf_string")
        df.loc[i, "cDNA_1"] = _instance_attributes.get("hgvsc_change")
        df.loc[i, "cDNA_2"] = _other_instance_attributes.get("hgvsc_change")
        df.loc[i, "amino_acid_1"] = _instance_attributes.get("hgvsp_change")
        df.loc[i, "amino_acid_2"] = _other_instance_attributes.get("hgvsp_change")
        df.loc[
            i, "var_1_full_name"] = f"{_instance_attributes.get('transcript')}:" \
                                    f"{_instance_attributes.get('hgvsc_change')} " \
                                    f"{_instance_attributes.get('hgvsp_change')}"
        if comphet:
            df.loc[
                i, "var_2_full_name"] = f"{_other_instance_attributes.get('transcript')}:" \
                                        f"{_other_instance_attributes.get('hgvsc_change')} " \
                                        f"{_other_instance_attributes.get('hgvsp_change')}"
        else:
            df.loc[i, "var_2_full_name"] = ""
        df.loc[i, "inheritance"] = _instance_attributes.get("inheritance")
        df.loc[i, "candidate_score"] = _instance_attributes.get("candidate_score")
        df.loc[i, "literature_plausibility"] = _instance_attributes.get("gene_plausibility")
        df.loc[i, "inheritance_score"] = _instance_attributes.get("inheritance_score")
        if comphet:
            df.loc[i, "variant_attribute_score"] = round(mean([_instance_attributes.get("variant_score"),
                                                               _other_instance_attributes.get("variant_score")]), 2)
        else:
            df.loc[i, "variant_attribute_score"] = _instance_attributes.get("variant_score")
        df.loc[i, "gene_constraint_score"] = _instance_attributes.get("gene_constraint_score")
        df["version"] = str(VERSION)

    data = io.StringIO()
    df.to_csv(data, sep="\t", decimal=",")
    data.seek(0)
    return dict(content=data.getvalue(), filename="AutoCaSc_results.tsv")