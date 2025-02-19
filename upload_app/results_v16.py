import pandas as pd
import datetime

class results:
    def __init__(self, files):
        # self.pathobj = pathlib.Path(folder_path)
        # time_stripped = self.pathobj.name.split("__")[0].replace(self.pathobj.name.split("_")[0], "")[1:]
        # print(time_stripped)
        # self.dt = datetime.strptime(time_stripped, "%b-%d-%Y_%H%M%S")
        # self.test = self.pathobj.stem.split("_")[0]
        self.files = files
        self.results_dict = {}
        self.read_all_results()
    def read_all_results(self):
        for file in self.files.keys():
            # match case
            match file:
                case "SUMMARY_AllLevels.csv":
                    self.read_SUMMARY_csv(self.files[file])
                case "ProAnalysis.log":
                    self.read_ProAnalysis_log(self.files[file])
                case "ProBookmarkRendering2D.log":
                    self.read_ProBookmarkRendering2D_log(self.files[file])
                case "ProBookmarkRendering3D.log":
                    self.read_ProBookmarkRendering3D_log(self.files[file])
                case "ProContour.log":
                    self.read_ProContour_log(self.files[file])
                case "ProEditing.log":
                    self.read_ProEditing_log(self.files[file])
                case "ProFocalStatistics.log":
                    self.read_ProFocalStatistics_log(self.files[file])
                case "ProMapAlgebra.log":
                    self.read_ProMapAlgebra_log(self.files[file])
                case "ProProjection.log":
                    self.read_ProProjection_log(self.files[file])
                case "ProSpatialAnalysis.log":
                    self.read_ProSpatialAnalysis_log(self.files[file])
                case "ProStartup.log":
                    self.read_ProStartup_log(self.files[file])
                case "ProXYTableToPoint.log":
                    self.read_ProXYTableToPoint_log(self.files[file])
                case "SUMMARY_Level3.log":
                    self.read_Summary3_log(self.files[file])
                case "SUMMARY_Level2.log":
                    self.read_Summary2_log(self.files[file])
                case "SUMMARY_Level1.log":
                    self.read_Summary1_log(self.files[file])
        #print(self.results_dict)
    def read_SUMMARY_csv(self, file):
        df = pd.read_csv(file, sep=",")
        self.results_dict["Level_1_Total_Time"] = df["Level 1"].loc[0]
        self.results_dict["Level_2_Total_Time"] = df["Level 2"].loc[0]
        self.results_dict["Level_3_Total_Time"] = df["Level 3"].loc[0]
    def read_ProAnalysis_log(self, file):
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Buffer:" in line:
                self.results_dict["ProAnalysis_Buffer"] = float(line.split(" ")[-1])
            if "Select Layer by Attribute:" in line:
                self.results_dict["ProAnalysis_Select"] = float(line.split(" ")[-1])
            if "Pairwise Erase:" in line:
                self.results_dict["ProAnalysis_Erase"] = float(line.split(" ")[-1])
            if "Intersect:" in line:
                self.results_dict["ProAnalysis_Intersect"] = float(line.split(" ")[-1])
    def read_ProBookmarkRendering2D_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "FirstDrawTime (Layers): " in line:
                self.results_dict["ProRender2D_FirstDraw"] = line.split(" ")[-1]
                self.results_dict["ProRender2D_FirstDraw_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if "PerfTools Script Execution Time = " in line:
                self.results_dict["ProRender2D_ExecutionTime"] = line.split(" ")[-1]
                self.results_dict["ProRender2D_ExecutionTime_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if "DrawTime Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender2D_DrawTime_Sum"] = comma_split[0].split(": ")[-1]
                self.results_dict["ProRender2D_DrawTime_Sum_af"] = self.decode_timecode(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender2D_DrawTime_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender2D_DrawTime_Avg"] = comma_split[2].split(": ")[-1]
                self.results_dict["ProRender2D_DrawTime_Avg_af"] = self.decode_timecode(comma_split[2].split(": ")[-1])
            if "AverageFPS Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender2D_AverageFPS_Sum"] = float(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender2D_AverageFPS_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender2D_AverageFPS_Avg"] = float(comma_split[2].split(": ")[-1])
            if "MinimumFPS Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender2D_MinimumFPS_Sum"] = float(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender2D_MinimumFPS_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender2D_MinimumFPS_Avg"] = float(comma_split[2].split(": ")[-1])
            if line == "Bookmark, Map, DrawTime, AverageFPS, MinimumFPS, FPSSamples, TimeStamp":
                df = pd.read_csv(file, sep=", ", skiprows=line_counter+2, names=line.split(", "), nrows=11)
                self.results_dict["ProRender2D_FPS_Table"] = df
            line_counter += 1
    def read_ProBookmarkRendering3D_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "FirstDrawTime (Layers): " in line:
                self.results_dict["ProRender3D_FirstDraw"] = line.split(" ")[-1]
                self.results_dict["ProRender3D_FirstDraw_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if "PerfTools Script Execution Time = " in line:
                self.results_dict["ProRender3D_ExecutionTime"] = line.split(" ")[-1]
                self.results_dict["ProRender3D_ExecutionTime_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if "DrawTime Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender3D_DrawTime_Sum"] = comma_split[0].split(": ")[-1]
                self.results_dict["ProRender3D_DrawTime_Sum_af"] = self.decode_timecode(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender3D_DrawTime_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender3D_DrawTime_Avg"] = comma_split[2].split(": ")[-1]
                self.results_dict["ProRender3D_DrawTime_Avg_af"] = self.decode_timecode(comma_split[2].split(": ")[-1])
            if "AverageFPS Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender3D_AverageFPS_Sum"] = float(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender3D_AverageFPS_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender3D_AverageFPS_Avg"] = float(comma_split[2].split(": ")[-1])
            if "MinimumFPS Sum: " in line:
                comma_split = line.split(", ")
                self.results_dict["ProRender3D_MinimumFPS_Sum"] = float(comma_split[0].split(": ")[-1])
                self.results_dict["ProRender3D_MinimumFPS_Count"] = int(comma_split[1].split(": ")[-1])
                self.results_dict["ProRender3D_MinimumFPS_Avg"] = float(comma_split[2].split(": ")[-1])
            if line == "Bookmark, Map, DrawTime, AverageFPS, MinimumFPS, FPSSamples, TimeStamp":
                df = pd.read_csv(file, sep=", ", skiprows=line_counter+2, names=line.split(", "), nrows=11)
                self.results_dict["ProRender3D_FPS_Table"] = df
            line_counter += 1
    def read_ProContour_log(self, file):
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Polyline" in line:
                self.results_dict["ProContour_Polyline"] = float(line.split(" ")[-2])
            if "Polygon" in line:
                self.results_dict["ProContour_Polygon"] = float(line.split(" ")[-2])
            if "Script Execution Time = " in line:
                self.results_dict["ProContour_ExecutionTime"] = float(line.split(" ")[-1])
    def read_ProEditing_log(self, file):
        line_counter = 0
        table_count = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "PerfTools Script Execution Time = " in line:
                self.results_dict["ProEditing_ExecutionTime"] = line.split(" ")[-1]
                self.results_dict["ProEditing_ExecutionTime_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if line == "Bookmark, Map, DrawTime, AverageFPS, MinimumFPS, FPSSamples, TimeStamp":
                table_count += 1
                df = pd.read_csv(file, sep=", ", skiprows=line_counter+2, names=line.split(", "), nrows=1)
                self.results_dict[f"ProEditing_Table_{table_count:02}"] = df
            line_counter += 1
        
        fsplit = file.split("----\n")
        section_counter = 0
        for section in fsplit:
            if "Task: Draw Polyline Fence" in section:
                name = "DrawPolylineFence"
                interest = fsplit[section_counter + 1]
                for line in interest.split("\n"):
                    if '"' in line and "Time" in line:
                        line = line.replace("\t", "")
                        sline = line.split('"')
                        self.results_dict[f"ProEditing_{name}_{sline[0]}"] = self.decode_timecode(sline[1])
            if "Task: Digitize Trees" in section:
                name = "DigitizeTrees"
                interest = fsplit[section_counter + 1]
                for line in interest.split("\n"):
                    if '"' in line and "Time" in line:
                        line = line.replace("\t", "")
                        sline = line.split('"')
                        self.results_dict[f"ProEditing_{name}_{sline[0]}"] = self.decode_timecode(sline[1])
            section_counter += 1
    def read_ProFocalStatistics_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Script Execution Time = " in line:
                self.results_dict["ProFocalStats_ExecutionTime"] = float(line.split(" ")[-1])
            if "Elapsed time for" in line:
                sline = line.split(" ")
                self.results_dict[f"ProFocalStats_{sline[-4]}"] = float(sline[-2])
            line_counter += 1
    def read_ProMapAlgebra_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Script Execution Time = " in line:
                self.results_dict["ProMapAlgebra_ExecutionTime"] = float(line.split(" ")[-1])
            if "Elapsed time for" in line:
                sline = line.split(" ")
                self.results_dict[f"ProMapAlgebra_{sline[-4]}"] = float(sline[-2])
            line_counter += 1
    def read_ProProjection_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Script Execution Time = " in line:
                self.results_dict["ProProjection_ExecutionTime"] = float(line.split(" ")[-1])
            if "Elapsed time for" in line:
                sline = line.split(" ")
                self.results_dict[f"ProProjection_{sline[-4]}"] = float(sline[-2])
            line_counter += 1
    def read_ProSpatialAnalysis_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Slope:" in line:
                self.results_dict["ProSpatialAnalysis_Slope"] = float(line.split(" ")[-1])
            if "SlopeTest:" in line:
                self.results_dict["ProSpatialAnalysis_SlopeTest"] = float(line.split(" ")[-1])
            if "Aspect:" in line:
                self.results_dict["ProSpatialAnalysis_Aspect"] = float(line.split(" ")[-1])
            if "AspectTest:" in line:
                self.results_dict["ProSpatialAnalysis_AspectTest"] = float(line.split(" ")[-1])
            if "Viewshed:" in line:
                self.results_dict["ProSpatialAnalysis_Viewshed"] = float(line.split(" ")[-1])
            line_counter += 1
    def read_ProStartup_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "FirstDrawTime (Layers): " in line:
                self.results_dict["ProStartup_FirstDraw"] = line.split(" ")[-1]
                self.results_dict["ProStartup_FirstDraw_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            if "PerfTools Script Execution Time = " in line:
                self.results_dict["ProStartup_ExecutionTime"] = line.split(" ")[-1]
                self.results_dict["ProStartup_ExecutionTime_af"] = self.decode_timecode(line.split(" ")[-1])# af = as float
            line_counter += 1
        r = file
        fixed = r.split("--- Fixed Metrics ---")[1].split("--- Named Metrics ---")[0]
        named = r.split("--- Named Metrics ---")[1].split("==================")[0]
        lines = fixed.split("\n") + named.split("\n")
        for line in lines:
            line = line.replace("\n", "")
            if " = " in line:
                sline = line.split(" = ")
                varname = sline[0]
                v = sline[1]
                if ":" in v:
                    v = self.decode_timecode(v)
                else:
                    v = int(v)
                self.results_dict[f"ProStartup_{varname}"] = v
    def read_ProXYTableToPoint_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Script Execution Time = " in line:
                self.results_dict["ProXYTable_ExecutionTime"] = float(line.split(" ")[-1])
            if "Elapsed time for" in line:
                sline = line.split(" ")
                self.results_dict[f"ProXYTable_{sline[-4]}"] = float(sline[-2])
            line_counter += 1
    def read_Summary3_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Total Elapsed Time" in line:
                self.results_dict["Summary3_TotalElapsed"] = float(line.split(" ")[-1])
            if "ProSpatialAnalysis Elapsed" in line:
                self.results_dict["Summary3_SpatialAnalysis"] = float(line.split(" ")[-1])
            if "ProFocalStatistics Elapsed" in line:
                self.results_dict["Summary3_FocalStats"] = float(line.split(" ")[-1])
            if "ProContour Elapsed" in line:
                self.results_dict["Summary3_Contour"] = float(line.split(" ")[-1])
            if "ProMapAlgebra Elapsed" in line:
                self.results_dict["Summary3_MapAlgebra"] = float(line.split(" ")[-1])
            line_counter += 1
    def read_Summary2_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Total Elapsed Time" in line:
                self.results_dict["Summary2_TotalElapsed"] = float(line.split(" ")[-1])
            if "ProStartup Elapsed" in line:
                self.results_dict["Summary2_Startup"] = float(line.split(" ")[-1])
            if "ProBookmarkRendering (Philly3D) Elapsed" in line:
                self.results_dict["Summary2_BookmarkRendering"] = float(line.split(" ")[-1])
            if "ProEditing Elapsed" in line:
                self.results_dict["Summary2_Editing"] = float(line.split(" ")[-1])
            if "ProProjection Elapsed" in line:
                self.results_dict["Summary2_Projection"] = float(line.split(" ")[-1])
            if "ProXYTableToPoint Elapsed" in line:
                self.results_dict["Summary2_XYTable"] = float(line.split(" ")[-1])
            line_counter += 1
    def read_Summary1_log(self, file):
        line_counter = 0
        for line in file.split("\n"):
            line = line.replace("\n", "")
            if "Total Elapsed Time" in line:
                self.results_dict["Summary1_TotalElapsed"] = float(line.split(" ")[-1])
            if "ProBookmarkRendering (Portland) Elapsed" in line:
                self.results_dict["Summary1_BookmarkRendering"] = float(line.split(" ")[-1])
            if "ProAnalysis Elapsed" in line:
                self.results_dict["Summary1_Analysis"] = float(line.split(" ")[-1]) 
            line_counter += 1
    def decode_timecode(self, timecode):
        ts = timecode.split(":")
        # print(ts)
        h, m, s = int(ts[0]), int(ts[1]), float(ts[2])
        total = (h * 60 * 60) + (m * 60) + s
        return(total)