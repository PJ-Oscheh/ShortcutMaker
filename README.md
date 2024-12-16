# Shortcut Maker

Easily create shortcuts on the GNOME desktop

<p align="center">
  <img src=./data/icons/io.github.pj_oscheh.shortcutmaker.svg width=256 height=256/>
</p>

<p align="center">
  <img src=https://github.com/user-attachments/assets/f541e31e-a9c6-4235-8e84-f516f0382e0c />
</p>

Ever come across a stubborn one-off app that REFUSES to ship as anything but a stand-alone binary? You know the one. Often times, these apps won't come with an install script (at least, one that creates a proper desktop icon!). For these apps,
let Shortcut Maker come to the rescue. It simplifies the process of creating a `.destkop` file by guiding the user through the shortcut creation process.

## Supported Features
Currently, the application supports:
### Creating Shortcuts
For creating shortcuts, this app supports:
- Naming the shortcut (`Name`)
- Setting the executable path (`Exec`)
- Setting the icon (`Icon`)
- Specifying whether the terminal should be used (`Terminal`)
- Setting comments (`Comment`)
- Specifying categories (although without any fancy front-end; just as a string) (`Categories`)

### Opening Shortcuts
Any `.desktop` file can be opened in Shortcut Maker and modified. That said, I strongly recommend against trying to modify shortcuts not made with Shortcut Maker - its primary purpose is to help users out when they make a typo in the shortcut.

### Deleting Shortcuts
Any `.desktop` file can be deleted using this app. Like with opening shortcuts, this is primarily used for deleting shortcuts created using Shortcut Maker and no longer needed. While it can delete shotcuts created from other applications,
I recommend against it. I also can't guarantee that those other applications won't bring back those `.desktop` files down the line, or if they'll break expecting to use that file for something.

This app creates `.desktop` files according to the [FreeDesktop Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/). While this app should work fine on KDE and other desktop environments
that follow these specifications, I haven't tested those environments.

## Development Information
Stack:
- UI Toolkit: GTK 4 and Adwaita
- Language: Python
