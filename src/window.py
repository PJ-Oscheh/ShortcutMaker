# window.py
#
# Copyright 2023 PJ Oschmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
from datetime import datetime
import os




@Gtk.Template(resource_path='/io/github/pj_oscheh/shortcutmaker/window.ui')
class ShortcutmakerWindow(Adw.ApplicationWindow):

    __gtype_name__ = 'ShortcutmakerWindow'

    #Header Bar:
    header_bar = Gtk.Template.Child()
    hbTitle = Gtk.Template.Child()


    #Header buttons:
    btnCancel = Gtk.Template.Child()
    btnCreate = Gtk.Template.Child()

    #Action Rows (and Entry, Expander rows)
    arName = Gtk.Template.Child()
    arExecPath = Gtk.Template.Child()
    arIcon = Gtk.Template.Child()
    arIconPath = Gtk.Template.Child()
    arComment = Gtk.Template.Child()
    arCategories = Gtk.Template.Child()
    arMore = Gtk.Template.Child()

    #Check Button for terminal usage
    cbUseTerminal = Gtk.Template.Child()

    #Navigation View
    navigation_view = Gtk.Template.Child()

    #Boxes (represent nav view pages)
    mainBox = Gtk.Template.Child()
    iconBox = Gtk.Template.Child()
    doneBox = Gtk.Template.Child()

    #Radio Buttons for icon usage
    rbUseIcon = Gtk.Template.Child()
    rbNoIcon = Gtk.Template.Child()

    #File Dialog
    open_dialog = Gtk.FileDialog.new()



    #Label and image for icon preview
    lblIconPrev = Gtk.Template.Child()
    imgIconPrev = Gtk.Template.Child()

    #Image and label on done page
    lblDone = Gtk.Template.Child()
    imgDone = Gtk.Template.Child()

    #Toast
    toast_overlay = Gtk.Template.Child()


    #Get username
    username = os.getlogin()

    #Keep track open file
    current_file = None

    #Temporarily store file to delete between logic and callback
    delete_file = None

    #Callbacks
    @Gtk.Template.Callback()
    def do_cancel(self, button):
        """Callback for Cancel button

            Args:
                button: Button clicked
            """
        self.closeEditShortcut()

    @Gtk.Template.Callback()
    def do_close(self, button):
        """Callback for Close and Finish button

            Args:
                button: Button clicked
            """
        self.destroy()

    @Gtk.Template.Callback()
    def do_create(self, button):
        """Callback for Create button (same as Edit button)

            Args:
                button: Button clicked
            """
        #If editing, remove the previous file as a new one will be made
        #Two checks since it's a destructive action
        if (button.get_label() == "_Edit" and self.current_file != None):
            os.remove(self.current_file)
            self.current_file = None

        summary = self.makeShortcut()

        self.lblDone.set_label(summary[0][6:])

        if summary[2][6:] != "":
            self.imgDone.set_visible(True)
            self.imgDone.set_from_file(summary[2][6:])
        else:
            self.imgDone.set_visible(False)
        self.navigation_view.push_by_tag("created_page")




    @Gtk.Template.Callback()
    def open_set_icon(self, actionRow):
        """Callback for Icon action row

            Args:
                actionRow: Action Row clicked
            """
        self.navigation_view.push_by_tag("icon_page")


    @Gtk.Template.Callback()
    def go_back(self, button):
        """Callback for back button

            Args:
                button: Button clicked
            """
        self.navigation_view.navigate(Adw.NavigationDirection.BACK)

    @Gtk.Template.Callback()
    def open_icon(self, button):
        """Callback for Open Icon button

            Args:
                button: Button clicked
            """
        self.show_open_dialog(button,"PICK_ICON")
        self.rbUseIcon.set_active(True)

    @Gtk.Template.Callback()
    def open_exec(self, button):
        """Callback for Open Executable button

            Args:
                button: Button clicked
            """
        self.show_open_dialog(button,"PICK_EXEC")

    @Gtk.Template.Callback()
    def use_icon_text_changed(self, entryRow):
        """Callback for Icon Path text changed

            Args:
                entryRow: Entry Row edited
            """
        self.rbUseIcon.set_active(True)
        self.use_icon(self.arIconPath.get_text(), False)

    @Gtk.Template.Callback()
    def name_exec_text_changed(self, entryRow):
        """Callback for Executable Path text changed

            Args:
                entryRow: Entry Row edited
            """
        if len(self.arName.get_text()) != 0 and len(self.arExecPath.get_text()) !=0:
            self.btnCreate.set_sensitive(True)
        else:
            self.btnCreate.set_sensitive(False)

    @Gtk.Template.Callback()
    def rbIconsToggled(self, checkButton):
        """Callback for Icon radio buttons

            Args:
                checkButton: Radio Button toggled
            """
        if self.rbUseIcon.get_active() == True:
            self.rbUseIconActive()
        elif self.rbNoIcon.get_active() == True:
            self.rbNoIconActive()

    @Gtk.Template.Callback()
    def do_create_another(self, button):
        """Callback for Create Another button

            Args:
                button: Button clicked
            """
        self.closeEditShortcut()

    #Dialogs created at runtime
    def unsupp_dlg_response_cb(self, dialog, response):
        """Opens a dialog warning the user of unsupported properties

        Args:
            dialog: The Adw Message Dialog
            response: The response the user picks
        """
        #Responses in UI file break dialog
        if response == "cancel":
            self.closeEditShortcut()

    #Dialogs created at runtime
    def delete_dlg_response_cb(self, dialog, response):
        """Opens a dialog warning the user that delete can't be undone

        Args:
            dialog: The Adw Message Dialog
            response: The response the user picks
        """
        if response == "delete":
            self.delete_shortcut(True, None, True)




    def resetAllFields(self):
        """Resets all elements to their default conditions"""
        self.arName.set_text("")
        self.arExecPath.set_text("")
        self.arIconPath.set_text("")
        self.rbNoIcon.set_active(True)
        self.cbUseTerminal.set_active(False)
        self.arComment.set_text("")
        self.arCategories.set_text("")
        self.arMore.set_expanded(False)
        self.imgIconPrev.set_from_file("")

        self.navigation_view.pop_to_tag("main_page")

    def closeEditShortcut(self):
        """Return app to default conditions and indicate in UI that the app
        will create a new shortcut rather than edit one.
        """
        self.resetAllFields()
        self.hbTitle.set_title("Create Shortcut")
        self.hbTitle.set_subtitle("")
        self.btnCancel.set_visible(False)
        self.btnCreate.set_label("_Create")
        self.btnCreate.get_style_context().remove_class("destructive-action")
        self.btnCreate.get_style_context().add_class("suggested-action")
        self.current_file = None


    def rbUseIconActive(self):
        """If using an icon, show a preview"""
        self.use_icon(self.arIconPath.get_text(),False)
        self.setIconPreviewVisibility(True)

    def rbNoIconActive(self):
        """If not using an icon, don't show a preview"""
        self.arIcon.set_subtitle("No icon set.")
        self.setIconPreviewVisibility(False)

    def open_shortcut(self, hasPath, path=None):
        """Opens a .desktop shortcut file

        Args:
            hasPath: Boolean, whether to show open dialog to select file,
                or to continue handling the file.
            path: Path to the .desktop file. Defaults to None.
        """
        #Open the file
        if hasPath == False:
            self.show_open_dialog(None, "OPEN_SHORTCUT")

        #Handle the file
        else:

            #Make Create Button suggested-action, if unsupported shortcut previously opened
            self.btnCreate.get_style_context().remove_class("destructive-action")
            self.btnCreate.get_style_context().add_class("suggested-action")

            #Keep track of open file
            self.current_file = path

            #Set window subtitle
            self.hbTitle.set_title("Edit Shortcut")
            self.hbTitle.set_subtitle(path)
            with open(path, "r") as file:
                lines = file.readlines()

            #Change button text:
            self.btnCancel.set_visible(True)

            self.btnCreate.set_label("_Edit")

            #Reset all widgets before filling them in with new information
            self.resetAllFields()

            #Track unsupported properties and warn user
            unsupportedProps = False
            strUnsupportedProps = ""
            #Read each line. Read before equal sign, then set value to that.
            for i in range(1,len(lines)):
                prop = lines[i].strip().find("=")
                #Set name
                if (lines[i].strip()[:prop] == "Name"):
                    self.arName.set_text(lines[i].strip()[prop+1:])
                elif (lines[i].strip()[:prop] == "Exec"):
                    self.arExecPath.set_text(lines[i].strip()[prop+1:])
                elif (lines[i].strip()[:prop] == "Icon"):
                    self.arIconPath.set_text(lines[i].strip()[prop+1:])
                    self.rbNoIconActive()
                    self.rbUseIconActive()
                elif (lines[i].strip()[:prop] =="Terminal"):
                    if (lines[i].strip()[prop+1:] == "true"):
                        self.cbUseTerminal.set_active(True)
                elif (lines[i].strip()[:prop] == "Comment"):
                    self.arComment.set_text(lines[i].strip()[prop+1:])
                elif (lines[i].strip()[:prop] == "Categories"):
                    self.arCategories.set_text(lines[i].strip()[prop+1:])
                elif (lines[i].strip()[:prop] == "Type"):
                    #Type is handled automatically
                    #Avoid triggering else.
                    pass
                else:
                    unsupportedProps = True



            if (unsupportedProps):
                #Create a dialog telling the user the shortcut might break if edited
                #(For example, shortcuts made by other applications with additional props)
                dlgUnsuppProps = Adw.MessageDialog()
                dlgUnsuppProps.set_heading("Unsupported Properties")
                dlgUnsuppProps.set_body("This shortcut uses unsupported properties. They will be lost upon saving, and the shortcut may break. Do you still want to edit it?")
                dlgUnsuppProps.set_modal(True)
                dlgUnsuppProps.set_transient_for(self)
                dlgUnsuppProps.add_response("cancel","_Cancel")
                dlgUnsuppProps.add_response("proceed","_Proceed")
                dlgUnsuppProps.set_response_appearance("proceed",Adw.ResponseAppearance.DESTRUCTIVE)
                dlgUnsuppProps.set_default_response("cancel")
                dlgUnsuppProps.connect('response',self.unsupp_dlg_response_cb)
                Gtk.Window.present(dlgUnsuppProps)
                self.btnCreate.get_style_context().remove_class("suggested-action")
                self.btnCreate.get_style_context().add_class("destructive-action")

            if (unsupportedProps == False and "_ShortcutMaker_" not in path):
                toastWarning = Adw.Toast(title="This shortcut wasn't made in Shortcut Maker. Be careful!")
                self.toast_overlay.add_toast(toastWarning)


    def delete_shortcut(self, hasPath, path=None, doDelete=False):
        """Deletes a shortcut. Asks the user for confirmation, then deletes.

        Args:
            hasPath: Boolean, whether to show open dialog to select file,
                or to continue handling the file.
            path: Path of .desktop file to delete. Defaults to None.
            doDelete: Whether to delete file. Condition is explicitly
                checked to ensure it isn't reached accidentally.
            """
        if (hasPath == False):
            self.show_open_dialog(None,"DELETE_SHORTCUT")
        elif (hasPath == True and doDelete == False):

            self.delete_file = path

            dlgDelete = Adw.MessageDialog()
            dlgDelete.set_heading("Delete Shortcut?")
            dlgDelete.set_body(f"Delete \"{path}\"? This action can't be undone!\n\nIt's only recommended to delete a shortcut if it was made with Shortcut Maker.")
            dlgDelete.set_modal(True)
            dlgDelete.set_transient_for(self)
            dlgDelete.add_response("cancel","_Cancel")
            dlgDelete.add_response("delete","_Delete")
            dlgDelete.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
            dlgDelete.set_default_response("cancel")
            dlgDelete.connect('response',self.delete_dlg_response_cb)
            Gtk.Window.present(dlgDelete)

        elif (doDelete == True): #Could be else, but check condition to be safe since it's destructive
            path = self.delete_file
            self.delete_file = None
            os.remove(path)
            toast = Adw.Toast(title=f"Deleted \"{path}\"")
            self.toast_overlay.add_toast(toast)



    #File picker
    def show_open_dialog(self, button, situation):
        """Opens the file picker, handling different types of situations.

        Args:
            button: The button clicked
            situation: Set the file picker title and filters based on the desired
                action.

        NOTE: Courtesy https://github.com/Taiko2k/GTK4PythonTutorial (and for
            syntax of file picker callbacks as well)
        """

        if (situation == "PICK_ICON"):
            f = Gtk.FileFilter()
            f.set_name("Image Files")
            f.add_mime_type("image/png")
            f.add_mime_type("image/svg+xml")
            self.open_dialog.set_title("Select Icon")

        elif (situation == "PICK_EXEC"):
            f = Gtk.FileFilter()
            f.set_name("Executable Files")
            f.add_mime_type("application/octet-stream")
            self.open_dialog.set_title("Select Application")

        elif (situation == "OPEN_SHORTCUT"):
            f = Gtk.FileFilter()
            f.set_name("Open Shortcut")
            f.add_mime_type("text/plain")
            self.open_dialog.set_title("Select Shortcut")

            #Default folder can't be set. Is this related to
            #xdg-desktop-portal-gnome Issue 5806?
            default_folder = Gio.File.new_for_path(f"/home/{self.username}/.local/share/applications")
            self.open_dialog.set_initial_folder(default_folder)

        elif (situation == "DELETE_SHORTCUT"):
            f = Gtk.FileFilter()
            f.set_name("Delete Shortcut")
            f.add_mime_type("text/plain")
            self.open_dialog.set_title("Delete Shortcut")

            default_folder = Gio.File.new_for_path(f"/home/{self.username}/.local/share/applications")
            self.open_dialog.set_initial_folder(default_folder)


        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(f)

        self.open_dialog.set_filters(filters)
        self.open_dialog.set_default_filter(f)

        if (situation == "PICK_ICON"):
            self.open_dialog.open(self, None, self.open_dialog_callback_icon)

        elif (situation == "PICK_EXEC"):
            self.open_dialog.open(self, None, self.open_dialog_callback_exec)

        elif (situation == "OPEN_SHORTCUT"):
            self.open_dialog.open(self, None, self.open_dialog_callback_open_sc)

        elif (situation == "DELETE_SHORTCUT"):
            self.open_dialog.open(self, None, self.open_dialog_callback_delete_sc)

    def open_dialog_callback_icon(self, dialog, result):
        """Open Dialog callback for setting icon

        Args:
            dialog: The file picker
            result: The user's action
        """
        try:
            file = dialog.open_finish(result)
            if file is not None:
                path=file.get_path()
                self.use_icon(path, True)
                self.imgIconPrev.set_from_file(path)
                self.setIconPreviewVisibility(True)
        except GLib.Error as error:
            print(f"Error: {error.message}")

    def open_dialog_callback_exec(self, dialog, result):
        """Open Dialog callback for setting execution path

        Args:
            dialog: The file picker
            result: The user's action
        """
        try:
            file = dialog.open_finish(result)
            if file is not None:
                path=file.get_path()
                self.set_exec_path(path,True)
        except GLib.Error as error:
            print(f"Error: {error.message}")

    def open_dialog_callback_open_sc(self, dialog, result):
        """Open Dialog callback for opening shortcut to edit

        Args:
            dialog: The file picker
            result: The user's action
        """
        try:
            file = dialog.open_finish(result)
            if file is not None:
                path = file.get_path()
                self.open_shortcut(True,path)
        except GLib.Error as error:
            print(f"Error: {error.message}")

    def open_dialog_callback_delete_sc(self, dialog, result):
        """Open Dialog callback for opening shortcut to delete

        Args:
            dialog: The file picker
            result: The user's action
        """
        try:
            file = dialog.open_finish(result)
            if file is not None:
                path = file.get_path()
                self.delete_shortcut(True, path)
        except GLib.Error as error:
            print(f"Error: {error.message}")

    def setIconPreviewVisibility(self, visibility):
        """Whether the icon preview should be visible. If the preview
        would show the image-missing icon, hide it.

        Args:
            visibility: Request the icon to be visible, as long as the path is
                valid
        """
        if visibility and self.imgIconPrev.get_icon_name() != "image-missing":
            self.lblIconPrev.set_visible(True)
            self.imgIconPrev.set_visible(True)
        else:
            self.lblIconPrev.set_visible(False)
            self.imgIconPrev.set_visible(False)


    def use_icon(self, path, changeActionRow):
        """Change GUI text and subtitles depending on whether an icon
            is being used."""
        if (len(path) != 0):
            self.arIcon.set_subtitle(path)
        else:
            self.arIcon.set_subtitle("No icon set.")
        if (changeActionRow):
            self.arIconPath.set_text(path)

    def set_exec_path(self, path, changeActionRow):
        if (changeActionRow):
            self.arExecPath.set_text(path)


    #Make the .desktop file
    def makeShortcut(self):
        """
        Takes fields from the GUI and creates a string for a desktop entry.
        Then, a .desktop file is created at ~/.local/share/applications
        """
        name = "\nName=" + self.arName.get_text().strip()
        exec_path = "\nExec=" + self.arExecPath.get_text().strip()
        icon_path = self.arIconPath.get_text().strip()

        #Check whether to append icon
        if len(icon_path) == 0 or self.rbNoIcon.get_active() == True:
            icon_path = ""
        else:
            icon_path="\nIcon=" + icon_path

        #Check whether to append use terminal
        if self.cbUseTerminal.get_active() == True:
            use_terminal = "\nTerminal=true"
        else:
            use_terminal = "\nTerminal=false"

        #Check whether to append comment
        if len(self.arComment.get_text()) != 0:
            comment = "\nComment=" + self.arComment.get_text()
        else:
            comment = ""

        #Check whether to append categories
        if len(self.arCategories.get_text()) != 0:
            categories = "\nCategories=" + self.arCategories.get_text()
        else:
            categories = ""



        desktopString = f"[Desktop Entry]\nType=Application{name}{exec_path}{icon_path}{use_terminal}{comment}{categories}"


        filePath = "/home/" + self.username + "/.local/share/applications/" + name[6:].replace(" ","_") + ".desktop"
        fileName = name[6:].replace(" ","_") + "_ShortcutMaker_" + self.getTime()
        filePath = "/home/" + self.username + "/.local/share/applications/" + fileName + ".desktop"




        with open(filePath, "w") as workingFile:
            workingFile.write(desktopString)

        return [name,exec_path,icon_path,use_terminal,comment,categories]

    def getTime(self):
        """Return the current time as a string, with no spaces or formatting.
            Ensures each .desktop file has a unique name"""
        currentTime = str(datetime.now())
        currentTime = currentTime.replace("-","")
        currentTime = currentTime.replace(" ", "")
        currentTime = currentTime.replace(":","")
        currentTime = currentTime.replace(".","")
        currentTime = currentTime[2:16]
        return currentTime


    def __init__(self, **kwargs):
        super().__init__(**kwargs)









