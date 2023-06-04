from datetime import datetime
from functools import partial
from source.util import *
from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
import threading
import requests
import pytz
from source.mission.index_generator import generate_mission_index

"""
Structure of missiondoanload_meta.json (used for local_mission_meta):
{
    "mission_name": {
        "name": "mission_name",
        "url": "https://github.com/.../mission_name.py"
        "author": "author",
        "tags": ["tag1", "tag2"],
        "title" : "title",
        "description": "description",
        "note": "note",
        "last_update": "2021-01-01 00:00:00",
        "create_time": "2021-01-01 00:00:00",
        "download_time" "2021-01-01 00:00:00",
    }
}

Sturcture of index.json (used for available_missions):
{
    "about": "",
    "tags": {
        "tag1": "tag description",
        "tag2": "tag description"
    },
    "missions": [
        {
            "name": "mission_name",
            "url": "https://github.com/.../mission_name.py",
            "author": "author",
            "tags": ["tag1", "tag2"],
            "title" : "title",
            "description": "description",
            "note": "note",
            "last_update": "2021-01-01 00:00:00",
            "create_time": "2021-01-01 00:00:00"
        }
    ]
}
"""
# TODO 待做
# TODO: Apply and Save 和 Install后自动编译

class MissionDownloadPage(AdvancePage):
    NAME_PROCESSBAR_MissionRebuild = 'PROCESSBAR_MissionRebuild'
    def __init__(self) -> None:
        super().__init__()
        self.REMOTE_REPO = "https://github.com/GenshinImpactAssistant/GIA-Missions"
        
        self.INDEX_SOURCE = {
            "Github (Direct)": "https://raw.githubusercontent.com/GenshinImpactAssistant/GIA-Missions/main/index.json",
            "Github (ghproxy.com)": "https://ghproxy.com/https://raw.githubusercontent.com/GenshinImpactAssistant/GIA-Missions/main/index.json",
            "Github (ghrpoxy.net)": "https://ghproxy.net/https://raw.githubusercontent.com/GenshinImpactAssistant/GIA-Missions/main/index.json"
        }
        self.INDEX_SOURCE_OPTIONS = [key+":  "+value for key, value in self.INDEX_SOURCE.items()]
        self.INDEX_SOURCE_SELECT = "Github (Direct)"
        self.INDEX_URL = self.INDEX_SOURCE[self.INDEX_SOURCE_SELECT]
        self.INDEX_URL = self.INDEX_URL.replace("index.json", "index_"+GLOBAL_LANG+".json") if GLOBAL_LANG in ["zh_CN", "en_US"] else self.INDEX_URL
        self.requests_headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}

        self.LOCAL_MISSION_FOLDER = f"{ROOT_PATH}\\missions"
        self.BACKUP_MISSION_FOLDER = f"{ROOT_PATH}\\missions\\backup"
        self.DISABLE_MISSION_FOLDER = f"{ROOT_PATH}\\missions\\disable"
        self.MISSION_DOWNLOAD_CONFIG_FOLDER = f"{CONFIG_PATH}\\missiondownload"

        self.local_mission_names = []
        self.enable_mission_names = []
        self.disable_mission_names = []
        self.local_mission_meta = {}
        self.mission_update_status = {}

        self.available_missions = {"missions": [], "tags": {}}
        self.available_missions_dict = {} # The same as available_missions, but in dict format.

        self._create_default_settings()
        self.local_mission_names, self.enable_mission_names, self.disable_mission_names = self._read_local_mission_names()
        self.local_mission_meta = self._read_local_mission_meta()
        self.mission_update_status = {mission_name: t2t("Unknown") for mission_name in self.local_mission_names}

        self.available_missions_display = [] # Missions to be displayed in the table. Depend on the filter settings.
        self.tags = [] # Tags to be displayed in the tag filter. From available_missions.
        self.hidden_number = 0 # Number of missions that are hidden by the filter settings.

        self.order_options = [t2t("newest first"), t2t("oldest first"), t2t("a-z"), t2t("z-a"), t2t("internal order")] # The order options for the table. Used in the order filter.
        self.error_occured = False # Whether an error occured during the process. Used in _apply_and_save.

    """
    The following methods are used to produce the UI.
    """
    def _load(self):
        """
        The entrance of the render process. Load the page.
        """
        with output.use_scope(self.main_scope):
            output.put_text("")
            output.put_scope("missiondownload-upload-board").style('border: 1px solid #0099FF; border-radius: 5px; padding: 10px; text-align: center;')
            output.put_text("")
            output.put_scope("missiondownload-setting-board")
            output.put_tabs([
                {"title": t2t("Installed"), "content": output.put_scope("missiondownload-installed-board")},
                {"title": t2t("Available"), "content": output.put_scope("missiondownload-available-board")},
            ])
        self._render_boards()

        # pin_on_change on setting_board
        pin.pin_on_change(name = "SELECT_INDEX_URL", onchange = self._on_select_index_url, init_run = False)
        
        # pin_on_change on available_board
        pin.pin_on_change(name = "CHECKBOX_HIDE_TAGS", onchange = self._render_available_table, init_run = False)
        pin.pin_on_change(name = "RADIO_SORT_BY", onchange = self._render_available_table, init_run = False)
        pin.pin_on_change(name = "INPUT_FILTER", onchange = self._render_available_table, init_run = False)
    

    def _render_boards(self):
        self._render_upload_board()
        self._render_setting_board()
        self._render_installed_board()
        self._render_available_board()

    def _render_upload_board(self):
        with output.use_scope("missiondownload-upload-board"):
            output.put_link(name=t2t("Upload and share your custom missions! (Custom Mission Document)"), url=self.REMOTE_REPO, new_window=True)

    def _render_setting_board(self):
        with output.use_scope("missiondownload-setting-board"):
            pin.put_select(name = "SELECT_INDEX_URL", label=t2t("Load index from:"),
                           options=self.INDEX_SOURCE_OPTIONS, value=self.INDEX_SOURCE_OPTIONS[0], # type: ignore
                           help_text=t2t("If error occurs, please check first whether this option is set correctly."))

    def _render_installed_board(self):
        self.mission_update_status = {mission_name: t2t("Unknown") for mission_name in self.local_mission_names}

        with output.use_scope("missiondownload-installed-board", clear=True):
            output.put_grid([
                [
                    pin.put_radio(label=t2t("Disable all missions"), name="RADIO_DISABLE_ALL_MISSIONS", options=["Yes", "No"], value="No", inline=True),
                    output.put_button(label=t2t("Check for Updates"), color="primary", outline=True, onclick=self._onclick_check_updates),
                    output.put_button(label=t2t("Apply and Save"), color="danger", outline=True, onclick=self._onclick_apply_and_save)
                ],
                [output.span(output.put_scope("missiondownload-installed-table"), col=3)] # type: ignore
            ])
        
        self._render_installed_table()
    
    def _render_installed_table(self):
        # Convert local_mission_meta to table
        table = []
        header = [t2t("Enabled"), t2t("ID"), t2t("Mission"), t2t("Tags"), t2t("Author"), t2t("Description"), t2t("Last Update Time"), t2t("Update")]
        header = [output.put_text(_) for _ in header]
        header = header + [output.put_text(t2t("Delete")).style("color: red")]
        table.append(header)
        for mission_name in self.local_mission_names:
            entry = self.local_mission_meta[mission_name]
            Enabled = False if mission_name in self.disable_mission_names else True
            Enabled_Checkbox = pin.put_checkbox(label="", name=f"ENABLED_{mission_name}", options=[""], value=["" if Enabled else None], inline=True).style("text-align: right")
            
            ID = entry["name"]
            Mission = entry["title"]
            entry_tags = entry["tags"]
            if t2t("installed") in entry["tags"]:
                entry_tags.remove(t2t("installed"))
            Tags = ", ".join(entry_tags)
            Author = entry["author"]
            Description = entry["description"]
            # Note = entry["note"]
            Last_Update_Time = entry["last_update"]
            # Download_Time = entry["download_time"]
            text_entry = [ID, Mission, Tags, Author, Description, Last_Update_Time]
            text_entry = [output.put_text(_) for _ in text_entry]

            Update = self.mission_update_status[mission_name]
            if Update == t2t("Update available"):
                Update = pin.put_checkbox(label="", name=f"UPDATE_{mission_name}", options=[t2t("Update")], value=[], inline=True).style("text-align: left; color:blue")
            elif Update == t2t("No update available"):
                Update = output.put_text("/")
            elif Update == t2t("Unknown"):
                Update = output.put_text(t2t("Unknown")).style("color: gray")
            else:
                Update = output.put_text(Update).style("color: red")
            
            Delete = pin.put_checkbox(label="", name=f"DELETE_{mission_name}", options=[""], value=[], inline=True).style("text-align: center")
            
            table += [[Enabled_Checkbox]+text_entry+[Update, Delete]]
        with output.use_scope("missiondownload-installed-table", clear=True):
            output.put_table(table)
    
    def _render_available_board(self):
        with output.use_scope("missiondownload-available-board", clear=True):
            output.put_button(label=t2t("Load/refresh mission index from remote"), color="primary", outline=True, onclick=self._refresh_available_board)
            if len(self.available_missions["tags"]) == 0:
                output.put_markdown(t2t("Please load the mission index first."))
            else:
                tagset = [t2t("installed")] + list(self.available_missions["tags"].keys())
                output.put_row([
                    pin.put_checkbox(name = "CHECKBOX_HIDE_TAGS", options=tagset, value=[t2t("installed")], inline=True, label=t2t("Hide tags:")), # type: ignore
                    pin.put_radio(name = "RADIO_SORT_BY", options=self.order_options, value=self.order_options[0], inline=True, label=t2t("Order:")) # type: ignore
                ])
                pin.put_input(name="INPUT_FILTER", label=t2t("Search:"), type="text", value="")
                output.put_scope("missiondownload-available-table")
                self._render_available_table()
    
    def _refresh_available_board(self):
        output.toast(t2t("Downloading mission index..."), color="info")
        self._refresh_available_missions()
        # Reset the Filter by rendering the board again
        self._render_available_board()
        output.toast(t2t("Finished downloading mission index"), color="success")

    def _render_available_table(self, piponchange=None):
        def onclick_install(mission_name):
            output.toast(t2t("Installing mission..."), color="info")
            self._download_mission(self.available_missions_dict[mission_name])
            self._render_installed_board()
            self._render_available_table()
            output.toast(t2t("Mission installed, please apply and save."), color="success")
        
        hide_tags = list(pin.pin["CHECKBOX_HIDE_TAGS"])
        sort_by = self.order_options.index(str(pin.pin["RADIO_SORT_BY"]))
        filter_text = str(pin.pin["INPUT_FILTER"])
        
        available_missions_display, hidden_number = self._get_available_missions_display(hide_tags, sort_by, filter_text)
        
        table = []
        header = [t2t("ID"), t2t("Mission"), t2t("Tag"), t2t("Author"), t2t("Description"), t2t("Last Update Time"), t2t("Action")]
        header = [output.put_text(_) for _ in header]
        table.append(header)

        for entry in available_missions_display:
            mission_name = entry["name"]
            ID = entry["name"]
            Mission = entry["title"]
            entry_tags = entry["tags"]
            Tags = ", ".join(entry_tags)
            Author = entry["author"]
            Description = entry["description"]
            Last_Update_Time = entry["last_update"]
            text_entry = [ID, Mission, Tags, Author, Description, Last_Update_Time]
            text_entry = [output.put_text(_) for _ in text_entry]

            if t2t("installed") in entry_tags:
                Action = output.put_text(t2t("Installed")).style("color: gray")
            else:
                Action = output.put_button(label=t2t("Install"), color="primary", onclick=partial(onclick_install, mission_name))
            
            table += [text_entry+[Action]]
        
        with output.use_scope("missiondownload-available-table", clear=True):
            if hidden_number > 0:
                output.put_text(f"{hidden_number} "+t2t("missions are hidden."))
            output.put_table(table)

    def _render_progress_popup(self):
        output.popup(t2t('Apply and Save'), [
            output.put_markdown(t2t('Please wait for the progress to finish.')),
            output.put_processbar(name="PROGRESS_APPLY_AND_SAVE", label=t2t('Update Progress'), auto_close=False),
            output.put_processbar(name=self.NAME_PROCESSBAR_MissionRebuild, label=t2t('Rebuild Progress'), auto_close=False),
            output.put_text("\n"),
            output.put_scope("POPUP_CLOSE")
        ], implicit_close = False)

    def _render_delete_confirm_popup(self, disable_list, update_list, disable_all, delete_list):
        delete_backup_message = t2t("Delete all backup files for this mission as well")
        def confirm_delete():
            output.close_popup()
            delete_backup = True if pin.pin["CHECKBOX_DELETE_BACKUP_CONFIRM"] ==  [delete_backup_message] else False
            self._apply_and_save(disable_list, update_list, disable_all, delete_list, delete_backup)
        
        output.popup(t2t('Delete Confirm'), [
            output.put_markdown(t2t('Are you sure you want to delete the selected missions?')),
            output.put_markdown(t2t('Notice: This action **cannot** be undone!')),
            pin.put_checkbox(name="CHECKBOX_DELETE_BACKUP_CONFIRM", options=[delete_backup_message], inline=True).style("color: red"),
            output.put_text("\n"),
            output.put_row([
                None,
                output.put_button(label=t2t("Confirm"), color="danger", onclick=confirm_delete),
                output.put_button(label=t2t("Cancel"), color="primary", onclick=output.close_popup),
                None
            ], size='20% 30% 30% 20%')
        ], implicit_close = False)

    def _event_thread(self):
        time.sleep(0.1)
    

    """
    The following methods are used to process the data.
    """
    def _on_select_index_url(self, option_select):
        # option like: Github (Direct):  https://raw.githubusercontent.com/GenshinImpactAssistant/GIA-Missions/main/index.json
        self.INDEX_SOURCE_SELECT = option_select.split(":  ")[0]
        self.INDEX_URL = option_select.split(":  ")[1]
        self.INDEX_URL = self.INDEX_URL.replace("index.json", "index_"+GLOBAL_LANG+".json") if GLOBAL_LANG in ["zh_CN", "en_US"] else self.INDEX_URL

    def _create_folder_if_not_exist(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def _create_default_settings(self):
        """
        Create the default settings for missiondownload if the settings file is not exist.
        """
        self._create_folder_if_not_exist(self.LOCAL_MISSION_FOLDER)
        self._create_folder_if_not_exist(self.BACKUP_MISSION_FOLDER)
        self._create_folder_if_not_exist(self.DISABLE_MISSION_FOLDER)
        self._create_folder_if_not_exist(self.MISSION_DOWNLOAD_CONFIG_FOLDER)
        
        j = load_json("missiondownload_meta.json", self.MISSION_DOWNLOAD_CONFIG_FOLDER, auto_create=True)

    def _read_local_mission_names(self):
        """
        Scan the local mission folder and return the mission names.

        Returns:
            List: The mission names.
        """
        # Mission file should be .py stored in LOCAL_MISSION_FOLDER and DISABLE_MISSION_FOLDER
        # Files in subfolder will be ignored.
        enable_missions = []
        disable_missions = []
        for f in os.listdir(self.LOCAL_MISSION_FOLDER):
            if os.path.isfile(os.path.join(self.LOCAL_MISSION_FOLDER, f)) and f.endswith(".py"):
                f = f[:-3]
                if f in ["mission_index", "mission_meta"]:
                    continue
                enable_missions.append(f)
        for f in os.listdir(self.DISABLE_MISSION_FOLDER):
            if os.path.isfile(os.path.join(self.DISABLE_MISSION_FOLDER, f)) and f.endswith(".py"):
                f = f[:-3]
                if f in ["mission_index", "mission_meta"]:
                    continue
                disable_missions.append(f)
        # Unique the mission names
        enable_missions = list(set(enable_missions))
        # If a mission is in both enable_missions and disable_missions, it will be enabled.
        disable_missions = list(set(disable_missions) - set(enable_missions))
        local_missions = enable_missions + disable_missions
        return local_missions, enable_missions, disable_missions
    
    def _read_local_mission_meta(self):
        j = load_json("missiondownload_meta.json", self.MISSION_DOWNLOAD_CONFIG_FOLDER, auto_create=True)
        # Deal with missions in local_mission_names but not in missiondownload_meta.json
        for mission_name in self.local_mission_names:
            if mission_name not in j:
                j[mission_name] = {
                    "name": mission_name,
                    "url": None,
                    "author": "Self-customized",
                    "tags": ["Self-customized"],
                    "title" : mission_name,
                    "description": "",
                    "note": "",
                    "last_update": None,
                    "create_time": None,
                    "download_time": None
                }
        save_json(j, "missiondownload_meta.json", self.MISSION_DOWNLOAD_CONFIG_FOLDER)
        return j

    def _convert_url_to_download_link(self, url):
        """
        Convert the url to download link, depends on the INDEX_SOURCE_SELECT.
        """
        if self.INDEX_SOURCE_SELECT not in ["Github (ghproxy.net)"]:
            url = url.replace("/blob/", "/raw/")
        if self.INDEX_SOURCE_SELECT == "Github (Direct)":
            return url
        elif self.INDEX_SOURCE_SELECT == "Github (ghproxy.com)":
            return "https://ghproxy.com/" + url
        elif self.INDEX_SOURCE_SELECT == "Github (ghproxy.net)":
            return "https://ghproxy.net/" + url
        return url

    def _refresh_available_missions(self):
        """
        Download the mission index and refresh the available_missions and available_missions_dict.
        """
        # NOTE: Multi thread may be needed here.
        url = self.INDEX_URL
        try:
            r = requests.get(url, headers=self.requests_headers)
            if r.status_code == 200:
                result = r.text
                self.available_missions = json.loads(result)
                self.available_missions_dict = {m["name"]: m for m in self.available_missions["missions"]}
            else:
                self.error_occured = True
                logger.error(f"Failed to download the mission index from {url}. Status code: {r.status_code}")
                output.toast(f"Failed to download the mission index from {url}. Status code: {r.status_code}", duration = 5, color="error")
        except Exception as e:
            self.error_occured = True
            logger.error(f"Failed to download the mission index from {url}: {e}")
            output.toast(f"Failed to download the mission index from {url}", duration = 5, color="error")
    
    def _get_file_path(self, mission_name):
        if os.path.exists(os.path.join(self.LOCAL_MISSION_FOLDER, mission_name+".py")):
            return os.path.join(self.LOCAL_MISSION_FOLDER, mission_name+".py")
        if os.path.exists(os.path.join(self.DISABLE_MISSION_FOLDER, mission_name+".py")):
            return os.path.join(self.DISABLE_MISSION_FOLDER, mission_name+".py")
        return os.path.join(self.LOCAL_MISSION_FOLDER, mission_name+".py")

    def _download_mission(self, mission_meta):
        """
        Download the mission from the remote (i.e. github).
        If the mission is already exist, it will be put into the backup folder.
        Update missiondownload_meta.json
        
        Args:
            mission_meta (Dict): The mission meta data from available_missions.
        """
        name = mission_meta["name"]
        # Download the mission from the url
        url = mission_meta["url"]
        file_path = self._get_file_path(name)
        url = self._convert_url_to_download_link(url)
        try:
            r = requests.get(url, headers=self.requests_headers)
            if r.status_code == 200:
                # If the mission is already exist, it will be put into the backup folder.
                if os.path.exists(file_path):
                    # Backup the mission. Keep the latest 3 backups.
                    backup_folder = f"{self.BACKUP_MISSION_FOLDER}\\{name}"
                    if not os.path.exists(backup_folder):
                        os.makedirs(backup_folder)
                    backup_files = [f for f in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, f)) and f.endswith(".py")]
                    if len(backup_files) >= 3:
                        backup_files.sort()
                        os.remove(os.path.join(backup_folder, backup_files[0]))
                    shutil.move(file_path, f"{backup_folder}\\{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.py")
                
                # Save the mission
                with open(file_path, "wb") as f:
                    f.write(r.content)
                
                # Update the mission list
                self.local_mission_names, self.enable_mission_names, self.disable_mission_names = self._read_local_mission_names()

                # Update the mission meta
                j = load_json("missiondownload_meta.json", self.MISSION_DOWNLOAD_CONFIG_FOLDER)
                mission_meta["download_time"] = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
                j[name] = mission_meta
                save_json(j, "missiondownload_meta.json", self.MISSION_DOWNLOAD_CONFIG_FOLDER)
                self.local_mission_meta = self._read_local_mission_meta()
        except Exception as e:
            self.error_occured = True
            logger.error(f"Error downloading mission {name}: {e}")
            output.toast(f"Error downloading mission {name} from {url}", duration = 5, color="error")
    
    def _apply_disable(self, disable_list):
        """
        Disable the mission.
        That is, move the mission from LOCAL_MISSION_FOLDER to DISABLE_MISSION_FOLDER if it should be disabled.
        And, move the mission from DISABLE_MISSION_FOLDER to LOCAL_MISSION_FOLDER if it should be enabled.

        Args:
            disable_list (List): A list containg the mission names to be disabled.
        """
        for mission_name in self.local_mission_names:
            if mission_name in disable_list:
                if os.path.exists(f"{self.LOCAL_MISSION_FOLDER}\\{mission_name}.py"):
                    shutil.move(f"{self.LOCAL_MISSION_FOLDER}\\{mission_name}.py", f"{self.DISABLE_MISSION_FOLDER}\\{mission_name}.py")
            else:
                if os.path.exists(f"{self.DISABLE_MISSION_FOLDER}\\{mission_name}.py"):
                    shutil.move(f"{self.DISABLE_MISSION_FOLDER}\\{mission_name}.py", f"{self.LOCAL_MISSION_FOLDER}\\{mission_name}.py")
        self.local_mission_names, self.enable_mission_names, self.disable_mission_names = self._read_local_mission_names()

    def _apply_delete(self, delete_list, delete_backup=False):
        # Delete mission in the delete_list
        for mission_name in delete_list:
            if mission_name in self.local_mission_names:
                if os.path.exists(f"{self.LOCAL_MISSION_FOLDER}\\{mission_name}.py"):
                    os.remove(f"{self.LOCAL_MISSION_FOLDER}\\{mission_name}.py")
                if os.path.exists(f"{self.DISABLE_MISSION_FOLDER}\\{mission_name}.py"):
                    os.remove(f"{self.DISABLE_MISSION_FOLDER}\\{mission_name}.py")
                if delete_backup:
                    backup_folder = f"{self.BACKUP_MISSION_FOLDER}\\{mission_name}"
                    if os.path.exists(backup_folder):
                        shutil.rmtree(backup_folder)
        self.local_mission_names, self.enable_mission_names, self.disable_mission_names = self._read_local_mission_names()
        output.set_processbar("PROGRESS_APPLY_AND_SAVE", 0.1)

    def _apply_and_save(self, disable_list, update_list, disable_all, delete_list, delete_backup):
        """
        Apply the changes (update, disable, delete).

        Args:
            disable_list (List): A list containg the mission names to be disabled.
            update_list (List): A list containg the mission names to be updated.
            disable_all (Boolean): Disable all missions if True.
            delete_list (List): A list containg the mission names to be deleted.
            delete_backup (Boolean): Delete the backup folder of mission if True.
        """
        self.error_occured = False

        self._render_progress_popup()

        self._refresh_available_missions()
        
        # Prioirity: Delete, Update, Disable

        # Handel Delete
        self._apply_delete(delete_list, delete_backup)

        # Handle Update
        update_list = set(update_list)
        job_count = len(update_list)
        i_count = 1

        for i, mission_name in enumerate(self.local_mission_names):
            if mission_name in update_list:
                try:
                    if mission_name in self.available_missions_dict:
                        # NOTE: Multi thread may be needed here.
                        self._download_mission(self.available_missions_dict[mission_name])
                    else:
                        self.error_occured = True
                        logger.error(f"Mission {mission_name} is not available in the remote.")
                        output.toast(f"Mission {mission_name} is not available in the remote.", duration = 5, color="error")
                except Exception:
                    self.error_occured = True
                    logger.error(f"Error getting updates for {mission_name}: {Exception}")
                    output.toast(f"Error getting updates for {mission_name}", duration = 5, color="error")
                output.set_processbar("PROGRESS_APPLY_AND_SAVE", min(0.1+i_count/job_count*0.8, 0.9))
                i_count += 1
        
        # Handle Disable
        if disable_all:
            disable_list = self.local_mission_names
        self._apply_disable(disable_list)

        output.set_processbar("PROGRESS_APPLY_AND_SAVE", 1)
        self._render_installed_board()
        self._render_available_board()
        
        t = threading.Thread(target = generate_mission_index)
        t.start()
        for i in range(1,400-1):
            time.sleep(0.1)
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, i/400)
            if not t.is_alive():
                break
        for i in range(60):
            if not t.is_alive():
                break
            time.sleep(1)
        if t.is_alive():
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0)
            self.error_occured = True
        else:
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 1)
        
        if not self.error_occured:
            output.put_button(t2t("Finished!"), color="success", onclick=lambda :output.close_popup(), scope="POPUP_CLOSE")
        else:
            output.put_button(t2t("Something went wrong! Please try again"), color="danger", onclick=lambda :output.close_popup(), scope="POPUP_CLOSE")
    
    def _onclick_apply_and_save(self):
        # generate disable list
        disable_list = []
        for mission_name in self.local_mission_names:
            if pin.pin[f"ENABLED_{mission_name}"] != [""]:
                disable_list.append(mission_name)
        disable_all = True if pin.pin["RADIO_DISABLE_ALL_MISSIONS"] == "Yes" else False
        update_list = []
        for mission_name in self.local_mission_names:
            if pin.pin[f"UPDATE_{mission_name}"] == [t2t("Update")]:
                update_list.append(mission_name)
        delete_list = []
        for mission_name in self.local_mission_names:
            if pin.pin[f"DELETE_{mission_name}"]:
                delete_list.append(mission_name)
        if len(delete_list) > 0:
            self._render_delete_confirm_popup(disable_list, update_list, disable_all, delete_list)
        else:
            self._apply_and_save(disable_list, update_list, disable_all, [], False)
    
    def _check_updates(self):
        """
        Check if there is any updates for the missions.

        Returns:
            Dict: A dict containing the mission names and the update status.
        """
        self._refresh_available_missions()

        process_mission_names = self.local_mission_names
        update_status = {}

        for i, mission_name in enumerate(process_mission_names):
            if mission_name not in self.available_missions_dict:
                update_status[mission_name] = t2t("Not available on remote")
                continue
            if mission_name not in self.local_mission_meta:
                update_status[mission_name] = t2t("No meta data in local")
                continue
            if not self.local_mission_meta[mission_name]["last_update"] or not self.available_missions_dict[mission_name]["last_update"]:
                update_status[mission_name] = t2t("No last update info")
                continue
            remote_last_update = datetime.strptime(self.available_missions_dict[mission_name]["last_update"], "%Y-%m-%d %H:%M:%S")
            local_last_update = datetime.strptime(self.local_mission_meta[mission_name]["last_update"], "%Y-%m-%d %H:%M:%S")
            if remote_last_update > local_last_update:
                update_status[mission_name] = t2t("Update available")
            else:
                update_status[mission_name] = t2t("No update available")
        
        return update_status

    def _onclick_check_updates(self):
        output.toast(t2t("Checking updates..."), color="info")
        self.mission_update_status = self._check_updates()
        self._render_installed_table()
        output.toast(t2t("Finished checking updates"), color="success")

    def _make_commit_link(self, commit_hash, remote, text=None):
        if text is None:
            text = commit_hash[:8]
        if remote.startswith("https://github.com/"):
            if remote.endswith(".git"):
                remote = remote[:-4]
            href = remote + "/commit/" + commit_hash
            return f'<a href="{href}" target="_blank">{text}</a>'
        else:
            return text
    
    def _normalize_git_url(self, url):
        if url is None:
            return ""

        url = url.replace(".git", "")
        return url
    
    def _get_available_missions_display(self, hide_tags, sort_column=0, filter_text=""):
        """
        Get the list of available missions to display according to the filter.
        The format of available_missions_display is the same as available_missions["missions"].

        Args:
            hide_tags (List): The list of tags to hide.
            sort_column (int): The ordering to sort by. Defaults to 0.
            filter_text (str, optional): The text to filter by. Defaults to "".

        Returns:
            List, int: available_missions_display, number of missions hidden
        """
        missionlist = self.available_missions["missions"]
        available_missions_display = []

        tags_to_hide = set(hide_tags)
        hidden_number = 0
        
        sort_ordering = [
            # (reverse, order_by_function)
            (True, lambda x: x.get("last_update", "z")),
            (False, lambda x: x.get("last_update", "z")),
            (False, lambda x: x.get("name", "z")),
            (True, lambda x: x.get("name", "z")),
            (False, lambda x: "z"),
        ]
        sort_reverse, sort_function = sort_ordering[sort_column if 0 <= sort_column < len(sort_ordering) else 0]

        for mission in sorted(missionlist, key=sort_function, reverse=sort_reverse):
            name = mission.get("name", "")

            mission_tags = mission.get("tags", [])

            # Examines if the mission is installed
            if t2t("installed") not in mission_tags:
                existing = name in self.local_mission_names
                mission_tags = mission_tags + [t2t("installed")] if existing else mission_tags
                mission["tags"] = mission_tags

            if len([x for x in mission_tags if x in tags_to_hide]) > 0:
                hidden_number += 1
                continue

            if filter_text and filter_text.strip():
                search_field = ["name", "title", "tags", "author", "description"]
                search_content = " ".join([str(mission.get(x, "")) for x in search_field])
                if filter_text.lower() not in search_content.lower():
                    hidden_number += 1
                    continue
            available_missions_display.append(mission)
        
        return available_missions_display, hidden_number


    """
    The following functions are for testing purposes only.
    """
    def _test_function(self):
        with output.use_scope(self.main_scope):
            with output.use_scope("missiondownload_test"):
                output.put_markdown("## Test functions")
                output.put_button(label = "_read_local_mission_names", onclick = self._test_read_local_mission_names)
                output.put_button(label = "_refresh_available_missions", onclick = self._test_refresh_available_missions)
                output.put_button(label = "_download_mission", onclick = self._test_download_mission)
                output.put_button(label = "_apply_disable", onclick = self._test_apply_disable)
                output.put_button(label = "_check_updates", onclick = self._test_check_updates)

    def _test_read_local_mission_names(self):
        logger.info("=== test _read_local_mission_names ===")
        logger.info(self._read_local_mission_names())
    
    def _test_refresh_available_missions(self):
        logger.info("=== test _refresh_available_missions ===")
        self._refresh_available_missions()
        logger.info(self.available_missions)
        logger.info(self.available_missions_dict)
    
    def _test_download_mission(self):
        logger.info("=== test _download_mission ===")
        self._download_mission(self.available_missions_dict["MissionGlazeLily"])
        logger.info(self.local_mission_names)
        logger.info(self.local_mission_meta)
    
    def _test_apply_disable(self):
        logger.info("=== test _apply_disable ===")
        self._apply_disable(["MissionGlazeLily"])
        logger.info(self.local_mission_names)
        logger.info(self.enable_mission_names)
        logger.info(self.disable_mission_names)

        self._apply_disable(["MissionQingXin1", "MissionGlazeLily"])
        logger.info(self.local_mission_names)
        logger.info(self.enable_mission_names)
        logger.info(self.disable_mission_names)

        self._apply_disable(["MissionQingXin1"])
        logger.info(self.local_mission_names)
        logger.info(self.enable_mission_names)
        logger.info(self.disable_mission_names)
    
    def _test_check_updates(self):
        logger.info("=== test _check_updates ===")
        logger.info(self.available_missions_dict)
        logger.info(self.local_mission_meta)
        logger.info(self._check_updates())
        logger.info(self.available_missions_dict)
        logger.info(self.local_mission_meta)