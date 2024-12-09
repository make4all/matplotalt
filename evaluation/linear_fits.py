import sys
import numpy as np
from scipy.stats import linregress, pearsonr
from contextlib import redirect_stdout

with open("./correlation_output.txt", "w") as output_file:
    with redirect_stdout(output_file):

        sim_metric_arrs = np.load("./caption_sim_metric_to_arr.npy", allow_pickle=True).item()
        blip_metric_arrs = np.load("./caption_blip_metric_to_arr.npy", allow_pickle=True).item()

        linear_fits = {
            "human_sim": {},
            "blipscores": {}
        }

        print("Human similarity len lines of fit ---------------------------------------")
        sim_len_arrs = sim_metric_arrs["lens"]
        for metric_name, cap_scores in sim_metric_arrs.items():
            if metric_name != "lens":
                #linfit = linregress(sim_len_arrs, cap_scores)
                print(f"Correlation between desc len and {metric_name}: {pearsonr(sim_len_arrs, cap_scores)}")
                #linear_fits["human_sim"][metric_name] = linfit
                #print(f"{metric_name}: {linfit}")

        print("BLIP len lines of fit ---------------------------------------")
        blip_len_arrs = blip_metric_arrs["lens"]
        for metric_name, cap_scores in blip_metric_arrs.items():
            if metric_name != "lens":
                #linfit = linregress(blip_len_arrs, cap_scores)
                print(f"Correlation between desc len and {metric_name}: {pearsonr(blip_len_arrs, cap_scores)}")
                #linear_fits["blipscores"][metric_name] = linfit
                #print(f"{metric_name}: {linfit}")

        #np.save("./len_linear_fits", linear_fits)

        print("correlation between blipscores and human sims --------------------------")
        # Correlation between blipscores and similarity to human captions
        blipscores_and_human_sims = np.load("./blipscores_and_human_sims.npy", allow_pickle=True).item()
        sim_metric_to_arr = blipscores_and_human_sims["sim_metrics"]
        for blip_metric in ["blip-probs", "blip-sims"]:
            cur_blip_scores = blipscores_and_human_sims[blip_metric]
            for sim_metric, sim_scores in sim_metric_to_arr.items():
                print(f"Correlation between {blip_metric} and {sim_metric}: {pearsonr(cur_blip_scores, sim_scores)}")


        # Correlation between manually labeled correct / incorrect and other scores
        annotated_caption_stat_arrs = np.load("./annotated_caption_stat_arrs.npy", allow_pickle=True).item()
        annotated_desc_lens = annotated_caption_stat_arrs["lens"]
        annotated_blipscores = annotated_caption_stat_arrs["blipscores"]
        annotated_errors = annotated_caption_stat_arrs["errors"]
        annotated_vistext_sims = annotated_caption_stat_arrs["vistext_human_sims"]
        annotated_vistext_errors = annotated_caption_stat_arrs["vistext_errors"]

        val_errors = ["chart type error", "axis error", "value error", "identity error", "trend error", "label error", "nonsense error", "deceptive error"]
        annotated_errors["val-correct"] = np.logical_not(np.logical_or.reduce([annotated_errors[err_type] for err_type in val_errors]))
        annotated_vistext_errors["val-correct"] = np.logical_not(np.logical_or.reduce([annotated_vistext_errors[err_type] for err_type in val_errors]))
        print("Correlation between error occurances and blipscores + lens --------------------------")
        for err_type, err_bool_arr in annotated_errors.items():
            print(f"Correlation between {err_type} and desc len: {pearsonr(annotated_desc_lens, err_bool_arr)}")
            print(f"Correlation between {err_type} and BLIP prob: {pearsonr(annotated_blipscores['prob'], err_bool_arr)}")
            print(f"Correlation between {err_type} and BLIP cos sim: {pearsonr(annotated_blipscores['cos-sim'], err_bool_arr)}")

        print("Correlation between error occurances and human sims --------------------------")
        for err_type, err_bool_arr in annotated_vistext_errors.items():
            for sim_metric, sim_scores in annotated_vistext_sims.items():
                print(f"Correlation between {err_type} and {sim_metric}: {pearsonr(err_bool_arr, sim_scores)}")