# ******************************************************************************
# graph_based_anomaly.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 3/1/19   Paudel     Initial version,
# ******************************************************************************
import os

class GraphBasedAnomaly():
    def run_anomaly_detection(self, d, graph_file, parameters):
        output_file = d[0]+ "_result.txt"
        graph_command = "bin/gbad " + parameters + ">>" + output_file

        command = GBAD.gbad_home + "/" + GBAD.run_command + " -nsubs " + str(
            param_n) + " -out " + subgraph_file + " " + graph_file + ">>" + output_file

        os.system(graph_command)
        return output_file